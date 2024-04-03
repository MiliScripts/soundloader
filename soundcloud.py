# ________________ SoundCLoud Auto Downloader -  By mili -  2024_____________________

import aiohttp
import asyncio
import requests
import json
import youtube_dl
from fake_useragent import UserAgent
import re
import os
ua = UserAgent() # fake agent For prevent Being Banned

# Fill This Yourself //

last_song = "" # stores last Likes Song / Updates and Compares
bot_token = '' # --- Your B OT Token here
chat_id   = '' # --- Your Channel ID here
user_id = ""   # --- Your Soundcloud User Id here
headers = {
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
    'User-Agent': ua.random
}

def findClientID():
    """
    Gets Fresh SoundCloud ClientId // 
    
    """
    sc = requests.get('https://soundcloud.com/').text
    scVersion = re.search(r'<script>window\.__sc_version="[0-9]{10}"<\/script>', sc).group(0)
    scVersion = re.search(r'[0-9]{10}', scVersion).group(0)
    scripts = re.findall(r'<script.+src="(.+)">', sc)
    clientid = None
    for url in scripts:
        if url and not url.startswith('https://a-v2.sndcdn.com'):
            return
        scrf =  requests.get(url).text
        id_match = re.search(r'\("client_id=[A-Za-z0-9]{32}"\)', scrf)
        if id_match and isinstance(id_match.group(0), str):
            clientid = re.search(r'[A-Za-z0-9]{32}', id_match.group(0)).group(0)
            return clientid
    
    


        



async def get_latest_liked_song():
    
    """
    Fetches Last Liked Song From SoundCloud
    
    """
    client_id = findClientID()
    base_url = f'https://api-v2.soundcloud.com/users/{user_id}/track_likes?client_id={client_id}&limit=1&offset=1&linked_partitioning=1&app_version=1693487844&app_locale=en'
    data = requests.get(url=base_url, headers=headers)
    tracks_json = json.loads(data.content)["collection"][0]
    track_urk = tracks_json['track']["permalink_url"]
    return track_urk

def get_sc_track_audio(song_url):
    """
    Gets download link of track with help of youtube_dl //
    
    """
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
        thumb = info_dict['thumbnails'][6]['url']
        uploader = info_dict.get("uploader", None)
        
        return [title, cover, url, uploader,thumb]


async def donwload_track(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                # print(f"Downloaded file: {filename}")
            else:
                print(f"Failed to download file: {response.status}")
                
                
                
async def download_photo(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                return filename
            else:
                print(f"Failed to download thumbnail: {response.status}")  
                
                              
async def send_track_to_telegram(file_path,cover,performer):
    url = f'https://api.telegram.org/bot{bot_token}/sendAudio'
    files = {'audio': open(file_path, 'rb'),'thumb' :open(cover,'rb')}
    params = {'chat_id': chat_id,"performer":performer}
    response = requests.post(url, files=files, data=params)
    if response.status_code == 200:
        pass
    else:
        print(f"Failed to send file to Telegram channel: {response.text}")

async def send_photo_and_caption_to_telegram(photo_path, caption):
    """
    Send Photo with caption to telegram Channel using telegram api
    """
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    files = {'photo': open(photo_path, 'rb')}
    params = {'chat_id': chat_id, 'caption': caption}
    response = requests.post(url, files=files, data=params)
    if response.status_code == 200:
        pass
    else:
        print(f"Failed to send photo to Telegram channel: {response.text}")


async def check_and_download():
    
    """
    Checks the last liked song and compared with the last_song variable
    if any changed updated last_song and downloads the new one 
    """
    
    global last_song
    while True:
        latest_song = await get_latest_liked_song()
        if latest_song != last_song:
            
            last_song = latest_song
            d = get_sc_track_audio(last_song)
            print("New Song Liked {}".format(d[0]))
            url = d[2]
            filename = d[0]+'.mp3'
            await donwload_track(url,filename)
            photo = await download_photo(d[1],"cover.jpg")
            
            thumb = d[-1]
            tm = await download_photo(thumb,"t.jpg")
            await send_photo_and_caption_to_telegram(photo_path=photo,caption=d[0]+'\n@imilisong')
            await send_track_to_telegram(filename,tm,d[-2])
            
            
            os.remove(filename)
            os.remove(photo)
            os.remove(tm)
            
            
        await asyncio.sleep(7)  

async def main():
    await check_and_download()



asyncio.run(main())
