"""
video_rename.py — Video Rename Feature
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• /renamevideo — 4-step video rename:
  1. Bot asks for video file
  2. Bot shows current video name, asks for new name
  3. Bot asks for batch name (/unknown supported)
  4. If global videocover not set: asks for cover image or /MS to skip
     If global videocover IS set: directly uses it
  Then re-uploads with cc1 caption + video cover
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import uuid
import time
import asyncio
import requests

import globals
from vars import AUTH_USERS, CREDIT
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

def register_video_rename_handlers(bot: Client):

    @bot.on_message(filters.command("renamevideo") & filters.private)
    async def video_rename_cmd(client: Client, m: Message):
        """
        /renamevideo — 4-step video rename:
        1. Ask for video file
        2. Show current name, ask for new name
        3. Ask for batch name
        4. Ask for cover image (or /MS if global cover set, or ask anyway if not set)
        Then resend renamed video with cc1 caption + cover to user
        """
        if m.chat.id not in AUTH_USERS:
            await m.reply_text(
                f"<blockquote>__**Oopss! You are not a Premium member**__\n"
                f"__**Please Upgrade Your Plan**__\n"
                f"__**Your User id**__ - `{m.chat.id}`</blockquote>\n"
            )
            return

        # ── Step 1: Ask for video file ────────────────────────────────────────
        editable = await m.reply_text(
            "**🎥 Video Rename — Step 1/4**\n\n"
            "Send the video file you want to rename.\n"
            "<blockquote>Send /cancel to abort.</blockquote>"
        )

        try:
            video_msg: Message = await bot.listen(m.chat.id, timeout=180)
        except asyncio.TimeoutError:
            await editable.edit("⏰ Timeout! Please try /renamevideo again.")
            return

        if video_msg.text and video_msg.text.strip().lower() == "/cancel":
            await editable.edit("❌ Cancelled.")
            await video_msg.delete(True)
            return

        # Delete user's video message
        await video_msg.delete(True)

        # Accept video or document (mkv, mp4, etc.)
        if not (video_msg.video or video_msg.document):
            await editable.edit("❌ Please send a valid video file. Use /renamevideo again.")
            return

        # Get original video title
        if video_msg.video:
            original_name = video_msg.video.file_name or "video.mp4"
        else:
            original_name = video_msg.document.file_name or "video.mp4"

        # ── Step 2: Show current name, ask for new name ───────────────────────
        await editable.edit(
            f"**🎥 Step 2/4**\n\n"
            f"Video received: `{original_name}`\n\n"
            f"Send the **new video name** (without extension).\n"
            f"<blockquote>This will be used as the video **title**.\n"
            f"Send /cancel to abort.</blockquote>"
        )

        try:
            name_msg: Message = await bot.listen(m.chat.id, timeout=120)
        except asyncio.TimeoutError:
            await editable.edit("⏰ Timeout! Please try /renamevideo again.")
            return

        if name_msg.text and name_msg.text.strip().lower() == "/cancel":
            await editable.edit("❌ Cancelled.")
            await name_msg.delete(True)
            return

        new_name_raw = name_msg.text.strip() if name_msg.text else ""
        await name_msg.delete(True)

        # Sanitize name
        new_name = "".join(c for c in new_name_raw if c not in r'\/:*?"<>|')
        if not new_name:
            await editable.edit("❌ Invalid video name. Use /renamevideo again.")
            return

        # Apply endfilename suffix from settings if set
        endfilename = globals.endfilename
        if endfilename and endfilename != "/d":
            new_name_final = f"{new_name} {endfilename}"
        else:
            new_name_final = new_name

        # ── Step 3: Ask for batch name ────────────────────────────────────────
        await editable.edit(
            f"**🎥 Step 3/4**\n\n"
            f"New Name: **{new_name_final}**\n\n"
            f"Enter **Batch Name** or send **/unknown** if you don't know.\n"
            f"<blockquote>Same /unknown system as direct link download.</blockquote>"
        )

        try:
            batch_msg: Message = await bot.listen(m.chat.id, timeout=120)
            b_text = batch_msg.text.strip() if batch_msg.text else "/unknown"
            b_name = "💥Contact: @CinderellaContactBot" if b_text.lower() in ["/unknown", "/unknow"] else b_text
            await batch_msg.delete(True)
        except asyncio.TimeoutError:
            b_name = "💥Contact: @CinderellaContactBot"

        # ── Step 4: Ask for cover image (or use global cover) ─────────────────
        current_cover = globals.videocover

        cover_file_id = None

        if current_cover and current_cover != "/d":
            # Global cover already set — skip asking, use it directly
            cover_file_id = current_cover
            await editable.edit(
                f"**wait wait🫷🏻🫸🏻**\n\n"
                f"✅ Using your **Global Video Cover** from settings.\n\n"
                f"⏳ Downloading video... Please wait."
            )
        else:
            # Global cover not set — ask user for image or /MS
            await editable.edit(
                f"**🎥 Step 4/4**\n\n"
                f"📸 Send a **photo** as video cover.\n\n"
                f"<blockquote>• Send a Telegram photo directly\n"
                f"• Send **/MS** to skip (no cover)\n"
                f"• Send **/cancel** to abort\n\n"
                f"⚠️ First set your global cover via /setvideocover\n"
                f"to avoid this step every time!</blockquote>"
            )

            try:
                cover_msg: Message = await bot.listen(m.chat.id, timeout=120)
            except asyncio.TimeoutError:
                cover_msg = None

            if cover_msg:
                if cover_msg.text and cover_msg.text.strip().lower() == "/cancel":
                    await editable.edit("❌ Cancelled.")
                    await cover_msg.delete(True)
                    return

                if cover_msg.text and cover_msg.text.strip().upper() == "/MS":
                    # Skip cover
                    cover_file_id = None
                    await cover_msg.delete(True)
                elif cover_msg.photo:
                    cover_file_id = cover_msg.photo.file_id
                    await cover_msg.delete(True)
                else:
                    # Unrecognized input — skip cover
                    cover_file_id = None
                    await cover_msg.delete(True)

            await editable.edit("⏳ Downloading video... Please wait.")

        # ── Download video ────────────────────────────────────────────────────
        os.makedirs("downloads", exist_ok=True)
        safe_dl_name = f"vidrn_{uuid.uuid4().hex}"

        # Get extension from original filename
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

        # Rename locally
        new_filename = f"{new_name_final}.{ext}"
        dir_path = os.path.dirname(download_path)
        renamed_path = os.path.join(dir_path, new_filename)
        try:
            os.rename(download_path, renamed_path)
        except Exception as e:
            await editable.edit(f"❌ Rename failed:\n<blockquote>{str(e)[:300]}</blockquote>")
            if os.path.exists(download_path):
                os.remove(download_path)
            return

        await editable.edit(f"📤 Uploading: `{new_filename}`...")

        # ── Build cc1 caption ─────────────────────────────────────────────────
        CR = globals.CR
        cc1 = (
            f"**📹 VID_ID: 001.\n\n"
            f"📝 Title: {new_name_final} .{ext}\n\n"
            f"<pre><code>📚 Batch Name: {b_name}</code></pre>\n\n"
            f"📥 Extracted By♠ : {CR}\n\n"
            f"**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**"
        )

        # ── Resolve cover thumbnail ───────────────────────────────────────────
        thumbnail = None
        local_cover = None
        local_frame = None

        # Try to extract a frame from video as fallback thumb
        safe_frame = f"vthumb_{uuid.uuid4().hex}.jpg"
        try:
            proc_th = await asyncio.create_subprocess_shell(
                f'ffmpeg -y -i "{renamed_path}" -ss 00:00:10 -vframes 1 -update 1 "{safe_frame}"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await asyncio.wait_for(proc_th.communicate(), timeout=25)
            if os.path.exists(safe_frame) and os.path.getsize(safe_frame) > 0:
                local_frame = safe_frame
        except Exception:
            pass

        if cover_file_id:
            # Download the cover from Telegram file_id
            local_cover = f"vcover_{uuid.uuid4().hex}.jpg"
            try:
                downloaded_cover = await bot.download_media(cover_file_id, file_name=local_cover)
                if downloaded_cover and os.path.exists(downloaded_cover):
                    thumbnail = downloaded_cover
                    local_cover = downloaded_cover
                else:
                    thumbnail = local_frame
            except Exception as e:
                print(f"[video_rename] Cover download error: {e}")
                thumbnail = local_frame
        else:
            thumbnail = local_frame

        # ── Upload video ──────────────────────────────────────────────────────
        start_time = time.time()
        try:
            # Get duration via ffprobe
            dur = 0
            try:
                import subprocess
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", renamed_path],
                    capture_output=True, text=True, timeout=15
                )
                dur = int(float(result.stdout.strip()))
            except Exception:
                dur = 0

            try:
                await bot.send_video(
                    m.chat.id,
                    video=renamed_path,
                    caption=cc1,
                    file_name=new_filename,
                    supports_streaming=True,
                    thumb=thumbnail,
                    duration=dur
                )
            except Exception:
                await bot.send_video(
                    m.chat.id,
                    video=renamed_path,
                    caption=cc1,
                    file_name=new_filename,
                    supports_streaming=True,
                    duration=dur
                )

            await editable.edit(
                f"✅ **Done!**\n"
                f"`{original_name}` → **{new_filename}**"
            )
        except Exception as e:
            await editable.edit(f"❌ Upload failed:\n<blockquote>{str(e)[:300]}</blockquote>")
        finally:
            if os.path.exists(renamed_path):
                os.remove(renamed_path)
            if local_cover and local_cover != local_frame and os.path.exists(local_cover):
                os.remove(local_cover)
            if local_frame and os.path.exists(local_frame):
                os.remove(local_frame)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
