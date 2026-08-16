import os
import json
import requests
import subprocess
from vars import OWNER, CREDIT, AUTH_USERS, TOTAL_USERS
from pyrogram import Client, filters
from pyrogram.types import Message

# ── Persistent AUTH store ────────────────────────────────────────────────────
_AUTH_STORE = "auth_store.json"

def _load_auth_store() -> list:
    """Load persisted AUTH_USERS from JSON file."""
    if os.path.exists(_AUTH_STORE):
        try:
            with open(_AUTH_STORE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [int(x) for x in data.get("auth_users", [])]
        except Exception as e:
            print(f"[auth] Load error: {e}")
    return []

def _save_auth_store():
    """Save current AUTH_USERS list to JSON file."""
    try:
        with open(_AUTH_STORE, "w", encoding="utf-8") as f:
            json.dump({"auth_users": list(AUTH_USERS)}, f, indent=2)
    except Exception as e:
        print(f"[auth] Save error: {e}")

def load_auth_users_on_start():
    """
    Bot start par call karo — persisted users ko AUTH_USERS mein add karo.
    vars.py ke AUTH_USERS pehle se load hote hain (env vars se),
    hum sirf additional saved users merge karte hain.
    """
    saved = _load_auth_store()
    added = 0
    for uid in saved:
        if uid not in AUTH_USERS:
            AUTH_USERS.append(uid)
            added += 1
    if added:
        print(f"[auth] Loaded {added} persisted auth users from {_AUTH_STORE}")

# ── Load on import ───────────────────────────────────────────────────────────
load_auth_users_on_start()

# ────────────────────────────────────────────────────────────────────────────

def register_authorisation_handlers(bot):
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_message(filters.command("addauth") & filters.private)
    async def add_auth_user(client: Client, message: Message):
        if message.chat.id != OWNER:
            return 
        try:
            new_user_id = int(message.command[1])
            if new_user_id in AUTH_USERS:
                await message.reply_text("**this User ID is already authorized🙆🏿‍♀️.**")
            else:
                AUTH_USERS.append(new_user_id)
                _save_auth_store()  # ← Persist karo immediately
                await message.reply_text(f"**User ID `{new_user_id}` ✅Successfully added to authorized users.**")
                await client.send_message(chat_id=new_user_id, text=f"<b>✅Great Baby You are added in Premium Membership!</b>")
        except (IndexError, ValueError):
            await message.reply_text("**Please provide a valid user ID🙄.**")
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_message(filters.command("users") & filters.private)
    async def list_auth_users(client: Client, message: Message):
        if message.chat.id != OWNER:
            return
    
        user_list = '\n'.join(map(str, AUTH_USERS))
        await message.reply_text(f"**Overall Authorized Users:**\n{user_list}")
  
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_message(filters.command("rmauth") & filters.private)
    async def remove_auth_user(client: Client, message: Message):
        if message.chat.id != OWNER:
            return
    
        try:
            user_id_to_remove = int(message.command[1])
            if user_id_to_remove not in AUTH_USERS:
                await message.reply_text("**this User ID is not in the authorized users list🙆🏿‍♀️.**")
            else:
                AUTH_USERS.remove(user_id_to_remove)
                _save_auth_store()  # ← Persist karo immediately
                await message.reply_text(f"**User ID `{user_id_to_remove}` ✅ Done! user removed from authorized users.**")
                await client.send_message(chat_id=user_id_to_remove, text=f"<b>🫩Oops! You are removed from Premium Membership!</b>")
        except (IndexError, ValueError):
            await message.reply_text("**Please provide a valid user ID🙄.**")
          
