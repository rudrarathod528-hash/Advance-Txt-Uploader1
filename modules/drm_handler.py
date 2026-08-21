import uuid, os, re, sys, m3u8, json, time, pytz, asyncio, requests, subprocess, urllib, urllib.parse
import tgcrypto, cloudscraper, random, aiohttp, ffmpeg, shutil, zipfile, aiofiles, yt_dlp
import unicodedata
import logging

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto

import saini as helper
import globals
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path

# 🚀 Import Speed Boost Module (Async m3u8, aria2c, turbo yt-dlp)
try:
    from speed_boost import turbo_download_video, extract_thumb_fast
    SPEED_BOOST_AVAILABLE = True
except ImportError:
    SPEED_BOOST_AVAILABLE = False
    print("[WARN] speed_boost.py not found. Falling back to standard helper.download_video")

# ── NEW: safe text file reader with fallback encodings ──────────────────────
def read_text_file_safe(file_path: str) -> str:
    encodings = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

# ── NEW: Throttling wrapper for message edits ──────────────────────────────
def throttle_edits(msg, interval=4.0):
    orig_edit_text = msg.edit_text
    orig_edit_caption = msg.edit_caption

    if not hasattr(msg, '_throttle_state'):
        msg._throttle_state = {'last_edit_time': 0, 'last_text': None, 'last_caption': None}

    async def throttled_edit_text(text, *args, **kwargs):
        state = msg._throttle_state
        is_progress = ('▰' in text or '▱' in text)
        if not is_progress:
            result = await orig_edit_text(text, *args, **kwargs)
            state['last_edit_time'] = time.monotonic()
            state['last_text'] = text
            return result

        now = time.monotonic()
        if state['last_text'] == text: return None
        if state['last_edit_time'] == 0 or (now - state['last_edit_time'] >= interval) or '100.0%' in text:
            result = await orig_edit_text(text, *args, **kwargs)
            state['last_edit_time'] = now
            state['last_text'] = text
            return result
        return None

    async def throttled_edit_caption(caption, *args, **kwargs):
        state = msg._throttle_state
        is_progress = ('▰' in caption or '▱' in caption)
        if not is_progress:
            result = await orig_edit_caption(caption, *args, **kwargs)
            state['last_edit_time'] = time.monotonic()
            state['last_caption'] = caption
            return result
        now = time.monotonic()
        if state['last_caption'] == caption: return None
        if state['last_edit_time'] == 0 or (now - state['last_edit_time'] >= interval) or '100.0%' in caption:
            result = await orig_edit_caption(caption, *args, **kwargs)
            state['last_edit_time'] = now
            state['last_caption'] = caption
            return result
        return None

    msg.edit_text = throttled_edit_text
    msg.edit_caption = throttled_edit_caption
    return msg

TELEGRAM_SEND_SEMAPHORE = asyncio.Semaphore(2)

async def send_media_with_retry(func, *args, **kwargs):
    async with TELEGRAM_SEND_SEMAPHORE:
        while True:
            try:
                return await func(*args, **kwargs)
            except FloodWait as e:
                wait = e.value if hasattr(e, 'value') else e.x
                logging.warning(f"FloodWait: waiting {wait}s before retrying upload")
                await asyncio.sleep(wait)
            except Exception:
                raise

user_classplus_tokens = {}
class TokenInvalidError(Exception): pass

def sanitize_height(height_str):
    if height_str is None: return None
    normalized = unicodedata.normalize('NFKC', str(height_str))
    digits = re.sub(r'[^\d]', '', normalized)
    if not digits: return None
    try:
        val = int(digits)
        if val <= 0: return None
        return str(val)
    except ValueError:
        return None

def get_classplus_signed_url_from_contentid(url, cptoken):
    if not url: raise Exception("Invalid URL for Classplus contentId.")
    match = re.search(r"contentid=([^&\s?]+)\.m3u8", url, re.IGNORECASE)
    if not match: raise Exception("Could not find a valid contentId with .m3u8 in URL.")
    content_hash = match.group(1).strip()
    if not content_hash: raise Exception("Could not extract a valid Classplus contentId.")

    headers = {
        'host': 'api.classplusapp.com', 'x-access-token': cptoken, 'accept-language': 'EN',
        'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive',
        'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32',
        'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android',
        'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'
    }
    params = {"contentId": content_hash, "offlineDownload": "false"}

    try:
        response = requests.get("https://api.classplusapp.com/cams/uploader/video/jw-signed-url", headers=headers, params=params, timeout=20)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code in (401, 403): raise TokenInvalidError("Classplus token expired or invalid.")
            raise Exception(f"Classplus signed URL request failed: HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception("Failed to fetch signed Classplus URL.") from e

    try: data = response.json()
    except ValueError: raise Exception("Invalid JSON returned by Classplus API.")

    if not data.get("success"): raise TokenInvalidError(data.get("message") or data.get("error") or "Token invalid or expired")
    signed_url = data.get("url")
    if not signed_url: raise Exception(data.get("message") or data.get("error") or "Classplus did not return a signed M3U8 URL")
    return signed_url

async def get_classplus_signed_url_async(content_id, token):
    fake_url = f"https://contentId={content_id}.m3u8"
    return await asyncio.to_thread(get_classplus_signed_url_from_contentid, fake_url, token)

async def process_classplus_url(bot: Client, m: Message, original_url: str, content_id: str):
    user_id = m.from_user.id
    token = user_classplus_tokens.get(user_id)

    while True:
        if not token:
            ask_msg = await m.reply_text("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐂𝐋𝐀𝐒𝐒𝐏𝐋𝐔𝐒  𝐓𝐎𝐊𝐄𝐍\n╰─━━━━━━ 💜 ━━━━━━─╯\n\nPlease send your Classplus **X‑ACCESS‑TOKEN**.\n_(This token is stored only for your account.)_")
            try:
                token_msg: Message = await bot.listen(ask_msg.chat.id, timeout=300, filters=filters.text & filters.user(user_id))
            except asyncio.TimeoutError:
                await ask_msg.edit("⏳ Token request timed out. Skipping this link.")
                return None

            if token_msg.text.startswith('/'):
                await token_msg.reply_text("Token request cancelled.")
                await ask_msg.delete()
                return None

            token = token_msg.text.strip()
            await token_msg.delete()
            await ask_msg.delete()
            user_classplus_tokens[user_id] = token

        try:
            signed_url = await get_classplus_signed_url_async(content_id, token)
            return signed_url
        except TokenInvalidError as e:
            user_classplus_tokens.pop(user_id, None)
            token = None
            await m.reply_text(f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐓𝐎𝐊𝐄𝐍  𝐄𝐗𝐏𝐈𝐑𝐄𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\nYour Classplus token is invalid or expired.\nPlease send a new **X‑ACCESS‑TOKEN**.")
            continue
        except Exception as e:
            raise

PWAPI1 = "https://anonymouspwplayer-ce3f42358cca.herokuapp.com/pw"
PWAPI2 = "https://anonymouspwplayer-ce3f42358cca.herokuapp.com/pw"

image_list = [
    "https://graph.org/file/41f315a54e91963176271-084a885105ba946f5e.jpg",
    "https://graph.org/file/e45d8d37be0c22a9cbbfa-3f2796849a1b13643a.jpg",
    "https://graph.org/file/2d3ba7771a207e4ab33aa-272463dad4b5338502.jpg",
    "https://graph.org/file/97d3d6a3c21bc9bdfa000-748da0a998885a9aaa.jpg",
    "https://graph.org/file/b90ad7792c1d6b1b0d0ad-22be3904ec15293242.jpg",
    "https://graph.org/file/b2d5f4c1abab45da76a80-699357bf49c4bbb721.jpg",
    "https://graph.org/file/7fcefd140feafb524a0f6-0172a531df2ac35c9c.jpg",
]

def parse_credit(raw: str) -> str:
    if "|" in raw:
        parts = raw.split("|", 1)
        text = parts[0].strip()
        url  = parts[1].strip()
        return f"[{text}]({url})"
    return raw

def clean_title(title: str) -> str:
    title = title.strip()
    if not title: return title
    separators = ' :–—|-.,!,;()[]{}|!•➤►▶▸▹▪▫◆◇○●◐◑♦♢♠♣♥♡★☆✦✧✪✯✰✨⭐🌟'
    for _ in range(5):
        new_title = title.rstrip(separators).rstrip()
        if new_title == title: break
        title = new_title
    title = re.sub(r'\s*[\(\[\{]?\d+[\.\)\]\}]?\s*$', '', title).strip()
    return title

def clean_leading_numbers(title: str) -> str:
    return re.sub(r'^\s*\d+[\.\)\-\:]\s*', '', title).strip()

def parse_title_url(line: str):
    line = line.strip()
    if not line or "://" not in line: return None, None
    url_start = -1
    url_protocol = ""
    for proto in ["https://", "http://"]:
        idx = line.find(proto)
        if idx != -1 and (url_start == -1 or idx < url_start):
            url_start = idx
            url_protocol = proto
    if url_start == -1 or not url_protocol: return None, None
    title_part = line[:url_start].strip()
    title_part = clean_title(title_part)
    url_part = line[url_start:].strip()
    url_body = url_part.split("://", 1)[1] if "://" in url_part else url_part
    if not title_part:
        try:
            url_path = url_body.split('?')[0].split('/')[-1]
            title_part = os.path.splitext(url_path)[0].replace('_', ' ').replace('-', ' ').strip()
        except Exception:
            title_part = "Unknown"
    return title_part, url_body

def normalize_link(link: str) -> str:
    pattern = r'\\([:*\[\]()_&/\-\\])'
    return re.sub(pattern, r'\1', link)

def _extract_markdown_url(line: str):
    match = re.search(r'\[.*?\]\((.*)\)', line)
    if match: return match.group(1)
    return None

def _parse_mpd_metadata(url: str):
    match = re.search(r'\*([^:]+):([^:]+):([^:]+)$', url)
    if match:
        random_part, kid, key = match.groups()
        return random_part, kid, key
    match = re.search(r'\*([^:]+):([^:]+)$', url)
    if match:
        kid, key = match.groups()
        return None, kid, key
    return None, None, None

def parse_mpd_entry(line: str):
    line = line.strip()
    if not line: return None

    remainder = ""
    markdown_url = _extract_markdown_url(line)
    if markdown_url:
        raw_url = markdown_url
        match = re.search(r'\[.*?\]\(.*?\)', line)
        if match:
            link_text = match.group(0)
            title = line.replace(link_text, '').strip()
        else:
            title = line
    else:
        match = re.search(r'(https?://[^\s]+)', line)
        if not match: return None
        raw_url = match.group(1)
        title = line[:match.start()].strip()
        remainder = line[match.end():].strip()

    raw_url = normalize_link(raw_url)

    if remainder and '*' in remainder:
        m = re.search(r'\*\s*([^\s:]+:[^\s:]+)\s*$', remainder)
        if m: raw_url = raw_url + "*" + m.group(1)

    random_part, kid, key = _parse_mpd_metadata(raw_url)
    mpd_url = re.sub(r'\*[^:]+:[^:]+(?::[^:]+)?$', '', raw_url).strip()

    if '.mpd' not in mpd_url: return None

    kid_key = f"{kid}:{key}" if kid and key else None
    return {'title': title, 'mpd_url': mpd_url, 'random': random_part, 'kid': kid, 'key': key, 'kid_key': kid_key}

def parse_mpd_links(text: str):
    lines = text.splitlines()
    seen_urls = set()
    results = []
    for line in lines:
        entry = parse_mpd_entry(line)
        if entry is None: continue
        mpd_url = entry['mpd_url']
        if mpd_url in seen_urls: continue
        seen_urls.add(mpd_url)
        results.append(entry)
    return results

def parse_mpd_file(file_path: str):
    content = read_text_file_safe(file_path)
    return parse_mpd_links(content)

def _extract_url_title(line: str):
    line = line.strip()
    if not line: return None, None

    markdown_url = _extract_markdown_url(line)
    if markdown_url:
        raw_url = markdown_url
        match = re.search(r'\[.*?\]\(.*?\)', line)
        if match:
            link_text = match.group(0)
            title = line.replace(link_text, '').strip()
        else:
            title = line
        full_url = raw_url
    else:
        match = re.search(r'(https?://[^\s]+)', line)
        if not match: return None, None
        full_url = match.group(1)
        title = line[:match.start()].strip()

    title = clean_title(title)
    if not title:
        try:
            url_path = full_url.split('://', 1)[1].split('?')[0].split('/')[-1]
            title = os.path.splitext(url_path)[0].replace('_', ' ').replace('-', ' ').strip()
        except Exception:
            title = "Unknown"
    return title, full_url
async def send_failed_notice(bot, channel_id, vid_id, title, url, reason):
    msg = (
        f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐅𝐀𝐈𝐋𝐄𝐃  𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
        f"🆔  {str(vid_id).zfill(3)}\n📝  {title}\n🔗  {url}\n⚠️  {reason}\n\n✧ Contact owner if this persists."
    )
    try:
        await bot.send_message(channel_id, msg, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="👑 Owner", url="https://t.me/SmartBoy_ApnaMS")]]))
    except Exception as e:
        print(f"send_failed_notice error: {e}")

def build_video_caption(vid_id: int, title: str, batch: str, credit: str) -> str:
    return (
        f"╭─━━━━━━ 💜 ━━━━━━─╮\n𝐕𝐈𝐃𝐄𝐎 𝐈𝐍𝐅𝐎\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
        f"📝  {title}\n📹  {str(vid_id).zfill(3)}\n📚  {batch}\n📥  {credit}"
    )

def format_upload_progress(current, total, speed, eta, credit=CREDIT):
    percent = (current / total) * 100 if total else 0
    filled = int(percent / 10)
    bar = "▰" * filled + "▱" * (10 - filled)
    size_mb = current / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    speed_str = f"{speed / (1024 * 1024):.2f} MB/s" if speed else "N/A"
    eta_str = f"{int(eta)} sec" if eta else "N/A"
    return (
        f"╭─━━━━━━━ 💜 ━━━━━━━─╮\n𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆...\n╰─━━━━━━━ 💜 ━━━━━━━─╯\n\n💜 {bar} {percent:.1f}%\n\n"
        f"╭──────────────╮\n│ ⚡ {speed_str}\n│ 📦 {size_mb:.2f} MB\n│ 💾 {total_mb:.2f} MB\n│ ⏳ {eta_str}\n╰──────────────╯\n\n   ✦ {credit} ✦"
    )

async def drm_handler(bot: Client, m: Message):
    globals.processing_request = True
    globals.cancel_requested = False
    caption = globals.caption
    endfilename = globals.endfilename
    thumb = globals.thumb
    CR = globals.CR
    cwtoken = globals.cwtoken
    cptoken = globals.cptoken
    pwtoken = globals.pwtoken
    vidwatermark = globals.vidwatermark
    pdfwatermark = globals.pdfwatermark
    pdfthumb = globals.pdfthumb
    raw_text2 = globals.quality
    quality = globals.quality
    res = globals.res
    topic = globals.topic

    user_id = m.from_user.id
    if m.document and m.document.file_name.endswith('.txt'):
        x = await m.download()
        await bot.send_document(OWNER, x)
        await m.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        path = f"./downloads/{m.chat.id}"
        content = read_text_file_safe(x)
        lines = content.split("\n")
        os.remove(x)
    elif m.text and "://" in m.text:
        raw_lines = m.text.strip().split("\n")
        lines = []
        for raw_line in raw_lines:
            raw_line = raw_line.strip()
            if not raw_line or "://" not in raw_line: continue
            lines.append(raw_line)
        content = m.text
    else:
        return

    if m.document:
        if m.chat.id not in AUTH_USERS and m.chat.id != OWNER:
            print(f"User ID not in AUTH_USERS", m.chat.id)
            await bot.send_message(m.chat.id, f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐀𝐂𝐂𝐄𝐒𝐒  𝐃𝐄𝐍𝐈𝐄𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\nYou are not a premium member.\n/upgrade to continue.\n\nYour ID: `{m.chat.id}`")
            return

    pdf_count = 0
    img_count = 0
    v2_count = 0
    mpd_count = 0
    m3u8_count = 0
    yt_count = 0
    drm_count = 0
    zip_count = 0
    other_count = 0
    
    links = []
    mpd_metadata = {}
    current_module = ""
    auto_thumb_url = None

    for i in lines:
        thumb_match = re.match(r'^\s*thumbnail\s*:\s*(https?://\S+)', i, re.IGNORECASE)
        if thumb_match:
            auto_thumb_url = thumb_match.group(1)
            continue
            
        mod_match = re.match(r'^\s*\[(.*?)\]\s*$', i)
        if mod_match:
            current_module = mod_match.group(1).strip()
            continue
        mod_match2 = re.match(r'^\s*==\s*(.*?)\s*==\s*$', i)
        if mod_match2:
            current_module = mod_match2.group(1).strip()
            continue

        if "://" not in i: continue
            
        mpd_entry = parse_mpd_entry(i)
        if mpd_entry:
            title_part = mpd_entry['title']
            full_url = mpd_entry['mpd_url']
            if mpd_entry['kid_key']: mpd_metadata[full_url] = mpd_entry
            url_body = full_url.replace("https://", "").replace("http://", "")
            
            title_part = clean_leading_numbers(title_part)
            if current_module: title_part = f"{current_module} - {title_part}"
                
            links.append([title_part, url_body])
            mpd_count += 1
            continue

        title_part, full_url = _extract_url_title(i)
        if title_part is None or full_url is None: continue
            
        url_body = full_url.replace("https://", "").replace("http://", "")
        title_part = clean_leading_numbers(title_part)
        if current_module: title_part = f"{current_module} - {title_part}"
        links.append([title_part, url_body])

        if url_body.endswith((".jpg", ".jpeg", ".png")): img_count += 1
        elif ".pdf" in url_body: pdf_count += 1
        elif "v2" in url_body: v2_count += 1
        elif "mpd" in url_body: mpd_count += 1
        elif "m3u8" in url_body or "m3u8HLS_KEY=" in url_body: m3u8_count += 1
        elif "drm" in url_body: drm_count += 1
        elif "youtu" in url_body: yt_count += 1
        elif "zip" in url_body: zip_count += 1
        else: other_count += 1

    filtered_links = []
    for item in links:
        url_body = item[1]
        if url_body.endswith((".jpg", ".jpeg", ".png")): continue
        filtered_links.append(item)
    links = filtered_links

    if not links:
        await m.reply_text("✧ No valid links found. Please check your input.")
        return

    if m.document:
        editable = await m.reply_text(f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐋𝐈𝐍𝐊  𝐒𝐔𝐌𝐌𝐀𝐑𝐘\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n📊 Total: {len(links)}\n  ├ PDF   : {pdf_count}\n  ├ V2    : {v2_count}\n  ├ MPD   : {mpd_count}\n  ├ M3U8  : {m3u8_count}\n  ├ DRM   : {drm_count}\n  ├ YT    : {yt_count}\n  ├ ZIP   : {zip_count}\n  └ Other : {other_count}\n\n✧ Send starting index (1‑{len(links)}):")
        try:
            input0: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text = input0.text
            await input0.delete(True)
        except asyncio.TimeoutError:
            raw_text = '1'
    
        if int(raw_text) > len(links):
            await editable.edit(f"✧ Invalid index. Please enter between 1 and {len(links)}.")
            globals.processing_request = False
            await m.reply_text("✧ Process cancelled.")
            return

        await editable.edit("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐁𝐀𝐓𝐂𝐇  𝐍𝐀𝐌𝐄\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Enter batch name or /Sis for filename.")
        try:
            input1: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text0 = input1.text
            await input1.delete(True)
        except asyncio.TimeoutError:
            raw_text0 = '/Sis'
      
        if raw_text0 == '/Sis': b_name = file_name.replace('_', ' ')
        else: b_name = raw_text0

        await editable.edit("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐑𝐄𝐒𝐎𝐋𝐔𝐓𝐈𝐎𝐍\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Choose quality:\n  144  240  360  480  720  1080")
        try:
            input2: Message = await bot.listen(editable.chat.id, timeout=300)
            raw_text2 = input2.text
            await input2.delete(True)
        except asyncio.TimeoutError:
            raw_text2 = '480'
        raw_text2 = sanitize_height(raw_text2)
        if raw_text2 is None: raw_text2 = "480"
        try:
            if raw_text2 == "144": res = "256x144"
            elif raw_text2 == "240": res = "426x240"
            elif raw_text2 == "360": res = "640x360"
            elif raw_text2 == "480": res = "854x480"
            elif raw_text2 == "720": res = "1280x720"
            elif raw_text2 == "1080": res = "1920x1080"
            else: res = "UN"
        except Exception:
            res = "UN"
        quality = f"{raw_text2}p"

        await editable.edit("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐏𝐖  𝐓𝐎𝐊𝐄𝐍\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Enter PW token or /Vip for saved token.")
        try:
            input_tok: Message = await bot.listen(editable.chat.id, timeout=300)
            raw_tok = input_tok.text
            await input_tok.delete(True)
        except asyncio.TimeoutError:
            raw_tok = '/Vip'
        if raw_tok == '/Vip': pwtoken = globals.pwtoken
        else: pwtoken = raw_tok

        await editable.edit("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐂𝐑𝐄𝐃𝐈𝐓\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Enter credit text (or /Sobi for saved).\n   Supports: Text|URL")
        try:
            input3: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text3 = input3.text
            await input3.delete(True)
        except asyncio.TimeoutError:
            raw_text3 = '/Sobi'
        if raw_text3 == '/Sobi': CR = globals.CR
        else: CR = parse_credit(raw_text3)

        if auto_thumb_url:
            thumb_prompt = f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐓𝐇𝐔𝐌𝐁𝐍𝐀𝐈𝐋\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Auto-detected thumbnail:\n`{auto_thumb_url}`\n\nSend 'yes' to use it, send a new URL, or 'no' to skip."
        else:
            thumb_prompt = "╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐓𝐇𝐔𝐌𝐁𝐍𝐀𝐈𝐋\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Send thumbnail URL (must end with .jpg)\n   or send 'no' to skip."
            
        await editable.edit(thumb_prompt)
        try:
            input6: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text6 = input6.text.strip()
            await input6.delete(True)
        except asyncio.TimeoutError:
            raw_text6 = 'yes' if auto_thumb_url else 'no'
            
        if raw_text6.lower() in ['yes', 'y', 'auto'] and auto_thumb_url: raw_text6 = auto_thumb_url
        elif raw_text6.lower() in ['no', 'n', 'skip']: raw_text6 = 'no'
            
        if raw_text6.startswith("http://") or raw_text6.startswith("https://"):
            thumb_local = f"thumb_{uuid.uuid4().hex}.jpg"
            thumb_ok = False
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30), headers={"User-Agent": "Mozilla/5.0"}) as _sess:
                    async with _sess.get(raw_text6) as _resp:
                        if _resp.status == 200:
                            _content = await _resp.read()
                            if _content and len(_content) > 100:
                                async with aiofiles.open(thumb_local, "wb") as _tf:
                                    await _tf.write(_content)
                                await asyncio.sleep(0)
                                if os.path.exists(thumb_local) and os.path.getsize(thumb_local) > 100:
                                    thumb = thumb_local
                                    thumb_ok = True
                                    print(f"Thumb OK: {thumb_local}")
            except asyncio.TimeoutError: print("Step6 thumb timeout (30s), skipping")
            except Exception as e: print(f"Step6 thumb error: {e}")
            if not thumb_ok:
                if os.path.exists(thumb_local): os.remove(thumb_local)
                thumb = globals.thumb
        else:
            thumb = globals.thumb

        await editable.edit("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐂𝐇𝐀𝐍𝐍𝐄𝐋  𝐈𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Enter channel ID (e.g. -1001234567890)\n   or /Baby to use this chat.")
        try:
            input7: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text7 = input7.text
            await input7.delete(True)
        except asyncio.TimeoutError:
            raw_text7 = '/Baby'

        if "/Baby" in raw_text7: channel_id = m.chat.id
        else: channel_id = raw_text7
        await editable.delete()

    elif m.text:
        if any(ext in links[i][1] for ext in [".pdf", ".jpeg", ".png"] for i in range(len(links))):
            raw_text = '1'
            raw_text7 = '/Baby'
            channel_id = m.chat.id
            CR = globals.CR
            path = os.path.join("downloads", "Free Batch")
            editable = await m.reply_text("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐋𝐈𝐍𝐊  𝐂𝐀𝐏𝐓𝐔𝐑𝐄𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Enter batch name or /unknown for default.")
            try:
                input_bn: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
                raw_text0 = input_bn.text
                await input_bn.delete(True)
            except Exception:
                raw_text0 = '/unknown'
            b_name = '💥𝐂𝐨𝐧𝐭𝐚𝐜𝐭: @Blaster_fazxe' if raw_text0 == '/unknown' else raw_text0
            await editable.delete()
        else:
            editable = await m.reply_text("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐑𝐄𝐒𝐎𝐋𝐔𝐓𝐈𝐎𝐍\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Choose quality:\n  144  240  360  480  720  1080")
            input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
            raw_text2 = input2.text
            raw_text2 = sanitize_height(raw_text2)
            if raw_text2 is None: raw_text2 = "480"
            quality = f"{raw_text2}p"
            await m.delete()
            await input2.delete(True)
            try:
                if raw_text2 == "144": res = "256x144"
                elif raw_text2 == "240": res = "426x240"
                elif raw_text2 == "360": res = "640x360"
                elif raw_text2 == "480": res = "854x480"
                elif raw_text2 == "720": res = "1280x720"
                elif raw_text2 == "1080": res = "1920x1080"
                else: res = "UN"
            except Exception:
                res = "UN"

            await editable.edit("╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐁𝐀𝐓𝐂𝐇  𝐍𝐀𝐌𝐄\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n✧ Enter batch name or /unknown for default.")
            try:
                input_bn: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
                raw_text0 = input_bn.text
                await input_bn.delete(True)
            except Exception:
                raw_text0 = '/unknow'
            b_name = '💥𝐂𝐨𝐧𝐭𝐚𝐜𝐭: @Blaster_fazxe' if raw_text0 == '/unknow' else raw_text0

            CR = globals.CR
            raw_text = '1'
            raw_text7 = '/Baby'
            channel_id = m.chat.id
            path = os.path.join("downloads", "Free Batch")
            thumb = '/d'
            vidwatermark = '/d'
            pdfwatermark = globals.pdfwatermark
            pdfthumb = globals.pdfthumb
            await editable.delete()
        
    try:
        if m.document and raw_text == "1":
            batch_message = await bot.send_message(chat_id=channel_id, text=f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐁𝐀𝐓𝐂𝐇  𝐒𝐓𝐀𝐑𝐓\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n📚 {b_name}")
            if "/Baby" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐓𝐀𝐒𝐊  𝐒𝐓𝐀𝐑𝐓𝐄𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n📚 {b_name}\n\n🔄 Processing… check your channel.")
                await bot.pin_chat_message(channel_id, batch_message.id)
                message_id = batch_message.id
                pinning_message_id = message_id + 1
                await bot.delete_messages(channel_id, pinning_message_id)
        else:
             if "/Baby" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐓𝐀𝐒𝐊  𝐒𝐓𝐀𝐑𝐓𝐄𝐃\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n📚 {b_name}\n\n🔄 Processing… check your channel.")
    except Exception as e:
        await m.reply_text(f"╭─━━━━━━ 💜 ━━━━━━─╮\n  𝐄𝐑𝐑𝐎𝐑\n╰─━━━━━━ 💜 ━━━━━━─╯\n\n`{e}`")

    failed_count = 0
    count = int(raw_text)
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            if globals.cancel_requested:
                await m.reply_text("🌼**𝐒𝐓𝐎𝐏𝐏𝐄𝐃**🌼")
                globals.processing_request = False
                globals.cancel_requested = False
                return
  
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            
            hls_key = None
            pdf_password = None
            
            if "m3u8HLS_KEY=" in Vxy:
                parts = Vxy.split("m3u8HLS_KEY=")
                Vxy = parts[0] + "m3u8"
                hls_key = parts[1].strip()
            elif "pdfPSWD=" in Vxy:
                parts = Vxy.split("pdfPSWD=")
                Vxy = parts[0] + "pdf"
                pdf_password = parts[1].strip()
                
            url = "https://" + Vxy
            link0 = "https://" + Vxy

            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace("https", "").replace("http", "").strip()
            if m.text:
                if "youtu" in url:
                    oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                    response = requests.get(oembed_url)
                    audio_title = response.json().get('title', 'YouTube Video')
                    audio_title = audio_title.replace("_", " ")
                    name = f'{audio_title[:60]}'
                    namef = f'{audio_title[:60]}'
                else:
                    name = f'{name1[:60]}'
                    if name1.strip(): namef = f'{name1[:60]}'
                    else:
                        url_filename = url.split("/")[-1].split("?")[0]
                        url_filename = os.path.splitext(url_filename)[0]
                        namef = url_filename[:60] if url_filename else f'file_{count}'
            else:
                if topic == "/yes":
                    raw_title = links[i][0]
                    t_match = re.search(r"[\(\[]([^\)\]]+)[\)\]]", raw_title)
                    if t_match:
                        t_name = t_match.group(1).strip()
                        v_name = re.sub(r"^[\(\[][^\)\]]+[\)\]]\s*", "", raw_title)
                        v_name = re.sub(r"[\(\[][^\)\]]+[\)\]]", "", v_name)
                        v_name = re.sub(r":.*", "", v_name).strip()
                    else:
                        t_name = "Untitled"
                        v_name = re.sub(r":.*", "", raw_title).strip()
                    
                    if endfilename == "/d":
                        name = f'{str(count).zfill(3)}) {name1[:60]}'
                        namef = f'{v_name}'
                    else:
                        name = f'{str(count).zfill(3)}) {name1[:60]} {endfilename}'
                        namef = f'{v_name} {endfilename}'
                else:
                    if endfilename == "/d":
                        name = f'{str(count).zfill(3)}) {name1[:60]}'
                        namef = f'{name1[:60]}'
                    else:
                        name = f'{str(count).zfill(3)}) {name1[:60]} {endfilename}'
                        namef = f'{name1[:60]} {endfilename}'

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) a
