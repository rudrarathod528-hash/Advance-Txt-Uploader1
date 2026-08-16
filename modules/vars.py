#🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "33088642"))
API_HASH = environ.get("API_HASH", "bf6a7d6071350cb64849d46b8b4849e9")
BOT_TOKEN = environ.get("BOT_TOKEN", "8865197527:AAFN_2Vf9xR8eX_GWCjBhxYRdl1cZZIDTOw")

OWNER = int(environ.get("OWNER", "5808599565"))
CREDIT = environ.get("CREDIT", " @CinderellaContactBot")
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")

TOTAL_USER = os.environ.get('TOTAL_USERS', '5808599565').split(',')
TOTAL_USERS = [int(user_id) for user_id in TOTAL_USER]

AUTH_USER = os.environ.get('AUTH_USERS', '5808599565').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))

