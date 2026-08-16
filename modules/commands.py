import os
import re
import sys
import json
import time
from vars import CREDIT
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

# ═══════════════════════════════════════════════════════════════════════════════
# 📜 AESTHETIC COMMANDS MENU & HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def register_commands_handlers(bot):
    
    # ── MAIN COMMANDS MENU ──────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("cmd_command"))
    async def cmd(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        
        caption = (
            f"╭─━━━━━━ 💜 ━━━━━━─╮\n"
            f"   📜 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 𝐌𝐄𝐍𝐔 📜\n"
            f"╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            f"✧ Welcome, [{first_name}](tg://user?id={user_id})!\n"
            f"✧ Select your access level below to\n"
            f"  view available bot commands.\n\n"
            f"👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚻 𝐔𝐬𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="user_command"), 
             InlineKeyboardButton("👑 𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="owner_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐌𝐚𝐢𝐧 𝐌𝐞𝐧𝐮", callback_data="back_to_main_menu")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/8c148221d261c06e2102b-7164eb21e504cbefe3.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── USER COMMANDS ───────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("user_command"))
    async def help_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="cmd_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🚻 𝐔𝐒𝐄𝐑 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 🚻\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ **Main Features:**\n"
            "  ├ `/start` – 🫩 Check Bot Status\n"
            "  ├ `/stop` – 🌼 Cancel Running Task\n"
            "  ├ `/love` – 💕 TXT Downloader (Premium)\n"
            "  ├ `/y2t` – 🎥 YT Playlist → `.txt`\n"
            "  ├ `/ytm` – 🎶 YT Video → `.mp3`\n"
            "  ├ `/t2t` – 📝 Message → `.txt`\n"
            "  ├ `/t2h` – 🌐 `.txt` → `.html`\n"
            "  └ `/pdfrename` – 📄 Rename PDF File\n\n"
            "✧ **Video Tools:**\n"
            "  ├ `/renamevideo` – 🎥 Rename Video\n"
            "  ├ `/setvideocover` – 🎞️ Set Global Cover\n"
            "  ├ `/changecover` – 🔄 Change Cover\n"
            "  ├ `/viewvideocover` – 👁️ View Cover\n"
            "  └ `/delvideocover` – ✖️ Delete Cover\n\n"
            "✧ **Tools & Settings:**\n"
            "  ├ `/cookies` – 🍪 Update YT Cookies\n"
            "  ├ `/id` – 🆔 Get Chat/User ID\n"
            "  ├ `/info` – ℹ️ User Details\n"
            "  └ `/logs` – 🖨️ View Bot Activity\n\n"
            "💡 **Pro Tip:**\n"
            "  ✧ Send any direct link or `.txt` file\n"
            "    for instant auto-extraction!\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/3f0529e0a232d7a076a60-998260a13c34d2b7ea.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── OWNER COMMANDS ──────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("owner_command"))
    async def owner_help_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="cmd_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   👑 𝐎𝐖𝐍𝐄𝐑 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 👑\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ **User Management:**\n"
            "  ├ `/addauth` <id> – ➕ Add Auth User\n"
            "  ├ `/rmauth` <id> – ➖ Remove Auth User\n"
            "  └ `/users` – 📊 View Total User List\n\n"
            "✧ **Broadcasting:**\n"
            "  ├ `/broadcast` – 📢 Send to All Users\n"
            "  └ `/broadusers` – 👁️ View Broadcast Stats\n\n"
            "✧ **System Control:**\n"
            "  ├ `/reset` – 🔄 Reset/Restart Bot\n"
            "  └ `/changeapi` – ⚡ Update PW API\n\n"
            "⚠️ **Restricted Access:**\n"
            "  ✧ These commands are strictly for the\n"
            "    bot administrator (@Blaster_fazxe).\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/28eaaf6ec37903d4c0841-93d28f7433c8e62dc2.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )