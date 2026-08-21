#馃嚦鈥岎焽€岎焽扳€岎焽€岎焽€岎焽扁€�
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "4942197"))
API_HASH = environ.get("API_HASH", "13248a2c551b73193969b42194023635")
BOT_TOKEN = environ.get("BOT_TOKEN", "8889351159:AAFce50SKx2NLkD7SFMfQX2tau1esuEvh5g")

OWNER = int(environ.get("OWNER", "5808599565"))
CREDIT = environ.get("CREDIT", " @CinderellaContactBot")
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")

TOTAL_USER = os.environ.get('TOTAL_USERS', '5808599565').split(',')
TOTAL_USERS = [int(user_id) for user_id in TOTAL_USER]

AUTH_USER = os.environ.get('AUTH_USERS', '5892781710').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
    
