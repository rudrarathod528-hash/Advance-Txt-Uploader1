import os
import re
import sys
import json
import time
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

# ═══════════════════════════════════════════════════════════════════════════════
# ✨ AESTHETIC FEATURES MENU & HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def register_feature_handlers(bot):
    
    # ── MAIN FEATURES MENU ──────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("feat_command"))
    async def feature_button(client, callback_query):
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   ✨ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐅𝐄𝐀𝐓𝐔𝐑𝐄𝐒 ✨\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Explore the powerful tools and\n"
            "  customizations available in this bot.\n\n"
            "👑 𝐎𝐰𝐧𝐞𝐫: @Blaster_fazxe"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📌 𝐀𝐮𝐭𝐨 𝐏𝐢𝐧", callback_data="pin_command"), 
             InlineKeyboardButton("💧 𝐖𝐚𝐭𝐞𝐫𝐦𝐚𝐫𝐤", callback_data="watermark_command")],
            [InlineKeyboardButton("🔄 𝐑𝐞𝐬𝐞𝐭", callback_data="reset_command"), 
             InlineKeyboardButton("🖨️ 𝐋𝐨𝐠𝐬", callback_data="logs_command")],
            [InlineKeyboardButton("🖋️ 𝐅𝐢𝐥𝐞 𝐍𝐚𝐦𝐞", callback_data="custom_command"), 
             InlineKeyboardButton("🏷️ 𝐓𝐢𝐭𝐥𝐞", callback_data="titlle_command")],
            [InlineKeyboardButton("🎥 𝐘𝐨𝐮𝐓𝐮𝐛𝐞", callback_data="yt_command"), 
             InlineKeyboardButton("🌐 𝐇𝐓𝐌𝐋", callback_data="html_command")],
            [InlineKeyboardButton("📝 𝐓𝐱𝐭 𝐌𝐚𝐤𝐞𝐫", callback_data="txt_maker_command"), 
             InlineKeyboardButton("📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭", callback_data="broadcast_command")],
            [InlineKeyboardButton("📄 𝐏𝐃𝐅 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="pdf_features_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐌𝐚𝐢𝐧 𝐌𝐞𝐧𝐮", callback_data="back_to_main_menu")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/d94225198c49f4837ad6d-956835edec68f686bb.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── AUTO PIN ────────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("pin_command"))
    async def pin_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📌 𝐀𝐔𝐓𝐎 𝐏𝐈𝐍 𝐁𝐀𝐓𝐂𝐇\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Automatically pins the **Batch Name**\n"
            "  in your Channel or Group when the\n"
            "  download starts from the first link.\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/4f489f48098e89b7240b2-0c35f0c5a758db2cb1.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── WATERMARK ───────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("watermark_command"))
    async def watermark_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   💧 𝐂𝐔𝐒𝐓𝐎𝐌 𝐖𝐀𝐓𝐄𝐑𝐌𝐀𝐑𝐊\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Set your own custom text or logo\n"
            "  watermark on all downloaded videos\n"
            "  for added personalization and branding.\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/45f48779e0aa39709d1e8-4c024567d60f6ec5c2.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── RESET ───────────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("reset_command"))
    async def restart_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🔄 𝐑𝐄𝐒𝐄𝐓 𝐁𝐎𝐓\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ If you want to reset or restart your\n"
            "  bot's current state, simply use the\n"
            "  command: `/reset`\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/033121ad32291bcaddd01-d91ae4a1f7ca9378fc.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── LOGS ────────────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("logs_command"))
    async def logs_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🖨️ 𝐁𝐎𝐓 𝐖𝐎𝐑𝐊𝐈𝐍𝐆 𝐋𝐎𝐆𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ View the internal working logs of\n"
            "  the bot to debug or track progress.\n\n"
            "  **Command:** `/logs`\n"
            "  _(Sends logs as a .txt file)_\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/29c4511ee7a4653d22fe1-67906a2a8392895644.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── CUSTOM FILE NAME ────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("custom_command"))
    async def custom_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🖋️ 𝐂𝐔𝐒𝐓𝐎𝐌 𝐅𝐈𝐋𝐄 𝐍𝐀𝐌𝐄\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Add a custom suffix or prefix to your\n"
            "  file names before the extension.\n\n"
            "  **How:** Add the name when the bot\n"
            "  asks during the `.txt` upload process.\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── CUSTOM TITLE ────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("titlle_command"))
    async def titlle_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🏷️ 𝐂𝐔𝐒𝐓𝐎𝐌 𝐓𝐈𝐓𝐋𝐄\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Add and customize titles at the\n"
            "  starting of your video names.\n\n"
            "  📍 **NOTE:** The Title must be\n"
            "  enclosed within `(Title)`.\n"
            "  _Best for Appx's .txt files._\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b67a919df868cbb82b3cb-131aaff80361c5af6e.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── BROADCAST ───────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("broadcast_command"))
    async def broadcast_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓𝐈𝐍𝐆\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Send messages to all registered users.\n\n"
            "  **Commands:**\n"
            "  ├ `/broadcast` - 📢 Send to all\n"
            "  └ `/broadusers` - 👁️ View user list\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/8c148221d261c06e2102b-7164eb21e504cbefe3.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── TXT MAKER ───────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("txt_maker_command"))
    async def editor_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📝 𝐓𝐗𝐓 𝐌𝐀𝐊𝐄𝐑\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Convert raw text messages into\n"
            "  formatted `.txt` files for batch\n"
            "  downloading.\n\n"
            "  **Command:** `/t2t`\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/3f0529e0a232d7a076a60-998260a13c34d2b7ea.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── YOUTUBE ─────────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("yt_command"))
    async def y2t_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🎥 𝐘𝐎𝐔𝐓𝐔𝐁𝐄 𝐓𝐎𝐎𝐋𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ **Commands:**\n"
            "  ├ `/y2t` - 🔪 Playlist → `.txt`\n"
            "  └ `/ytm` - 🎶 Video → `.mp3`\n\n"
            "  📍 **How to use `.mp3` downloader:**\n"
            "  1. Send `/ytm`\n"
            "  2. Send single or multiple YT links:\n"
            "  `https://youtube.com/watch?v=xxx`\n"
            "  `https://youtube.com/watch?v=yyy`\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/28eaaf6ec37903d4c0841-93d28f7433c8e62dc2.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── HTML ────────────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("html_command"))
    async def html_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🌐 𝐇𝐓𝐌𝐋 𝐂𝐎𝐍𝐕𝐄𝐑𝐓𝐄𝐑\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Convert your `.txt` batch files into\n"
            "  beautiful, viewable HTML web pages.\n\n"
            "  **Command:** `/t2h`\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/d94225198c49f4837ad6d-956835edec68f686bb.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── PDF FEATURES MENU ───────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("^pdf_features_command$"))
    async def pdf_features_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 𝐏𝐃𝐅 𝐑𝐞𝐧𝐚𝐦𝐞", callback_data="pdfrename_command")],
            [InlineKeyboardButton("🖼️ 𝐏𝐃𝐅 𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥", callback_data="pdfthumb_command")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="feat_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📄 𝐏𝐃𝐅 𝐅𝐄𝐀𝐓𝐔𝐑𝐄𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ **Available Tools:**\n"
            "  ├ 📄 **PDF Rename** — Rename & Re-upload\n"
            "  └ 🖼️ **PDF Thumbnail** — ⚠️ Unavailable\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── PDF RENAME ──────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("^pdfrename_command$"))
    async def pdfrename_feat_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💥 𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧", url="https://t.me/Cinderella_recaptionBot"), 
             InlineKeyboardButton("💥 𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐒𝐭𝐫𝐢𝐧𝐠", url="https://t.me/Cinderella_StringBot")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐏𝐃𝐅 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="pdf_features_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📄 𝐏𝐃𝐅 𝐑𝐄𝐍𝐀𝐌𝐄\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ **Command:** `/pdfrename`\n\n"
            "  📍 **How to use:**\n"
            "  1. Send `/pdfrename`\n"
            "  2. Upload your PDF file\n"
            "  3. Send the new name _(without .pdf)_\n"
            "  4. Bot renames and re-uploads it!\n\n"
            "  ✅ _PDF Thumbnail is applied automatically._\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── PDF THUMBNAIL ───────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("^pdfthumb_command$"))
    async def pdfthumb_feat_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💥 𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧", url="https://t.me/Blaster_fazxe"), 
             InlineKeyboardButton("💥 𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐒𝐭𝐫𝐢𝐧𝐠", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐏𝐃𝐅 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬", callback_data="pdf_features_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🖼️ 𝐏𝐃𝐅 𝐓𝐇𝐔𝐌𝐁𝐍𝐀𝐈𝐋\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "⚠️ **Temporary Unavailable**\n"
            "This feature is currently disabled\n"
            "in this version of the bot.\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )