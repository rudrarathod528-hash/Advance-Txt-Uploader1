import os
from vars import CREDIT, OWNER
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# upgrade button
def register_upgrade_handlers(bot):
    @bot.on_callback_query(filters.regex("upgrade_command"))
    async def upgrade_button(client, callback_query):
      user_id = callback_query.from_user.id
      first_name = callback_query.from_user.first_name
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
      caption = (
               f" 🎉 Welcome [{first_name}](tg://user?id={user_id}) to DRM Bot! 🎉\n\n"
               f"You can have access to download all Non-DRM+AES Encrypted URLs 🔐 including\n\n"
               f"<blockquote>• 📚 Appx Zip+Encrypted Url\n"
               f"• 🎓 Classplus DRM+ NDRM\n"
               f"• 🧑‍🏫 PhysicsWallah DRM\n"
               f"• 📚 CareerWill + PDF\n"
               f"• 🎓 Khan GS\n"
               f"• 🎓 Study Iq DRM\n"
               f"• 🚀 APPX + APPX Enc PDF\n"
               f"• 🎓 Vimeo Protection\n"
               f"• 🎓 Brightcove Protection\n"
               f"• 🎓 Visionias Protection\n"
               f"• 🎓 Zoom Video\n"
               f"• 🎓 Utkarsh Protection(Video + PDF)\n"
               f"• 🎓 All Non DRM+AES Encrypted URLs\n"
               f"• 🎓 MPD URLs if the key is known (e.g., Mpd_url?key=key XX:XX)</blockquote>\n\n"
               f"<b>💵 Monthly Plan: 100 INR</b>\n\n"
               f"If you want to buy membership of the bot, feel free to contact [{CREDIT}](tg://user?id={OWNER})\n"
        )  
    
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/b67a919df868cbb82b3cb-131aaff80361c5af6e.jpg",
          caption=caption
        ),
        reply_markup=keyboard
   )
