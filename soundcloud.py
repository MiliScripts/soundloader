# ________________ SoundCLoud Auto Downloader -  By mili -  2024_____________________

import aiohttp
import asyncio
import requests
import json
import youtube_dl
from fake_useragent import UserAgent
import re
import os

# Constants
BOT_TOKEN = ''
CHAT_ID = ''
USER_ID = ""  # Your Soundcloud User Id here

# Global Variables
LAST_SONG = ""

# HTTP Headers
HEADERS = {
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'api-v2.soundcloud.com',
    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
}


def get_client_id():
    sc = requests.get('https://soundcloud.com/').text
    sc_version = re.search(r'<script>window\.__sc_version="[0-9]{10}"<\/script>', sc).group(0)
    sc_version = re.search(r'[0-9]{10}', sc_version).group(0)

    scripts = re.findall(r'<script.+src="(.+)">', sc)
    client_id = None
    for url in scripts:
        if url and not url.startswith('https://a-v2.sndcdn.com'):
            return
        scrf = requests.get(url).text
        id_match = re.search(r'\("client_id=[A-Za-z0-9]{32}"\)', scrf)
        if id_match and isinstance(id_match.group(0), str):
            client_id = re.search(r'[A-Za-z0-9]{32}', id_match.group(0)).group(0)
            return client_id


async def get_latest_liked_song():
    try:
        base_url = f'https://api-v2.soundcloud.com/users/{USER_ID}/track_likes?client_id={get_client_id()}&limit=24&offset=24&linked_partitioning=1&app_version=1693487844&app_locale=en'
        data = requests.get(url=base_url, headers=HEADERS)
        tracks_json = json.loads(data.content)["collection"][0]
        trk_id = tracks_json['track']["permalink_url"]
        return trk_id
    except (json.JSONDecodeError, requests.exceptions.ConnectionError) as e:
        print(f"Error occurred: {e}")
        print("Sleeping for 15 minutes...")
        await asyncio.sleep(15 * 60)
        return await get_latest_liked_song()


def get_url(song_url):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(song_url, download=False)
        title = info_dict.get("title", None)
        url = info_dict['formats'][-1]['url']
        cover = info_dict['thumbnails'][-1]['url']
        try:
            thumb = info_dict['thumbnails'][6]['url']
        except IndexError:
            thumb = "meow.jpg"
        uploader = info_dict.get("uploader", None)
        track_id = info_dict.get("id")

        return [title, cover, url, uploader, thumb, track_id]


async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"Downloaded file: {filename}")
            else:
                print(f"Failed to download file: {response.status}")


async def download_thumbnail(url, filename):
    if url == "meow.jpg":
        return "meow.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"Downloaded thumbnail: {filename}")
                return filename
            else:
                print(f"Failed to download thumbnail: {response.status}")


async def send_to_telegram(file_path, cover, performer, track_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio'
    files = {'audio': open(file_path, 'rb'), 'thumb': open(cover, 'rb')}

    inline_keyboard = {"inline_keyboard": [[{"text": "✉️", "callback_data": str(track_id)}]]}
    reply_markup = json.dumps(inline_keyboard)
    params = {'chat_id': CHAT_ID, "performer": performer, 'reply_markup': reply_markup}

    response = requests.post(url, files=files, data=params)
    if response.status_code == 200:
        print("File sent to Telegram channel successfully!")
    else:
        print(f"Failed to send file to Telegram channel: {response.text}")


async def send_photo_and_caption_to_telegram(photo_path, caption):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': open(photo_path, 'rb')}
    params = {'chat_id': CHAT_ID, 'caption': caption}

    response = requests.post(url, files=files, data=params)
    if response.status_code == 200:
        print("Photo sent to Telegram channel successfully!")
    else:
        print(f"Failed to send photo to Telegram channel: {response.text}")


async def check_and_download():
    global LAST_SONG
    while True:
        latest_song = await get_latest_liked_song()
        if latest_song != LAST_SONG:
            LAST_SONG = latest_song
            data = get_url(latest_song)
            url = data[2]
            filename = data[0] + '.mp3'
            await download_file(url, filename)
            photo = await download_thumbnail(data[1], "cover.jpg")
            thumb = data[-2]
            performer = data[-3]
            track_id = data[-1]

            tm = await download_thumbnail(thumb, "t.jpg")
            await send_photo_and_caption_to_telegram(photo_path=photo, caption=data[0] + '\n@imilisong')
            await send_to_telegram(filename, tm, performer, track_id)

            print("New song downloaded!")
            os.remove(filename)
            os.remove(photo)
            os.remove(tm)

        await asyncio.sleep(13)


async def main():
    await check_and_download()


asyncio.run(main())
