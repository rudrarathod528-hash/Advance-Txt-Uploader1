"""
pdfthumb.py — Persistent PDF Thumbnail System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• /setpdfthumb  — URL ya direct image bhejo, thumbnail set hoga
• /viewpdfthumb — current thumbnail dekho
• /delpdfthumb  — thumbnail delete karo
• Bot restart par thumbnail saved rehti hai (JSON file mein)
• /reset (settings) se thumbnail hata jaati hai
• Sirf AUTH USERS use kar sakte hain
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import uuid
import asyncio
import requests

import globals
from vars import AUTH_USERS, CREDIT
from pyrogram import Client, filters
from pyrogram.types import Message

# ── Persistent store file ────────────────────────────────────────────────────
_THUMB_STORE = "pdfthumb_store.json"

# ────────────────────────────────────────────────────────────────────────────
# Storage helpers
# ────────────────────────────────────────────────────────────────────────────

def _load_thumb_store() -> dict:
    """Load persistent thumbnail store from JSON file."""
    if os.path.exists(_THUMB_STORE):
        try:
            with open(_THUMB_STORE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_thumb_store(data: dict):
    """Save thumbnail store to JSON file."""
    try:
        with open(_THUMB_STORE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[pdfthumb] Save error: {e}")


def save_pdfthumb_for_user(user_id: int, thumb_value: str):
    """
    Save pdfthumb value for a user persistently.
    thumb_value can be a URL (graph.org .jpg) or Telegram file_id.
    """
    data = _load_thumb_store()
    data[str(user_id)] = thumb_value
    _save_thumb_store(data)


def get_pdfthumb_for_user(user_id: int) -> str:
    """Get saved pdfthumb for a user. Returns '/d' if not set."""
    data = _load_thumb_store()
    return data.get(str(user_id), "/d")


def delete_pdfthumb_for_user(user_id: int):
    """Remove pdfthumb entry for a user."""
    data = _load_thumb_store()
    data.pop(str(user_id), None)
    _save_thumb_store(data)


def load_global_pdfthumb_on_start():
    """
    Bot start par globals.pdfthumb load karo from store.
    Use OWNER id ya pehle available user ka thumb load karna
    — yahan hum store ki first entry load karte hain as global fallback.
    Agar chahte ho per-user, toh drm_handler mein get_pdfthumb_for_user() call karo.
    """
    data = _load_thumb_store()
    if data:
        # Latest entry use karo (last saved)
        last_val = list(data.values())[-1]
        if last_val and last_val != "/d":
            globals.pdfthumb = last_val
            print(f"[pdfthumb] Loaded pdfthumb from store on start: {last_val[:60]}")


# ────────────────────────────────────────────────────────────────────────────
# Telegram photo → URL converter (upload to graph.org style)
# We simply store the Telegram file_id; download at upload time.
# ────────────────────────────────────────────────────────────────────────────

async def download_and_save_tg_photo(bot: Client, photo_message: Message) -> str | None:
    """
    Telegram se bheja gaya photo download karo aur local path return karo.
    Phir caller globals.pdfthumb mein set kar sakta hai.
    """
    try:
        local_path = f"pdfthumb_tg_{uuid.uuid4().hex}.jpg"
        downloaded = await bot.download_media(photo_message.photo, file_name=local_path)
        if downloaded and os.path.exists(downloaded):
            return downloaded
    except Exception as e:
        print(f"[pdfthumb] TG photo download error: {e}")
    return None


# ────────────────────────────────────────────────────────────────────────────
# Handler registration
# ────────────────────────────────────────────────────────────────────────────

def register_pdfthumb_handlers(bot: Client):

    # ── /setpdfthumb ─────────────────────────────────────────────────────────
    @bot.on_message(filters.command(["setpdfthumb", "pdfthumb"]) & filters.private)
    async def set_pdfthumb_cmd(client: Client, m: Message):
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        editable = await m.reply_text(
            "**🖼️ PDF Thumbnail Set — Step 1/1**\n\n"
            "Do any one of these:\n"
            "• **URL bhejo** — `https://graph.org/file/xxx.jpg` (ya koi bhi direct image URL)\n"
            "• **Photo bhejo** — directly Telegram mein image bhejo\n"
            "• **/d bhejo** — thumbnail disable karo\n\n"
            "<blockquote>Send /cancel to abort.</blockquote>"
        )

        try:
            inp: Message = await bot.listen(m.chat.id, timeout=120)
        except asyncio.TimeoutError:
            await editable.edit("⏰ Timeout! Please try /setpdfthumb again.")
            return

        # Cancel check
        if inp.text and inp.text.strip().lower() == "/cancel":
            await editable.edit("❌ Cancelled.")
            await inp.delete(True)
            return

        # ── Case 1: /d disable ──────────────────────────────────────────────
        if inp.text and inp.text.strip().lower() == "/d":
            globals.pdfthumb = "/d"
            delete_pdfthumb_for_user(m.chat.id)
            await editable.edit(
                "✅ **PDF Thumbnail disabled!**\n"
                "Ab PDF files bina thumbnail ke upload hongi."
            )
            await inp.delete(True)
            return

        # ── Case 2: Photo directly sent ─────────────────────────────────────
        if inp.photo:
            await editable.edit("⏳ Photo save ho raha hai...")
            # Store Telegram file_id — download at upload time
            file_id = inp.photo.file_id
            globals.pdfthumb = file_id
            save_pdfthumb_for_user(m.chat.id, file_id)
            await editable.edit(
                "✅ **PDF Thumbnail set from photo!**\n"
                "<blockquote>Ye thumbnail ab sabhi PDF uploads par lagegi.\n"
                "Bot restart ke baad bhi saved rahegi.</blockquote>"
            )
            await inp.delete(True)
            return

        # ── Case 3: URL ─────────────────────────────────────────────────────
        if inp.text:
            url = inp.text.strip()
            if url.startswith("http://") or url.startswith("https://"):
                # Quick validation — check URL reachable
                await editable.edit("⏳ URL verify ho raha hai...")
                try:
                    test = requests.head(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
                    if test.status_code in [200, 301, 302]:
                        globals.pdfthumb = url
                        save_pdfthumb_for_user(m.chat.id, url)
                        await editable.edit(
                            f"✅ **PDF Thumbnail URL set!**\n"
                            f"<blockquote>`{url[:80]}...`\n"
                            f"Ye thumbnail ab sabhi PDF uploads par lagegi.\n"
                            f"Bot restart ke baad bhi saved rahegi.</blockquote>"
                        )
                    else:
                        await editable.edit(
                            f"⚠️ URL respond nahi kar rahi (HTTP {test.status_code}).\n"
                            f"Phir bhi save kar raha hoon...\n"
                        )
                        globals.pdfthumb = url
                        save_pdfthumb_for_user(m.chat.id, url)
                        await editable.edit(
                            f"✅ **PDF Thumbnail URL saved!** (unverified)\n"
                            f"<blockquote>`{url[:80]}`</blockquote>"
                        )
                except Exception as e:
                    # Network error but still save
                    globals.pdfthumb = url
                    save_pdfthumb_for_user(m.chat.id, url)
                    await editable.edit(
                        f"✅ **PDF Thumbnail URL saved!** (could not verify)\n"
                        f"<blockquote>`{url[:80]}`</blockquote>"
                    )
                await inp.delete(True)
                return
            else:
                await editable.edit(
                    "❌ Invalid input!\n"
                    "URL chahiye (http/https se start ho) ya directly photo bhejo.\n"
                    "Try /setpdfthumb again."
                )
                await inp.delete(True)
                return

        await editable.edit("❌ Kuch samajh nahi aaya. Try /setpdfthumb again.")
        await inp.delete(True)

    # ── /viewpdfthumb ─────────────────────────────────────────────────────────
    @bot.on_message(filters.command(["viewpdfthumb", "vpdfthumb"]) & filters.private)
    async def view_pdfthumb_cmd(client: Client, m: Message):
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        saved = get_pdfthumb_for_user(m.chat.id)
        current = globals.pdfthumb

        if saved == "/d" or not saved:
            await m.reply_text(
                "📭 **PDF Thumbnail set nahi hai.**\n\n"
                "Use /setpdfthumb to set one."
            )
            return

        # Try to show the thumbnail
        try:
            if saved.startswith("http://") or saved.startswith("https://"):
                await m.reply_photo(
                    photo=saved,
                    caption=(
                        f"🖼️ **Your PDF Thumbnail**\n\n"
                        f"<blockquote>URL: `{saved[:80]}`\n"
                        f"Type: URL (graph.org / direct)\n"
                        f"Status: ✅ Active</blockquote>"
                    )
                )
            else:
                # Telegram file_id
                await m.reply_photo(
                    photo=saved,
                    caption=(
                        f"🖼️ **Your PDF Thumbnail**\n\n"
                        f"<blockquote>Type: Direct Photo (Telegram)\n"
                        f"Status: ✅ Active</blockquote>"
                    )
                )
        except Exception as e:
            await m.reply_text(
                f"🖼️ PDF Thumbnail set hai:\n<blockquote>`{saved[:100]}`</blockquote>\n\n"
                f"⚠️ Preview load nahi hua: {str(e)[:100]}"
            )

    # ── /delpdfthumb ──────────────────────────────────────────────────────────
    @bot.on_message(filters.command(["delpdfthumb", "removepdfthumb"]) & filters.private)
    async def del_pdfthumb_cmd(client: Client, m: Message):
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        saved = get_pdfthumb_for_user(m.chat.id)
        if saved == "/d" or not saved:
            await m.reply_text("📭 **Koi thumbnail set nahi hai already.**")
            return

        globals.pdfthumb = "/d"
        delete_pdfthumb_for_user(m.chat.id)
        await m.reply_text(
            "❌ **PDF Thumbnail deleted!**\n\n"
            "Ab PDF files bina thumbnail ke upload hongi.\n"
            "Use /setpdfthumb to set a new one."
        )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
