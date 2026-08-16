import os
import re
import sys
import json
import time
import pytz
import asyncio
import requests
import subprocess
import random
from collections import defaultdict
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
import globals
from logs import logging
from html_handler import register_html_handlers
from drm_handler import register_drm_handlers
from pdf_rename import register_pdf_rename_handlers
from pdfthumb import register_pdfthumb_handlers
from video_cover import register_video_cover_handlers, load_global_videocover_on_start
from video_rename import register_video_rename_handlers
from text_handler import register_text_handlers
from features import register_feature_handlers
from upgrade import register_upgrade_handlers
from commands import register_commands_handlers
from settings import register_settings_handlers
from broadcast import register_broadcast_handlers
from youtube_handler import register_youtube_handlers
from authorisation import register_authorisation_handlers
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path
import user_store
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# ── Random image list ────────────────────────────────────────────────────────
image_list = [
    "https://graph.org/file/41f315a54e91963176271-084a885105ba946f5e.jpg",
    "https://graph.org/file/e45d8d37be0c22a9cbbfa-3f2796849a1b13643a.jpg",
    "https://graph.org/file/2d3ba7771a207e4ab33aa-272463dad4b5338502.jpg",
    "https://graph.org/file/97d3d6a3c21bc9bdfa000-748da0a998885a9aaa.jpg",
    "https://graph.org/file/b90ad7792c1d6b1b0d0ad-22be3904ec15293242.jpg",
    "https://graph.org/file/b2d5f4c1abab45da76a80-699357bf49c4bbb721.jpg",
    "https://graph.org/file/7fcefd140feafb524a0f6-0172a531df2ac35c9c.jpg",
]
# ─────────────────────────────────────────────────────────────────────────────────────────

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ── pyromod bugfix ──────────────────────────────────────────────────────────
# pyromod's message-handler patch runs on EVERY incoming update and does
# `self.listeners[listener_type]` without a fallback. If a listener type
# (e.g. ListenerTypes.MESSAGE) was never registered via listen()/ask(), that
# key doesn't exist in the dict yet and it raises:
#   KeyError: <ListenerTypes.MESSAGE: 'message'>
# on every single message. A defaultdict auto-creates any missing key with
# an empty list, so this works no matter where a given pyromod version/fork
# stores its ListenerTypes enum.
bot.listeners = defaultdict(list)
# ─────────────────────────────────────────────────────────────────────────────

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📜 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="cmd_command")],
            [InlineKeyboardButton("🧩 𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command"), InlineKeyboardButton("⚙️ 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")],
            [InlineKeyboardButton("💎 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐏𝐥𝐚𝐧𝐬", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="🧑‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/CinderellaContactBot"), InlineKeyboardButton(text="👑 𝐎𝐰𝐧𝐞𝐫", url="https://t.me/MR_Toxic_1")],
            [InlineKeyboardButton(text="🎀 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧 𝐁𝐨𝐭", url="https://t.me/Cinderella_recaptionBot"), InlineKeyboardButton(text="🧵 𝐒𝐭𝐫𝐢𝐧𝐠 𝐁𝐨𝐭", url="https://t.me/Cinderella_StringBot")],
        ])

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user_store.register_user(m.chat.id)
    user = await bot.get_me()
    mention = user.mention

    # ── Funny intro: random sticker + random message, auto-delete after 3s ───
    _funny_stickers = [
        "CAACAgQAAxkBAAFLwupqJX_GZsMsZ4vKxBwfGAOG1Euz7wACARcAArCTAAFQdAouNB1rJc47BA",
        "CAACAgQAAxkBAAFLwwABaiWAv8N8krwglxUaqaZAqVHFBIQAAv4ZAAJxARlQagc8NAy31zc7BA",
        "CAACAgQAAxkBAAFLwwRqJYDvJ-13xb2Un4RXhLGwSIaSzwACthMAAk6TsVJWVlvl5KoXAjsE",
        "CAACAgQAAxkBAAFLwwhqJYEmGcRB22SDL1DzL9blbqPAyQACfxMAAmERCVDdA1gaEWW1kTsE",
        "CAACAgUAAxkBAAFL05lqJoLZ-QerDkqU2nNl8sQpnEyOuAACixAAAsX32VRZyV5Pre9nNzsE",
        "CAACAgUAAxkBAAFL06FqJoL8PmQovETo4roJGJqHp2tPQQAC_hUAAlNMYVWcrcTIq12jpDsE",
        "CAACAgIAAxkBAAFL06lqJoMQfJyWwCGyNeWXlKRucSYlKgACdzIAArwF0EgMDONyCH8JTjsE",
        "CAACAgQAAxkBAAFL06tqJoMjdaCrqJfmyWL2QtdiXD2y1AACrSEAAhBb4VCgAphtKkZfRDsE",
        "CAACAgUAAxkBAAFL069qJoM_HXC5M809uNst3VQ4_YeHKgACThMAAljGUFZRGBj2BWiaTTsE",
        "CAACAgUAAxkBAAFL07pqJoNjyTljx_e4XhCgAAGR3LvnzbAAAk4SAAJx4NhXLiw7mX0hn9E7BA",
        "CAACAgUAAxkBAAFL08NqJoOIlsozCZESe3Zde7Ie-5AicwACnAcAAoh_4VaxIDI2w_8W9DsE",
        "CAACAgUAAxkBAAFL08tqJoOpFL8c1JqvStiFDi6eOkjIhAACxBIAAniFEFYlHX1uOsR-5DsE",
    ]
    _funny_messages = [
        "🙈 Oho... aakhir mil hi gayi apne baby se fursat?\nChalo koi baat nahi, ab thoda time mujhe bhi de do. 😏",
        "👀 Welcome yaar...\nItni der laga di, kya /start button dhundhne Japan gaye the? 😂",
        "🙈 Oho... yaad aa hi gayi meri?\nMain to samjha tha tum physics ki tarah mujhe bhi bhul hi gaye. 😏",
        "😏 Oye! Finally aa hi gaye... Main to soch raha thi tum mujhe ignore kar rahe ho🥺.",
        "💭 My life feels like a test and I forgot to study for. 😭",
        "👀 Arre wah, aaj to darshan ho gaye... lagta hai free Wi-Fi mil gaya kahin. 🤣",
        "😌 Welcome back janab, itni late entry to filmo ke hero bhi nahi marte. 😏",
        "👀 Dekho kaun aaya hai... lagta hai aaj duniya ke saare kaam khatam ho gaye. 😏",
    ]
    _idx = random.randint(0, 3)
    _sticker_msg = await bot.send_sticker(chat_id=m.chat.id, sticker=_funny_stickers[_idx])
    _text_msg = await bot.send_message(chat_id=m.chat.id, text=_funny_messages[_idx])
    await asyncio.sleep(3)
    try:
        await _sticker_msg.delete()
        await _text_msg.delete()
    except Exception:
        pass
    # ─────────────────────────────────────────────────────────────────────────

    if m.chat.id in AUTH_USERS:
        caption = (
            f"✨ <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐀𝐂𝐊, 𝐁𝐎𝐒𝐒!</b> 👑\n"
            f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
            f"🚀 𝐈'𝐦 𝐚𝐧 <b>𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭</b>\n\n"
            f"🎬 I can extract <b>Videos</b> &amp; <b>PDFs</b> from your text file "
            f"and send them straight to you!\n\n"
            f"📖 Tap <b>✨ Commands</b> below for the full guide\n"
            f"💎 <b>Status:</b> Premium Member\n"
            f"👨‍💻 <b>Made by:</b> {CREDIT} 🗿"
        )
    else:
        caption = (
            f"💘 <b>𝐇𝐞𝐥𝐥𝐨, {m.from_user.first_name}!</b> 👋\n"
            f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
            f"🚀 𝐈'𝐦 𝐚𝐧 <b>𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭</b>\n\n"
            f"🎬 I can extract <b>Videos</b> &amp; <b>PDFs</b> from your text file "
            f"and send them straight to you!\n\n"
            f"🆓 <b>Plan:</b> Free Version\n"
            f"💎 Want Premium? Press <b>/id</b> to get started\n"
            f"📞 <b>Contact:</b> {CREDIT} to upgrade 🚀"
        )
    await bot.send_photo(
        chat_id=m.chat.id,
        photo=random.choice(image_list),
        caption=caption,
        reply_markup=keyboard
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = (
        f"💕 <b>𝐇𝐞𝐥𝐥𝐨, {first_name}!</b>\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
        f"🚀 𝐈'𝐦 𝐚𝐧 <b>𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭</b>!\n\n"
        f"👨‍💻 <b>By:</b> [{CREDIT}](tg://openmessage?user_id={OWNER})"
    )

    await callback_query.message.edit_media(
      InputMediaPhoto(
        media=random.choice(image_list),
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer("🏠 Back to main menu")

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="📩 𝐒𝐞𝐧𝐝 𝐭𝐨 𝐎𝐰𝐧𝐞𝐫", url=f"tg://openmessage?user_id={OWNER}")]])
    chat_id = message.chat.id
    text = (
        f"🆔 <blockquote expandable><b>𝐓𝐡𝐞 𝐈𝐃 𝐨𝐟 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭 𝐢𝐬:</b></blockquote>\n"
        f"`{chat_id}`\n\n"
        f"💎 Send this ID to the owner to activate Premium!"
    )

    if str(chat_id).startswith("-100"):
        await message.reply_text(text)
    else:
        await message.reply_text(text, reply_markup=keyboard)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    text = (
        f"╭─────────────────╮\n"
        f"│  ✨ <b>𝐘𝐨𝐮𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐈𝐧𝐟𝐨</b> ✨\n"
        f"├─────────────────\n"
        f"├ 🙋 <b>Name :</b> `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else ''}`\n"
        f"├ 🔖 <b>Username :</b> {('@' + update.from_user.username) if update.from_user.username else 'None'}\n"
        f"├ 🆔 <b>User ID :</b> `{update.from_user.id}`\n"
        f"├ 👤 <b>Profile :</b> {update.from_user.mention}\n"
        f"╰─────────────────╯"
    )
    await update.reply_text(
        text=text,
        disable_web_page_preview=True
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("📤 <b>Sending you the logs...</b>")
            await m.reply_document(document=file, caption="🗒️ <b>Bot Activity Logs</b>")
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"❌ <b>Error sending logs:</b>\n<blockquote>{e}</blockquote>")

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["reset"]))
async def restart_handler(_, m):
    if m.chat.id != OWNER:
        return
    else:
        await m.reply_text("🔄 <b>𝐁𝐨𝐭 𝐢𝐬 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠...</b> ⏳", True)
        os.execl(sys.executable, sys.executable, *sys.argv)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("stop") & filters.private)
async def cancel_handler(client: Client, m: Message):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(
            m.chat.id,
            f"<blockquote>🙆🏿‍♀️ <b>Oopss! You are not a Premium member</b>\n"
            f"📈 <b>Please Upgrade Your Plan</b>\n"
            f"📩 <b>Send me your user id for authorization</b>\n"
            f"🆔 <b>Your User ID:</b> `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        if globals.processing_request:
            globals.cancel_requested = True
            await m.reply_text("🚦 <b>Process cancel request received. Stopping after current video...</b>")
        else:
            await m.reply_text("⚡ <b>No active process to cancel.</b>")


#=================================================================

register_text_handlers(bot)
register_html_handlers(bot)
register_feature_handlers(bot)
register_settings_handlers(bot)
register_upgrade_handlers(bot)
register_commands_handlers(bot)
register_broadcast_handlers(bot)
register_youtube_handlers(bot)
register_authorisation_handlers(bot)
register_pdf_rename_handlers(bot)  # MUST be before drm_handlers so /pdfrename is caught first
register_pdfthumb_handlers(bot)    # PDF Thumbnail commands: /setpdfthumb /viewpdfthumb /delpdfthumb
register_video_cover_handlers(bot) # Video Cover commands: /setvideocover /viewvideocover /delvideocover
register_video_rename_handlers(bot) # Video Rename command: /renamevideo
register_drm_handlers(bot)
#==================================================================

def notify_owner():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "✅ <b>𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲</b> 🚀",
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"

    # General users ke liye commands
    general_commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "stop", "description": "🚫 Stop the ongoing process"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"},
        {"command": "cookies", "description": "📁 Upload YT Cookies"},
        {"command": "y2t", "description": "🔪 YouTube → .txt Converter"},
        {"command": "ytm", "description": "🎶 YouTube → .mp3 downloader"},
        {"command": "t2t", "description": "📟 Text → .txt Generator"},
        {"command": "t2h", "description": "🌐 .txt → .html Converter"},
        {"command": "pdfrename", "description": "📄 Rename a PDF file"},
        {"command": "renamevideo", "description": "🎥 Rename a Video file"},
        {"command": "setvideocover", "description": "🖼️ Set Global Video Cover"},
        {"command": "changecover", "description": "🔄 Change Cover of a Video"},
        {"command": "viewvideocover", "description": "👁️ View Current Video Cover"},
        {"command": "delvideocover", "description": "❌ Delete Video Cover"},
        {"command": "logs", "description": "🗒️ View Bot Activity"},
    ]
    # Owner ke liye extra commands
    owner_commands = general_commands + [
        {"command": "broadcast", "description": "📢 Broadcast to All Users"},
        {"command": "broadusers", "description": "👨‍❤️‍👨 All Broadcasting Users"},
        {"command": "addauth", "description": "▶️ Add Authorisation"},
        {"command": "rmauth", "description": "⏸️ Remove Authorisation"},
        {"command": "users", "description": "👨‍👨‍👧‍👦 All Premium Users"},
        {"command": "reset", "description": "🔄 Reset the Bot"}
    ]

    # General users ke liye set commands (scope default)
    requests.post(url, json={
        "commands": general_commands,
        "scope": {"type": "default"},
        "language_code": "en"
    })

    # Owner ke liye set commands (scope user)
    requests.post(url, json={
        "commands": owner_commands,
        "scope": {"type": "chat", "chat_id": OWNER},  # OWNER variable me chat id hona chahiye
        "language_code": "en"
    })

if __name__ == "__main__":
    load_global_videocover_on_start()
    reset_and_set_commands()
    notify_owner()

bot.run()
