import os
import json
import argparse
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime, timedelta
from llm_processor import process_video 
from typing import Dict, Any

load_dotenv()

def read_channel_ids(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        channel = response['items'][0]
        return {
            'CID': channel['id'],
            'channel': channel['snippet']['title'],
            'description': channel['snippet']['description'],
            'subscriber_count': channel['statistics']['subscriberCount'],
            'video_count': channel['statistics']['videoCount'],
            'view_count': channel['statistics']['viewCount']
        }
    return None

def get_recent_video_ids(youtube, channel_id, max_results=50):  # Increased to 50 to have more candidates
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=max_results
    )
    
    response = request.execute()
    return [(item['id']['videoId'], item['snippet']['title'], item['snippet']['publishedAt']) for item in response['items']]

def is_not_short(youtube, video_id):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        duration = response['items'][0]['contentDetails']['duration']
        # Convert duration to seconds
        duration_seconds = parse_duration(duration)
        # Consider videos longer than 60 seconds as not Shorts
        return duration_seconds > 60
    return False

def parse_duration(duration):
    # Remove 'PT' from the beginning of the duration string
    duration = duration[2:]
    seconds = 0
    # Parse hours
    if 'H' in duration:
        hours, duration = duration.split('H')
        seconds += int(hours) * 3600
    # Parse minutes
    if 'M' in duration:
        minutes, duration = duration.split('M')
        seconds += int(minutes) * 60
    # Parse seconds
    if 'S' in duration:
        s, _ = duration.split('S')
        seconds += int(s)
    return seconds

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join(item['text'] for item in transcript)
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {str(e)}")
        return None

def save_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_persona(persona_file: str, persona_id: str = None) -> Dict[str, Any]:
    with open(persona_file, 'r') as f:
        personas_data = json.load(f)
    personas = personas_data['personas']
    
    if persona_id:
        for persona in personas:
            if persona['id'] == persona_id:
                return persona
        raise ValueError(f"Persona with ID '{persona_id}' not found in the personas file.")
    else:
        # Return the first persona as default
        return personas[0]

def main():
    parser = argparse.ArgumentParser(description="Process YouTube videos with a specific persona.")
    parser.add_argument("--persona", help="ID of the persona to use (default: first persona in the file)")
    args = parser.parse_args()

    if not API_KEY:
        raise ValueError("No API key found. Set the YOUTUBE_API_KEY environment variable.")

    CHANNEL_IDS_FILE = 'channel_ids.txt'
    OUTPUT_DIR = 'channel_data'
    PERSONA_FILE = 'persona.json'

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channel_ids = read_channel_ids(CHANNEL_IDS_FILE)
    persona = load_persona(PERSONA_FILE, args.persona)

    print(f"Using persona: {persona['name']} (ID: {persona['id']})")

    for channel_id in channel_ids:
        print(f"Processing channel: {channel_id}")
        channel_info = get_channel_info(youtube, channel_id)
        
        if not channel_info:
            print(f"Could not fetch info for channel: {channel_id}")
            continue
        
        videos = get_recent_video_ids(youtube, channel_id)
        channel_info['videos'] = []
        
        for video_id, video_title, published_at in videos:
            if is_not_short(youtube, video_id):
                transcript = get_video_transcript(video_id)
                video_info = {
                    'CID': channel_info['CID'],
                    'channel': channel_info['channel'],
                    'vid': video_id,
                    'title': video_title,
                    'published_at': published_at,
                    'transcript': transcript
                }
                
                try:
                    # Process the video with the LLM using the selected persona
                    processed_video = process_video(video_info, persona)
                    channel_info['videos'].append(processed_video)
                    
                    if transcript:
                        print(f"Fetched and processed transcript for video: {video_title}")
                    else:
                        print(f"No transcript available for video: {video_title}")
                except Exception as e:
                    print(f"Error processing video {video_id}: {str(e)}")
                    # Add the video without LLM processing
                    channel_info['videos'].append(video_info)
                
                if len(channel_info['videos']) == 1:
                    break  # Stop after getting 5 non-Short videos
            else:
                print(f"Skipped Short video: {video_title}")
        
        filename = f"{OUTPUT_DIR}/{channel_id}_data.json"
        save_data(channel_info, filename)
        print(f"Saved data for channel: {channel_info['channel']}\n")

if __name__ == "__main__":
    main()