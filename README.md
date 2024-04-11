# SoundCloud Liked Songs Downloader & Telegram Sharer

This Python script allows users to automatically download their latest liked songs from SoundCloud and share them to their Telegram channel. It provides a seamless integration between SoundCloud's API, YouTube DL for song extraction, and Telegram's API for sharing.

## Features

- **Automatic Download**: Continuously monitors the user's liked songs on SoundCloud and downloads any new additions automatically.
- **Quality Preservation**: Utilizes YouTube DL to ensure high-quality audio downloads.
- **Telegram Integration**: Shares downloaded songs along with cover art to a specified Telegram channel or group.
- **Customizable**: Easily configurable settings for Telegram channel ID, bot token, and file download directory.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MiliScripts/soundcloud_like_downloader.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Obtain necessary tokens and IDs:
   - Fill in your SoundCloud user ID, Telegram bot token, Telegram channel ID, and initialize the `last_song` variable to store the last liked song. You can find your SoundCloud user ID by going to your profile and copying the numerical part of the URL. For the Telegram bot token and channel ID, you need to create a bot on Telegram and get the token, as well as the ID of the channel where you want to share the songs.
   
   Example:
   ```python
   last_song = "" # stores last Likes Song / Updates and Compares
   bot_token = 'YOUR_TELEGRAM_BOT_TOKEN' # --- Your BOT Token here
   chat_id   = 'YOUR_TELEGRAM_CHANNEL_ID' # --- Your Channel ID here
   user_id = "YOUR_SOUNDCLOUD_USER_ID"   # --- Your Soundcloud User Id here
   - Update `bot_token` and `chat_id` variables in the script with your Telegram bot token and chat ID, respectively.

5. Run the script:

    ```bash
    python soundcloud.py
    ```


## Demo

### Watch the Demo Video

[!SoundCloud Telegram Downloader Demo](vid.mp4)

### Try the Bot on Telegram

[See hwo it works on my channel ](https://t.me/imilisong)

    

## Usage

1. Like a song on SoundCloud.
2. Wait for the script to detect the new liked song.
3. The song will be automatically downloaded and shared to your Telegram channel.
