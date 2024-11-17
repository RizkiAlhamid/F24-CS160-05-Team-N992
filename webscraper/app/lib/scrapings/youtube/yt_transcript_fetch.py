import os
import json
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from app.lib.llm.llm_processor import process_video
from typing import Dict, Any, List, Tuple
import aiohttp
import asyncio
from app.lib.credentials import YOUTUBE_API_KEY
from pathlib import Path


DATA_PATH = Path("./data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir(exist_ok=True)

BASE_URL = "https://www.googleapis.com/youtube/v3"


async def fetch_data(session, url, params):
    """Fetches data from YouTube API asynchronously."""
    async with session.get(url, params=params) as response:
        return await response.json()


async def get_channel_info(session, channel_id) -> Dict[str, Any]:
    """Fetches channel information."""
    url = f"{BASE_URL}/channels"
    params = {
        "part": "snippet,statistics",
        "id": channel_id,
        "key": YOUTUBE_API_KEY
    }
    data = await fetch_data(session, url, params)
    if 'items' in data and data['items']:
        channel = data['items'][0]
        return {
            'CID': channel['id'],
            'channel': channel['snippet']['title'],
            'description': channel['snippet']['description'],
            'subscriber_count': channel['statistics']['subscriberCount'],
            'video_count': channel['statistics']['videoCount'],
            'view_count': channel['statistics']['viewCount']
        }
    return {}


async def get_recent_video_ids(session, channel_id, max_results=50) -> List[Tuple[str, str, str]]:
    """Fetches recent video IDs for a channel."""
    url = f"{BASE_URL}/search"
    params = {
        "part": "id,snippet",
        "channelId": channel_id,
        "order": "date",
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY 
    }
    data = await fetch_data(session, url, params)
    return [(item['id']['videoId'], item['snippet']['title'], item['snippet']['publishedAt']) for item in data['items']]


async def is_not_short(session, video_id) -> bool:
    """Checks if a video is not a YouTube Short (longer than 60 seconds)."""
    url = f"{BASE_URL}/videos"
    params = {
        "part": "contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY 
    }
    data = await fetch_data(session, url, params)
    if 'items' in data and data['items']:
        duration = data['items'][0]['contentDetails']['duration']
        return parse_duration(duration) > 60
    return False


def parse_duration(duration) -> int:
    """Parses an ISO 8601 duration into seconds."""
    duration = duration[2:]  # Strip 'PT'
    seconds = 0
    if 'H' in duration:
        hours, duration = duration.split('H')
        seconds += int(hours) * 3600
    if 'M' in duration:
        minutes, duration = duration.split('M')
        seconds += int(minutes) * 60
    if 'S' in duration:
        seconds += int(duration.split('S')[0])
    return seconds


async def get_video_transcript(video_id) -> str:
    """Fetches video transcript."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join(item['text'] for item in transcript)
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {str(e)}")
        return ""


def save_data(data, filename):
    """Saves JSON data to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_persona(persona_file: str, persona_id: str) -> Dict[str, Any]:
    """Loads persona data from a file."""
    with open(persona_file, 'r') as f:
        personas_data = json.load(f)
    personas = personas_data['personas']
    if persona_id:
        for persona in personas:
            if persona['id'] == persona_id:
                return persona
        raise ValueError(f"Persona with ID '{persona_id}' not found in the personas file.")
    return personas[0]


async def process_channel(session, channel_id, persona) -> Dict[str, Any]:
    """Processes a single channel, gathering its data and video information."""
    channel_info = await get_channel_info(session, channel_id)
    if not channel_info:
        print(f"Could not fetch info for channel: {channel_id}")
        return {}
    
    videos = await get_recent_video_ids(session, channel_id)
    channel_info['videos'] = []
    
    for video_id, video_title, published_at in videos:
        if await is_not_short(session, video_id):
            transcript = await get_video_transcript(video_id)
            video_info = {
                'CID': channel_info['CID'],
                'channel': channel_info['channel'],
                'vid': video_id,
                'title': video_title,
                'published_at': published_at,
                'transcript': transcript
            }
            try:
                processed_video = process_video(video_info, persona)
                channel_info['videos'].append(processed_video)
            except Exception as e:
                print(f"Error processing video {video_id}: {str(e)}")
                channel_info['videos'].append(video_info)
        else:
            print(f"Skipped Short video: {video_title}")
    
    return channel_info


async def main_async(persona_id):
    """Main asynchronous function to process multiple channels."""
    CHANNEL_IDS_FILE = 'channel_ids.txt'
    OUTPUT_DIR = 'channel_data'
    PERSONA_FILE = 'persona.json'

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    channel_ids = [line.strip() for line in open(CHANNEL_IDS_FILE) if line.strip()]
    persona = load_persona(PERSONA_FILE, persona_id)
    print(f"Using persona: {persona['name']} (ID: {persona['id']})")

    async with aiohttp.ClientSession() as session:
        tasks = [process_channel(session, channel_id, persona) for channel_id in channel_ids]
        results = await asyncio.gather(*tasks)
        for channel_info in results:
            if channel_info:
                filename = f"{OUTPUT_DIR}/{channel_info['CID']}_data.json"
                save_data(channel_info, filename)
                print(f"Saved data for channel: {channel_info['channel']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process YouTube videos with a specific persona.")
    parser.add_argument("--persona", help="ID of the persona to use (default: first persona in the file)")
    args = parser.parse_args()
    asyncio.run(main_async(args.persona))
