import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from vars import OWNER, CREDIT
import user_store

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

def register_broadcast_handlers(bot):

    # ── Register every user who messages the bot (private) ──────────────────
    @bot.on_message(filters.private, group=-1)
    async def auto_register_user(client: Client, message: Message):
        try:
            if message.from_user:
                user_store.register_user(message.from_user.id)
        except Exception:
            pass

    # ── Register every group the bot is active in ────────────────────────────
    @bot.on_message(filters.group, group=-1)
    async def auto_register_group(client: Client, message: Message):
        try:
            user_store.register_group(message.chat.id)
        except Exception:
            pass

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

    @bot.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_handler(client: Client, message: Message):
        if message.chat.id != OWNER:
            return

        if not message.reply_to_message:
            return await message.reply_text(
                "📢 **Broadcast Mode**\n\n"
                "Please Boss reply with content to broadcast.\n\n"
                "<blockquote>Broadcast goes to:\n"
                "• All users who ever started the bot (persisted across restarts)\n"
                "• All groups where bot is active</blockquote>"
            )

        content = message.reply_to_message
        all_targets = user_store.get_all_targets()

        if not all_targets:
            return await message.reply_text("❌ No users/groups in database yet.")

        sent = 0
        failed = 0
        status_msg = await message.reply_text(
            f"📤 Broadcasting to `{len(all_targets)}` targets (users + groups)..."
        )

        for target_id in all_targets:
            try:
                await content.copy(target_id)
                sent += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.08)

        await status_msg.edit_text(
            f"✅ **Broadcast Complete!**\n\n"
            f"📨 Sent: `{sent}`\n"
            f"❌ Failed: `{failed}`\n"
            f"👥 Total Targets: `{len(all_targets)}`\n\n"
            f"<blockquote>Users: {len(user_store.get_all_users())}\n"
            f"Groups: {len(user_store.get_all_groups())}</blockquote>"
        )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

    @bot.on_message(filters.command("broadusers") & filters.private)
    async def broadusers_handler(client: Client, message: Message):
        if message.chat.id != OWNER:
            return

        all_users = user_store.get_all_users()
        all_groups = user_store.get_all_groups()

        if not all_users and not all_groups:
            return await message.reply_text("**No users or groups found.**")

        total_users = len(all_users)
        total_groups = len(all_groups)
        total = total_users + total_groups

        # Build users text
        user_lines = []
        for user_id in all_users:
            try:
                user = await client.get_users(int(user_id))
                fname = user.first_name if user.first_name else " "
                uname = f"@{user.username}" if user.username else "no username"
                user_lines.append(
                    f"👤 [{fname}](tg://openmessage?user_id={user_id}) | `{user_id}` | {uname}"
                )
            except Exception:
                user_lines.append(f"👤 `{user_id}` | (could not fetch info)")

        # Build groups text
        group_lines = []
        for chat_id in all_groups:
            try:
                chat = await client.get_chat(int(chat_id))
                gname = chat.title if chat.title else "Unnamed"
                group_lines.append(f"👥 {gname} | `{chat_id}`")
            except Exception:
                group_lines.append(f"👥 `{chat_id}` | (could not fetch info)")

        header = (
            f"📊 **Broadcast Targets — Total: {total}**\n"
            f"<blockquote>👤 Users: {total_users}  |  👥 Groups: {total_groups}</blockquote>\n\n"
        )

        async def send_chunks(lines: list, section_header: str):
            chunk = section_header
            for line in lines:
                addition = line + "\n"
                if len(chunk) + len(addition) > 4000:
                    await message.reply_text(chunk, disable_web_page_preview=True)
                    chunk = ""
                chunk += addition
            if chunk.strip():
                await message.reply_text(chunk, disable_web_page_preview=True)

        await message.reply_text(header, disable_web_page_preview=True)

        if user_lines:
            await send_chunks(user_lines, f"**👤 Users ({total_users}):**\n")
        if group_lines:
            await send_chunks(group_lines, f"**👥 Groups ({total_groups}):**\n")

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
