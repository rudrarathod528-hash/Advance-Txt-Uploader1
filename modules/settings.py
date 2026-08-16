import globals
from vars import CREDIT
import random
import os
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ AESTHETIC SETTINGS PANEL & HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def register_settings_handlers(bot):
    
    # ── MAIN SETTINGS MENU ──────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("setttings"))
    async def settings_button(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   ⚙️ 𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒 𝐏𝐀𝐍𝐄𝐋 ⚙️\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            f"✧ Welcome, [{first_name}](tg://user?id={user_id})!\n"
            "✧ Customize your bot's behavior,\n"
            "  watermarks, tokens, and more.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 𝐂𝐚𝐩𝐭𝐢𝐨𝐧", callback_data="caption_style_command"), 
             InlineKeyboardButton("🖋️ 𝐅𝐢𝐥𝐞 𝐍𝐚𝐦𝐞", callback_data="file_name_command")],
            [InlineKeyboardButton("🌅 𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥", callback_data="thummbnail_command")],
            [InlineKeyboardButton("✍️ 𝐂𝐫𝐞𝐝𝐢𝐭", callback_data="add_credit_command"), 
             InlineKeyboardButton("🔏 𝐓𝐨𝐤𝐞𝐧𝐬", callback_data="set_token_command")],
            [InlineKeyboardButton("💧 𝐖𝐚𝐭𝐞𝐫𝐦𝐚𝐫𝐤", callback_data="wattermark_command")],
            [InlineKeyboardButton("📽️ 𝐐𝐮𝐚𝐥𝐢𝐭𝐲", callback_data="quality_command"), 
             InlineKeyboardButton("🏷️ 𝐓𝐨𝐩𝐢𝐜", callback_data="topic_command")],
            [InlineKeyboardButton("🔄 𝐑𝐞𝐬𝐞𝐭 𝐀𝐥𝐥", callback_data="resset_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐌𝐚𝐢𝐧 𝐌𝐞𝐧𝐮", callback_data="back_to_main_menu")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/45f48779e0aa39709d1e8-4c024567d60f6ec5c2.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── THUMBNAIL MENU ──────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("thummbnail_command"))
    async def thumbnail_menu(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🌅 𝐓𝐇𝐔𝐌𝐁𝐍𝐀𝐈𝐋 𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Choose which type of thumbnail\n"
            "  or cover photo you want to configure.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="viideo_thumbnail_command"), 
             InlineKeyboardButton("📑 𝐏𝐃𝐅 𝐓𝐡𝐮𝐦𝐛", callback_data="pddf_thumbnail_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b23084c3e9124e14e18ec-d385f8f9c8b1635a2e.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── WATERMARK MENU ──────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("wattermark_command"))
    async def watermark_menu(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   💧 𝐖𝐀𝐓𝐄𝐑𝐌𝐀𝐑𝐊 𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Apply custom watermarks to your\n"
            "  downloaded videos or PDF files.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 𝐕𝐢𝐝𝐞𝐨", callback_data="video_wateermark_command"), 
             InlineKeyboardButton("📑 𝐏𝐃𝐅", callback_data="pdf_wateermark_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/033121ad32291bcaddd01-d91ae4a1f7ca9378fc.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── TOKEN MANAGER MENU ──────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("set_token_command"))
    async def token_menu(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🔏 𝐓𝐎𝐊𝐄𝐍 𝐌𝐀𝐍𝐀𝐆𝐄𝐑\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Set or update your authentication\n"
            "  tokens for premium platforms.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 𝐂𝐥𝐚𝐬𝐬𝐩𝐥𝐮𝐬", callback_data="cp_token_command")],
            [InlineKeyboardButton("🟢 𝐏𝐡𝐲𝐬𝐢𝐜𝐬 𝐖𝐚𝐥𝐥𝐚𝐡", callback_data="pw_token_command"), 
             InlineKeyboardButton("🟢 𝐂𝐚𝐫𝐞𝐞𝐫𝐰𝐢𝐥𝐥", callback_data="cw_token_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/417cc7326cab9036c0152-f6a281db2a6975dfa9.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

    # ── CAPTION STYLE ───────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("caption_style_command"))
    async def handle_caption(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📝 𝐂𝐀𝐏𝐓𝐈𝐎𝐍 𝐒𝐓𝐘𝐋𝐄𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "**Style 1:**\n"
            "`[🎥] 001 | Title [480p]`\n"
            "`Batch: Name | By: Credit`\n\n"
            "**Style 2:**\n"
            "`——— ✦ 001 ✦ ———`\n"
            "`🎞️ Title`\n"
            "`📚 Course | 🌟 Credit`\n\n"
            "**Style 3:**\n"
            "`001. Title [480p]`\n\n"
            "✧ **Send your choice:** `/cc1`, `/cc2`, `/cc3`\n"
            "  _or send a custom caption format._\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/cc1":
                globals.caption = '/cc1'
                await editable.edit(f"✅ **Caption Style 1 Updated!**", reply_markup=keyboard)
            elif input_msg.text.lower() == "/cc2":
                globals.caption = '/cc2'
                await editable.edit(f"✅ **Caption Style 2 Updated!**", reply_markup=keyboard)
            else:
                globals.caption = input_msg.text
                await editable.edit(f"✅ **Custom Caption Updated!**", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Caption Style:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── FILE NAME ───────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("file_name_command"))
    async def handle_filename(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🖋️ 𝐂𝐔𝐒𝐓𝐎𝐌 𝐅𝐈𝐋𝐄 𝐍𝐀𝐌𝐄\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Send the text you want to append\n"
            "  at the end of every file name.\n\n"
            "✧ Send `/d` to disable this feature.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.endfilename = '/d'
                await editable.edit(f"✅ **End File Name Disabled!**", reply_markup=keyboard)
            else:
                globals.endfilename = input_msg.text
                await editable.edit(f"✅ **End File Name** `{globals.endfilename}` **is enabled!**", reply_markup=keyboard)            
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set End File Name:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── VIDEO THUMBNAIL (COVER) MENU ────────────────────────────────────────
    @bot.on_callback_query(filters.regex("viideo_thumbnail_command"))
    async def video_thumbnail(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 𝐒𝐞𝐭 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="set_video_cover_command")],
            [InlineKeyboardButton("👁️ 𝐕𝐢𝐞𝐰 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="view_video_cover_command")],
            [InlineKeyboardButton("❌ 𝐃𝐞𝐥𝐞𝐭𝐞 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="del_video_cover_command")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥", callback_data="thummbnail_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🎥 𝐕𝐈𝐃𝐄𝐎 𝐂𝐎𝐕𝐄𝐑 𝐏𝐇𝐎𝐓𝐎\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Set a global cover photo for your\n"
            "  downloaded videos.\n\n"
            "📍 **Note:** Only direct Telegram photos\n"
            "are supported (no URLs).\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit(caption, reply_markup=keyboard)

    # ── SET VIDEO COVER ─────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("set_video_cover_command"))
    async def set_video_cover_settings(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="viideo_thumbnail_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🖼️ 𝐒𝐄𝐓 𝐕𝐈𝐃𝐄𝐎 𝐂𝐎𝐕𝐄𝐑\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ **Send a photo** directly in this chat\n"
            "  to set it as the Global Video Cover.\n\n"
            "✧ Send `/d` to disable the cover.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text and input_msg.text.strip().lower() == "/d":
                globals.videocover = "/d"
                from video_cover import delete_videocover_for_user
                delete_videocover_for_user(callback_query.from_user.id)
                await editable.edit("✅ **Video Cover Disabled!**", reply_markup=keyboard)
            elif input_msg.photo:
                file_id = input_msg.photo.file_id
                globals.videocover = file_id
                from video_cover import save_videocover_for_user
                save_videocover_for_user(callback_query.from_user.id, file_id)
                await editable.edit("✅ **Video Cover set from photo!**", reply_markup=keyboard)
            else:
                await editable.edit("❌ **Invalid input!** Please send a Telegram photo.", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── VIEW VIDEO COVER ────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("view_video_cover_command"))
    async def view_video_cover_settings(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="viideo_thumbnail_command")]
        ])
        from video_cover import get_videocover_for_user
        saved = get_videocover_for_user(callback_query.from_user.id)
        if saved == "/d" or not saved:
            await callback_query.message.edit("📭 **Video Cover is not set.**\n\nUse /setvideocover to set one.", reply_markup=keyboard)
            return
        try:
            await callback_query.message.reply_photo(
                photo=saved,
                caption="🎥 **Your Current Video Cover**\n<blockquote>Status: ✅ Active</blockquote>"
            )
            await callback_query.message.edit("✅ Cover shown above.", reply_markup=keyboard)
        except Exception as e:
            await callback_query.message.edit(f"🎥 Video Cover is set.\n⚠️ Preview error: {str(e)[:100]}", reply_markup=keyboard)

    # ── DELETE VIDEO COVER ──────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("del_video_cover_command"))
    async def del_video_cover_settings(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐕𝐢𝐝𝐞𝐨 𝐂𝐨𝐯𝐞𝐫", callback_data="viideo_thumbnail_command")]
        ])
        from video_cover import get_videocover_for_user, delete_videocover_for_user
        saved = get_videocover_for_user(callback_query.from_user.id)
        if saved == "/d" or not saved:
            await callback_query.message.edit("📭 **No Video Cover is currently set.**", reply_markup=keyboard)
            return
        globals.videocover = "/d"
        delete_videocover_for_user(callback_query.from_user.id)
        await callback_query.message.edit("❌ **Video Cover deleted!**\n\nUse /setvideocover to set a new one.", reply_markup=keyboard)

    # ── PDF THUMBNAIL (UNAVAILABLE) ─────────────────────────────────────────
    @bot.on_callback_query(filters.regex("pddf_thumbnail_command"))
    async def pdf_thumbnail_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥", callback_data="thummbnail_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📸 𝐏𝐃𝐅 𝐓𝐇𝐔𝐌𝐁𝐍𝐀𝐈𝐋\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "⚠️ **Temporary Unavailable**\n"
            "This feature is currently disabled\n"
            "in this version of the bot.\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit(caption, reply_markup=keyboard)

    # ── ADD CREDIT ──────────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("add_credit_command"))
    async def credit(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   ✍️ 𝐀𝐃𝐃 𝐂𝐑𝐄𝐃𝐈𝐓\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Send your custom Credit Name/Text.\n"
            "✧ Send `/d` to use the default credit.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.CR = f"{CREDIT}"
                await editable.edit(f"✅ **Credit set to default!**", reply_markup=keyboard)
            else:
                globals.CR = input_msg.text
                await editable.edit(f"✅ **Credit set as** `{globals.CR}` **!**", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Credit:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── CLASSPLUS TOKEN ─────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("cp_token_command"))
    async def handle_cp_token(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐓𝐨𝐤𝐞𝐧𝐬", callback_data="set_token_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🟢 𝐂𝐋𝐀𝐒𝐒𝐏𝐋𝐔𝐒 𝐓𝐎𝐊𝐄𝐍\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Send your Classplus X-Access-Token.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            globals.cptoken = input_msg.text
            await editable.edit(f"✅ **Classplus Token set successfully!**\n\n<blockquote expandable>`{globals.cptoken}`</blockquote>", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Classplus Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── PHYSICS WALLAH TOKEN ────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("pw_token_command"))
    async def handle_pw_token(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐓𝐨𝐤𝐞𝐧𝐬", callback_data="set_token_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🟢 𝐏𝐇𝐘𝐒𝐈𝐂𝐒 𝐖𝐀𝐋𝐋𝐀𝐇 𝐓𝐎𝐊𝐄𝐍\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Send your Physics Wallah Token.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            globals.pwtoken = input_msg.text
            await editable.edit(f"✅ **Physics Wallah Token set successfully!**\n\n<blockquote expandable>`{globals.pwtoken}`</blockquote>", reply_markup=keyboard) 
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set PW Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── CAREERWILL TOKEN ────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("cw_token_command"))
    async def handle_cw_token(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐓𝐨𝐤𝐞𝐧𝐬", callback_data="set_token_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🟢 𝐂𝐀𝐑𝐄𝐄𝐑𝐖𝐈𝐋𝐋 𝐓𝐎𝐊𝐄𝐍\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Send your Careerwill Token.\n"
            "✧ Send `/d` to use the default token.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                await editable.edit(f"✅ **Careerwill Token set to default!**", reply_markup=keyboard)
            else:
                globals.cwtoken = input_msg.text
                await editable.edit(f"✅ **Careerwill Token set successfully!**\n\n<blockquote expandable>`{globals.cwtoken}`</blockquote>", reply_markup=keyboard)      
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Careerwill Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── VIDEO WATERMARK (UNAVAILABLE) ───────────────────────────────────────
    @bot.on_callback_query(filters.regex("video_wateermark_command"))
    async def video_watermark(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐖𝐚𝐭𝐞𝐫𝐦𝐚𝐫𝐤", callback_data="wattermark_command")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🎥 𝐕𝐈𝐃𝐄𝐎 𝐖𝐀𝐓𝐄𝐑𝐌𝐀𝐑𝐊\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "⚠️ **Temporary Unavailable**\n"
            "This feature is currently disabled\n"
            "in this version of the bot.\n\n"
            "✧ 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit(caption, reply_markup=keyboard)

    # ── PDF WATERMARK LOCATIONS ─────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("^pdf_wateermark_command$"))
    async def pdf_watermark_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("↗️ 𝐔𝐩𝐩𝐞𝐫 𝐑𝐢𝐠𝐡𝐭", callback_data="pdfwm_upper_right"),
             InlineKeyboardButton("↖️ 𝐔𝐩𝐩𝐞𝐫 𝐋𝐞𝐟𝐭",  callback_data="pdfwm_upper_left")],
            [InlineKeyboardButton("↘️ 𝐃𝐨𝐰𝐧 𝐑𝐢𝐠𝐡𝐭",  callback_data="pdfwm_down_right"),
             InlineKeyboardButton("↙️ 𝐃𝐨𝐰𝐧 𝐋𝐞𝐟𝐭",   callback_data="pdfwm_down_left")],
            [InlineKeyboardButton("⬇️ 𝐃𝐨𝐰𝐧 𝐌𝐢𝐝𝐝𝐥𝐞", callback_data="pdfwm_down_middle")],
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐖𝐚𝐭𝐞𝐫𝐦𝐚𝐫𝐤", callback_data="wattermark_command")]
        ])

        def _wm_status(wm_dict):
            t = wm_dict.get("title", "/d")
            u = wm_dict.get("url", "/d")
            if t == "/d":
                return "❌ Off"
            if u == "/d":
                return f"✅ `{t[:18]}`"
            return f"✅ `{t[:15]}` 🔗"

        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📑 𝐏𝐃𝐅 𝐖𝐀𝐓𝐄𝐑𝐌𝐀𝐑𝐊 𝐋𝐎𝐂𝐀𝐓𝐈𝐎𝐍𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            f"↗️ **Upper Right**: {_wm_status(globals.pdf_wm_upper_right)}\n"
            f"↖️ **Upper Left**: {_wm_status(globals.pdf_wm_upper_left)}\n"
            f"↘️ **Down Right**: {_wm_status(globals.pdf_wm_down_right)}\n"
            f"↙️ **Down Left**: {_wm_status(globals.pdf_wm_down_left)}\n"
            f"⬇️ **Down Middle**: {_wm_status(globals.pdf_wm_down_middle)}\n\n"
            "<blockquote>Tap a location to set/disable its watermark.\n"
            "All enabled locations appear on every PDF page simultaneously.</blockquote>\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        await callback_query.message.edit(caption, reply_markup=keyboard)

    # ── HELPER: GENERIC PDF WATERMARK LOCATION SETTER ───────────────────────
    def _make_pdfwm_handler(location_key: str, location_label: str, bot_ref):
        @bot_ref.on_callback_query(filters.regex(f"^{location_key}$"))
        async def _handler(client, callback_query):
            back_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
                [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐏𝐃𝐅 𝐖𝐌", callback_data="pdf_wateermark_command")]
            ])

            caption1 = (
                f"╭─━━━━━━ 💜 ━━━━━━─╮\n"
                f"   📑 {location_label} 𝐖𝐀𝐓𝐄𝐑𝐌𝐀𝐑𝐊\n"
                f"╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
                f"**Step 1/2:** Send Title text (max 40 chars)\n"
                f"Or send `/d` to **disable** this location.\n\n"
                f"<blockquote>Examples: Shahrukh Khan, My Batch</blockquote>"
            )
            editable = await callback_query.message.edit(caption1, reply_markup=back_kb)
            input_title = None
            input_url = None
            try:
                input_title = await bot_ref.listen(editable.chat.id)
                if input_title.text.strip().lower() == "/d":
                    attr = location_key.replace("pdfwm_", "pdf_wm_")
                    setattr(globals, attr, {"title": "/d", "url": "/d"})
                    await editable.edit(f"✅ **{location_label}** watermark **disabled**.", reply_markup=back_kb)
                    return

                title_val = input_title.text.strip()[:40]

                caption2 = (
                    f"╭─━━━━━━ 💜 ━━━━━━─╮\n"
                    f"   📑 {location_label} 𝐖𝐀𝐓𝐄𝐑𝐌𝐀𝐑𝐊\n"
                    f"╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
                    f"**Step 2/2:** Send URL (must start with http/https)\n"
                    f"Or send `/d` if **no URL** needed.\n\n"
                    f"<blockquote>Title set: `{title_val}`</blockquote>"
                )
                await editable.edit(caption2, reply_markup=back_kb)
                input_url = await bot_ref.listen(editable.chat.id)
                url_text = input_url.text.strip() if input_url.text else "/d"

                if url_text.lower() == "/d" or not (url_text.startswith("http://") or url_text.startswith("https://")):
                    url_val = "/d"
                else:
                    url_val = url_text

                attr = location_key.replace("pdfwm_", "pdf_wm_")
                setattr(globals, attr, {"title": title_val, "url": url_val})

                url_info = f" with URL 🔗" if url_val != "/d" else " (title only)"
                await editable.edit(
                    f"✅ **{location_label}** watermark set!\n\n"
                    f"**Title:** `{title_val}`\n"
                    f"**URL:** `{url_val}`{url_info}",
                    reply_markup=back_kb
                )
            except Exception as e:
                await editable.edit(f"<b>❌ Error:</b>\n<blockquote>{str(e)}</blockquote>", reply_markup=back_kb)
            finally:
                try:
                    if input_title is not None: await input_title.delete(True)
                except Exception: pass
                try:
                    if input_url is not None: await input_url.delete(True)
                except Exception: pass

    _make_pdfwm_handler("pdfwm_upper_right", "↗️ Upper Right", bot)
    _make_pdfwm_handler("pdfwm_upper_left",  "↖️ Upper Left",  bot)
    _make_pdfwm_handler("pdfwm_down_right",  "↘️ Down Right",  bot)
    _make_pdfwm_handler("pdfwm_down_left",   "↙️ Down Left",   bot)
    _make_pdfwm_handler("pdfwm_down_middle", "⬇️ Down Middle", bot)

    # ── VIDEO QUALITY ───────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("quality_command"))
    async def handle_quality(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   📽️ 𝐕𝐈𝐃𝐄𝐎 𝐐𝐔𝐀𝐋𝐈𝐓𝐘\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Enter resolution: `144`, `240`, `360`,\n"
            "  `480`, `720`, or `1080`.\n\n"
            "✧ Send `/d` for default (480p).\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            res_map = {
                "144": ("144", "256x144"), "240": ("240", "426x240"), "360": ("360", "640x360"),
                "480": ("480", "854x480"), "720": ("720", "1280x720"), "1080": ("1080", "1920x1080")
            }
            choice = input_msg.text.lower()
            if choice in res_map:
                globals.raw_text2, globals.res = res_map[choice]
                globals.quality = f"{globals.raw_text2}p"
                await editable.edit(f"✅ **Video Quality set to {globals.quality}!**", reply_markup=keyboard)
            else:
                globals.raw_text2, globals.res = "480", "854x480"
                globals.quality = "480p"
                await editable.edit(f"✅ **Video Quality set to {globals.quality} (Default)!**", reply_markup=keyboard)  
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Video Quality:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── TOPIC IN CAPTION ────────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("topic_command"))
    async def handle_topic(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🏷️ 𝐓𝐎𝐏𝐈𝐂 𝐈𝐍 𝐂𝐀𝐏𝐓𝐈𝐎𝐍\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "✧ Extract topic from `(brackets)` in title.\n\n"
            "✧ Send `/yes` to enable.\n"
            "✧ Send `/d` to disable.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/yes":               
                globals.topic = "/yes"
                await editable.edit(f"✅ **Topic enabled in Caption!**", reply_markup=keyboard)
            else:
                globals.topic = "/d"
                await editable.edit(f"✅ **Topic disabled in Caption!**", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Topic:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

    # ── RESET ALL SETTINGS ──────────────────────────────────────────────────
    @bot.on_callback_query(filters.regex("resset_command"))
    async def handle_reset(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 • @Blaster_fazxe", url="https://t.me/Blaster_fazxe")],
            [InlineKeyboardButton("🔙 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬", callback_data="setttings")]
        ])
        caption = (
            "╭─━━━━━━ 💜 ━━━━━━─╮\n"
            "   🔄 𝐑𝐄𝐒𝐄𝐓 𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒\n"
            "╰─━━━━━━ 💜 ━━━━━━─╯\n\n"
            "⚠️ **Warning:** This will reset all your\n"
            "  custom settings, tokens, and watermarks\n"
            "  back to their default state.\n\n"
            "✧ Send `/yes` to confirm.\n"
            "✧ Send `/no` to cancel.\n\n"
            "👑 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲: @Blaster_fazxe"
        )
        editable = await callback_query.message.edit(caption, reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/yes":
                globals.caption = '/cc1'
                globals.endfilename = '/d'
                globals.thumb = '/d'
                globals.CR = f"{CREDIT}"
                globals.cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                globals.cptoken = "cptoken"
                globals.pwtoken = "pwtoken"
                globals.vidwatermark = '/d'
                globals.pdfwatermark = '/d'
                globals.videocover = '/d'
                globals.pdfthumb = '/d'
                globals.raw_text2 = '480'
                globals.quality = '480p'
                globals.res = '854x480'
                globals.topic = '/d'
                
                globals.pdf_wm_upper_right = {"title": "/d", "url": "/d"}
                globals.pdf_wm_upper_left  = {"title": "/d", "url": "/d"}
                globals.pdf_wm_down_right  = {"title": "/d", "url": "/d"}
                globals.pdf_wm_down_left   = {"title": "/d", "url": "/d"}
                globals.pdf_wm_down_middle = {"title": "/d", "url": "/d"}
                
                _THUMB_STORE = "pdfthumb_store.json"
                if os.path.exists(_THUMB_STORE):
                    os.remove(_THUMB_STORE)
                _VCOVER_STORE = "videocover_store.json"
                if os.path.exists(_VCOVER_STORE):
                    os.remove(_VCOVER_STORE)
                    
                await editable.edit(f"✅ **Settings reset to default!**", reply_markup=keyboard)
            else:
                await editable.edit(f"✅ **Settings Not Changed!**", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to Reset Settings:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)