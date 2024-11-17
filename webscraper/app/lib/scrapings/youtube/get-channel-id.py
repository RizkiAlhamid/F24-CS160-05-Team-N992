import aiohttp
import asyncio
from app.lib.credentials import YOUTUBE_API_KEY
from pathlib import Path


DATA_PATH = Path("./data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir(exist_ok=True)

BASE_URL = "https://www.googleapis.com/youtube/v3"

async def fetch_channel_id(session, channel_name):
    """Fetches the channel ID for a given channel name asynchronously."""
    url = f"{BASE_URL}/search"
    params = {
        "part": "id",
        "type": "channel",
        "q": channel_name,
        "maxResults": 1,
        "key": YOUTUBE_API_KEY 
    }
    
    async with session.get(url, params=params) as response:
        data = await response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']['channelId']
        return None

async def get_channel_ids(channel_names):
    """Fetches channel IDs for a list of channel names asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_channel_id(session, name) for name in channel_names]
        results = await asyncio.gather(*tasks)
        return {name: result for name, result in zip(channel_names, results) if result}

def read_channel_names(filename):
    """Reads channel names from a file and returns a list of names."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_channel_ids(channel_ids, output_file='channel_ids.txt'):
    """Saves the channel IDs to a specified file."""
    with open(output_file, 'w') as f:
        for name, channel_id in channel_ids.items():
            f.write(f"{name}: {channel_id}\n")

# Example usage
async def main():
    channel_names = read_channel_names('channel_names.txt')
    channel_ids = await get_channel_ids(channel_names)
    save_channel_ids(channel_ids)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
