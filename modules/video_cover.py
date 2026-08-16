"""
video_cover.py — Video Cover (Thumbnail) System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• /setvideocover  — Global video cover set karo (direct Telegram photo only, URL not supported)
• /viewvideocover — Current video cover dekho
• /delvideocover  — Video cover delete karo

• /MS send karne par global settings wala cover use hoga
• Agar global cover set nahi hai to user se image maango
• Bot restart ke baad bhi saved rehta hai (JSON file mein)
• Sirf AUTH_USERS use kar sakte hain
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import json
import uuid
import asyncio

import globals
from vars import AUTH_USERS, CREDIT
from pyrogram import Client, filters
from pyrogram.types import Message

# ── Persistent store file ────────────────────────────────────────────────────
_VCOVER_STORE = "videocover_store.json"

# ────────────────────────────────────────────────────────────────────────────
# Storage helpers
# ────────────────────────────────────────────────────────────────────────────

def _load_vcover_store() -> dict:
    if os.path.exists(_VCOVER_STORE):
        try:
            with open(_VCOVER_STORE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_vcover_store(data: dict):
    try:
        with open(_VCOVER_STORE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[video_cover] Save error: {e}")


def save_videocover_for_user(user_id: int, cover_value: str):
    data = _load_vcover_store()
    data[str(user_id)] = cover_value
    _save_vcover_store(data)
    # Also update global
    globals.videocover = cover_value


def get_videocover_for_user(user_id: int) -> str:
    data = _load_vcover_store()
    return data.get(str(user_id), "/d")


def delete_videocover_for_user(user_id: int):
    data = _load_vcover_store()
    data.pop(str(user_id), None)
    _save_vcover_store(data)
    globals.videocover = "/d"


def load_global_videocover_on_start():
    """Bot start par globals.videocover load karo from store."""
    data = _load_vcover_store()
    if data:
        last_val = list(data.values())[-1]
        if last_val and last_val != "/d":
            globals.videocover = last_val
            print(f"[video_cover] Loaded videocover from store: {last_val[:60]}")


# ────────────────────────────────────────────────────────────────────────────
# Handler registration
# ────────────────────────────────────────────────────────────────────────────

def register_video_cover_handlers(bot: Client):

    # ── /setvideocover ────────────────────────────────────────────────────────
    @bot.on_message(filters.command(["setvideocover", "videocover"]) & filters.private)
    async def set_videocover_cmd(client: Client, m: Message):
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        editable = await m.reply_text(
            "**🎥 Video Cover Set — Step 1/1**\n\n"
            "📸 **Direct Telegram se photo bhejo** as Video Cover.\n\n"
            "<blockquote>⚠️ Note: Sirf Telegram photo supported hai.\n"
            "URL supported nahi hai.\n\n"
            "Send /d to disable cover.\n"
            "Send /cancel to abort.</blockquote>"
        )

        try:
            inp: Message = await bot.listen(m.chat.id, timeout=120)
        except asyncio.TimeoutError:
            await editable.edit("⏰ Timeout! Please try /setvideocover again.")
            return

        # Cancel check
        if inp.text and inp.text.strip().lower() == "/cancel":
            await editable.edit("❌ Cancelled.")
            await inp.delete(True)
            return

        # Disable
        if inp.text and inp.text.strip().lower() == "/d":
            globals.videocover = "/d"
            delete_videocover_for_user(m.chat.id)
            await editable.edit(
                "✅ **Video Cover disabled!**\n"
                "Ab videos bina custom cover ke upload honge."
            )
            await inp.delete(True)
            return

        # Photo sent
        if inp.photo:
            file_id = inp.photo.file_id
            globals.videocover = file_id
            save_videocover_for_user(m.chat.id, file_id)
            await editable.edit(
                "✅ **Video Cover set successfully!**\n"
                "<blockquote>Ye cover ab /setvideocover command aur video rename mein use hoga.\n"
                "Bot restart ke baad bhi saved rahega.</blockquote>"
            )
            await inp.delete(True)
            return

        # Invalid
        await editable.edit(
            "❌ Invalid input!\n"
            "Sirf Telegram photo bhejein (URL supported nahi).\n"
            "Try /setvideocover again."
        )
        await inp.delete(True)

    # ── /viewvideocover ───────────────────────────────────────────────────────
    @bot.on_message(filters.command(["viewvideocover", "vvideocover"]) & filters.private)
    async def view_videocover_cmd(client: Client, m: Message):
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        saved = get_videocover_for_user(m.chat.id)
        if saved == "/d" or not saved:
            await m.reply_text(
                "📭 **Video Cover set nahi hai.**\n\n"
                "Use /setvideocover to set one."
            )
            return

        try:
            await m.reply_photo(
                photo=saved,
                caption=(
                    "🎥 **Your Video Cover**\n\n"
                    "<blockquote>Type: Direct Photo (Telegram)\n"
                    "Status: ✅ Active</blockquote>"
                )
            )
        except Exception as e:
            await m.reply_text(
                f"🎥 Video Cover set hai.\n\n"
                f"⚠️ Preview load nahi hua: {str(e)[:100]}"
            )

    # ── /delvideocover ────────────────────────────────────────────────────────
    @bot.on_message(filters.command(["delvideocover", "removevideocover"]) & filters.private)
    async def del_videocover_cmd(client: Client, m: Message):
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        saved = get_videocover_for_user(m.chat.id)
        if saved == "/d" or not saved:
            await m.reply_text("📭 **Koi video cover set nahi hai already.**")
            return

        globals.videocover = "/d"
        delete_videocover_for_user(m.chat.id)
        await m.reply_text(
            "❌ **Video Cover deleted!**\n\n"
            "Ab videos bina custom cover ke upload honge.\n"
            "Use /setvideocover to set a new one."
        )

    # ── /changecover ──────────────────────────────────────────────────────────
    @bot.on_message(filters.command("changecover") & filters.private)
    async def change_cover_cmd(client: Client, m: Message):
        """
        /changecover — Video ka cover change karo:
        1. Video bhejo (original caption preserve hoga)
        2. New cover photo bhejo ya /MS for global cover
        Then same video with new cover + exact same caption resend
        """
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>"
            )
            return

        # ── Step 1: Ask for video ─────────────────────────────────────────────
        editable = await m.reply_text(
            "**🎥 Change Video Cover — Step 1/2**\n\n"
            "Send the video whose cover you want to change.\n"
            "<blockquote>The original caption will be preserved exactly.\n"
            "Send /cancel to abort.</blockquote>"
        )

        try:
            video_msg: Message = await bot.listen(m.chat.id, timeout=180)
        except asyncio.TimeoutError:
            await editable.edit("⏰ Timeout! Please try /changecover again.")
            return

        if video_msg.text and video_msg.text.strip().lower() == "/cancel":
            await editable.edit("❌ Cancelled.")
            await video_msg.delete(True)
            return

        # Accept video or document
        if not (video_msg.video or video_msg.document):
            await editable.edit("❌ Please send a valid video file. Use /changecover again.")
            await video_msg.delete(True)
            return

        # Save original caption exactly as-is
        original_caption = video_msg.caption or ""

        # Get video filename
        if video_msg.video:
            original_name = video_msg.video.file_name or "video.mp4"
        else:
            original_name = video_msg.document.file_name or "video.mp4"

        # Delete user video message
        await video_msg.delete(True)

        # ── Step 2: Ask for new cover ─────────────────────────────────────────
        current_cover = globals.videocover
        cover_hint = ""
        if current_cover and current_cover != "/d":
            cover_hint = "\n• Send **/MS** to use your Global Cover from settings"
        else:
            cover_hint = "\n• Send **/MS** to skip cover (no thumbnail)\n⚠️ Set global cover via /setvideocover to use it"

        await editable.edit(
            f"**🎥 Step 2/2**\n\n"
            f"Video received: `{original_name}`\n\n"
            f"📸 **Send new cover photo** for this video.{cover_hint}\n"
            f"<blockquote>Send /cancel to abort.</blockquote>"
        )

        try:
            cover_msg: Message = await bot.listen(m.chat.id, timeout=120)
        except asyncio.TimeoutError:
            await editable.edit("⏰ Timeout! Please try /changecover again.")
            return

        if cover_msg.text and cover_msg.text.strip().lower() == "/cancel":
            await editable.edit("❌ Cancelled.")
            await cover_msg.delete(True)
            return

        # Determine cover to use
        cover_file_id = None
        if cover_msg.text and cover_msg.text.strip().upper() == "/MS":
            # Use global cover if set
            if current_cover and current_cover != "/d":
                cover_file_id = current_cover
            else:
                cover_file_id = None
            await cover_msg.delete(True)
        elif cover_msg.photo:
            cover_file_id = cover_msg.photo.file_id
            await cover_msg.delete(True)
        else:
            # Unrecognized — skip cover
            cover_file_id = None
            await cover_msg.delete(True)

        await editable.edit("⏳ Downloading video... Please wait.")

        # ── Download video ────────────────────────────────────────────────────
        os.makedirs("downloads", exist_ok=True)
        safe_dl_name = f"chcover_{uuid.uuid4().hex}"

        ext = "mp4"
        if "." in original_name:
            ext = original_name.rsplit(".", 1)[-1].lower()
            if ext not in ["mp4", "mkv", "avi", "mov", "webm", "flv", "wmv", "3gp"]:
                ext = "mp4"

        dl_filename = f"{safe_dl_name}.{ext}"

        try:
            download_path = await bot.download_media(
                video_msg,
                file_name=f"downloads/{dl_filename}"
            )
        except Exception as e:
            await editable.edit(f"❌ Download failed:\n<blockquote>{str(e)[:300]}</blockquote>")
            return

        await editable.edit("📤 Uploading with new cover...")

        # ── Resolve thumbnail ─────────────────────────────────────────────────
        thumbnail = None
        local_cover = None
        local_frame = None

        # Extract frame from video as fallback
        safe_frame = f"ccthumb_{uuid.uuid4().hex}.jpg"
        try:
            import asyncio as _aio
            proc_th = await _aio.create_subprocess_shell(
                f'ffmpeg -y -i "{download_path}" -ss 00:00:10 -vframes 1 -update 1 "{safe_frame}"',
                stdout=_aio.subprocess.PIPE,
                stderr=_aio.subprocess.PIPE
            )
            await _aio.wait_for(proc_th.communicate(), timeout=25)
            if os.path.exists(safe_frame) and os.path.getsize(safe_frame) > 0:
                local_frame = safe_frame
        except Exception:
            pass

        if cover_file_id:
            local_cover = f"cccover_{uuid.uuid4().hex}.jpg"
            try:
                downloaded_cover = await bot.download_media(cover_file_id, file_name=local_cover)
                if downloaded_cover and os.path.exists(downloaded_cover):
                    thumbnail = downloaded_cover
                    local_cover = downloaded_cover
                else:
                    thumbnail = local_frame
            except Exception as e:
                print(f"[changecover] Cover download error: {e}")
                thumbnail = local_frame
        else:
            thumbnail = local_frame

        # ── Get duration ──────────────────────────────────────────────────────
        dur = 0
        try:
            import subprocess
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", download_path],
                capture_output=True, text=True, timeout=15
            )
            dur = int(float(result.stdout.strip()))
        except Exception:
            dur = 0

        # ── Upload with original caption + new cover ──────────────────────────
        try:
            try:
                await bot.send_video(
                    m.chat.id,
                    video=download_path,
                    caption=original_caption if original_caption else None,
                    file_name=original_name,
                    supports_streaming=True,
                    thumb=thumbnail,
                    duration=dur
                )
            except Exception:
                await bot.send_video(
                    m.chat.id,
                    video=download_path,
                    caption=original_caption if original_caption else None,
                    file_name=original_name,
                    supports_streaming=True,
                    duration=dur
                )

            await editable.edit(
                "✅ **Done!**\n"
                f"Video resent with new cover.\n"
                f"<blockquote>Original caption preserved exactly.</blockquote>"
            )
        except Exception as e:
            await editable.edit(f"❌ Upload failed:\n<blockquote>{str(e)[:300]}</blockquote>")
        finally:
            if os.path.exists(download_path):
                os.remove(download_path)
            if local_cover and local_cover != local_frame and os.path.exists(local_cover):
                os.remove(local_cover)
            if local_frame and os.path.exists(local_frame):
                os.remove(local_frame)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
