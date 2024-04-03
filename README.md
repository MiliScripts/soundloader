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
    git clone https://github.com/yourusername/soundcloud-telegram-downloader.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Obtain necessary tokens and IDs:
   - Obtain a SoundCloud API client ID by registering your application on the SoundCloud developer portal.
   - Create a Telegram bot and obtain the bot token.
   - Identify the chat ID of the Telegram channel or group where you want to share the songs.

4. Update the configuration:
   - Replace `client_id.txt` with your SoundCloud API client ID.
   - Update `bot_token` and `chat_id` variables in the script with your Telegram bot token and chat ID, respectively.

5. Run the script:

    ```bash
    python soundcloud_telegram_downloader.py
    ```

## Usage

1. Like a song on SoundCloud.
2. Wait for the script to detect the new liked song.
3. The song will be automatically downloaded and shared to your Telegram channel.
