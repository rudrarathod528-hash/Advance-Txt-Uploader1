🚀 Digizoro Uploader Bot
<div align="center">
https://img.shields.io/github/repo-size/yourusername/digizoro-uploader-bot?color=purple&style=for-the-badge
https://img.shields.io/badge/Python-3.10%252B-blue?style=for-the-badge&logo=python
https://img.shields.io/badge/Pyrogram-2.0.106-orange?style=for-the-badge
https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram
https://img.shields.io/badge/Contact-@CinderellaContactBot-blue?style=for-the-badge&logo=telegram

Powerful Telegram Bot for downloading DRM‑protected videos, PDFs, and more – with advanced link extraction & batch processing.

</div>
📖 Table of Contents
✨ Features

🖼️ Screenshots

⚙️ Setup & Installation

🔧 Configuration

🤖 Bot Commands

📡 Deployment

👨‍💻 Credits

📞 Contact

✨ Features
TXT & Link Processing – Upload a .txt file or send direct links; the bot extracts, downloads, and uploads videos/PDFs in bulk.

DRM Support – Handles encrypted streams (Widevine, MPD, M3U8, AES‑encrypted .m files) with token‑based decryption.

Batch Management – Set custom batch names, resolution (144p to 1080p), credits, thumbnails, and watermark.

Premium & Owner Flow –

Owner bypasses all checks – just /love and send TXT.

Premium Users (in AUTH_USERS) require /download eligibility before using /love.

Unauthorized users are politely redirected.

One‑time Permission – /love enables a single TXT upload session; after processing, permission is revoked automatically.

Live API Switching – Owner can update the Physics Wallah API endpoint on‑the‑fly via /changeapi.

Progress & Sticker Feedback – Real‑time download/upload status with animated stickers.

Fault‑Tolerant – Retries on failures, sends failure notices per link.

Multi‑Format Support – Videos, PDFs, images, audio, zip files, and HTML.

🖼️ Screenshots
Coming soon – we’ll add preview images of the bot in action!

⚙️ Setup & Installation
Prerequisites
Python 3.10 or higher

A Telegram Bot Token (from @BotFather)

ffmpeg installed on your system (for video processing)

(Optional) yt-dlp for enhanced downloading

1. Clone the Repository
bash
git clone https://github.com/yourusername/digizoro-uploader-bot.git
cd digizoro-uploader-bot
2. Install Dependencies
bash
pip install -r requirements.txt
Note: The requirements.txt should include pyrogram, pyromod, aiohttp, cloudscraper, ffmpeg‑python, yt‑dlp, m3u8, tgcrypto, etc. – adjust according to your imports.

3. Set Environment Variables
Create a .env file or export the following variables:

env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER=your_telegram_user_id
AUTH_USERS=comma,separated,user_ids  # premium users
CREDIT=Your_Credit_Name             # default credit text
Alternatively, you can edit vars.py directly.

4. Run the Bot
bash
python bot.py
Replace bot.py with the entry point of your application (likely the file that calls Client.run()).

🔧 Configuration
All configurable variables are in vars.py and globals.py. Key ones:

Variable	Description
OWNER	Telegram User ID of the owner (bypasses premium check)
AUTH_USERS	List of premium user IDs (comma‑separated)
PWAPI1/2	Physics Wallah API endpoints (can be changed via /changeapi)
CREDIT	Default credit text (supports Text|URL for hyperlink)
thumb	Default thumbnail URL
vidwatermark	Video watermark text
pdfwatermark	PDF watermark text
cwtoken	Brightcove token
cptoken	Classplus token
pwtoken	Physics Wallah token
🤖 Bot Commands
Command	Who	Description
/download	All users	Grants eligibility to send TXT/link (required for premium users before /love)
/Love	Owner & premium	Enables the TXT upload session – owner bypasses /download, premium needs it first.
/start	All users	Welcome message.
/stop	All users (during download)	Cancels the ongoing download process.
/changeapi	Owner only	Updates the PW API endpoint globally. Usage: /changeapi <new_url>
/owner	All users	Shows contact info of the owner.
(send .txt)	After /love	The bot processes the TXT file – asks for batch name, resolution, tokens, credit, thumb, channel ID.
📡 Deployment
Docker (coming soon)
A Dockerfile is on the way – stay tuned!

Manual Deployment (e.g., on VPS)
Install ffmpeg:

bash
sudo apt update && sudo apt install ffmpeg -y
Set up Python environment and install dependencies.

Run the bot using screen or systemd to keep it alive.

Heroku / Railway
Make sure to add environment variables in the dashboard and include ffmpeg buildpack if needed.

👨‍💻 Credits
Bot Developer – ArzanXD

Powered by – Digizoro

Special Thanks – All contributors and supporters.

Disclaimer: This bot is intended for educational purposes only. Users are responsible for respecting content copyrights and DRM policies.

📞 Contact
For support, queries, or feedback:

Telegram: @CinderellaContactBot

Channel: @Digizoro_Official

<div align="center">
⭐ Star this repo if you find it useful!
Made with ❤️ by Team Digizoro

</div>