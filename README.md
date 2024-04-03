SoundCloud Liked Songs Downloader & Telegram Sharer
This Python script allows users to automatically download their latest liked songs from SoundCloud and share them to their Telegram channel. It provides a seamless integration between SoundCloud's API, YouTube DL for song extraction, and Telegram's API for sharing.

Features
Automatic Download: Continuously monitors the user's liked songs on SoundCloud and downloads any new additions automatically.
Quality Preservation: Utilizes YouTube DL to ensure high-quality audio downloads.
Telegram Integration: Shares downloaded songs along with cover art to a specified Telegram channel or group.
Customizable: Easily configurable settings for Telegram channel ID, bot token, and file download directory.
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/soundcloud-telegram-downloader.git
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Obtain necessary tokens and IDs:

Obtain a SoundCloud API client ID by registering your application on the SoundCloud developer portal.
Create a Telegram bot and obtain the bot token.
Identify the chat ID of the Telegram channel or group where you want to share the songs.
Update the configuration:

Replace client_id.txt with your SoundCloud API client ID.
Update bot_token and chat_id variables in the script with your Telegram bot token and chat ID, respectively.
Run the script:

bash
Copy code
python soundcloud_telegram_downloader.py
Usage
Like a song on SoundCloud.
Wait for the script to detect the new liked song.
The song will be automatically downloaded and shared to your Telegram channel.
Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
