import requests
import time
import json
from bs4 import BeautifulSoup

PAGE_ID = "YOUR_PAGE_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
LAST_FILE = "last_post.json"

def get_latest_video():
    url = "REDNOTE_PROFILE_URL"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    video = soup.find("video")
    if video:
        return video.get("src")
    return None

def upload_video(video_url):
    endpoint = f"https://graph.facebook.com/v18.0/{PAGE_ID}/videos"
    payload = {
        "file_url": video_url,
        "description": "Auto posted from Rednote",
        "access_token": ACCESS_TOKEN
    }
    r = requests.post(endpoint, data=payload)
    print(r.json())

def is_new(video_url):
    try:
        with open(LAST_FILE, "r") as f:
            data = json.load(f)
            return data.get("last") != video_url
    except:
        return True

def save_last(video_url):
    with open(LAST_FILE, "w") as f:
        json.dump({"last": video_url}, f)

while True:
    try:
        video = get_latest_video()
        if video and is_new(video):
            upload_video(video)
            save_last(video)
    except Exception as e:
        print("Error:", e)

    time.sleep(600)
