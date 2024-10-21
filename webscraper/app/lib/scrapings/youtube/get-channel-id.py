from googleapiclient.discovery import build

def read_channel_names(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_channel_id(youtube, channel_name):
    request = youtube.search().list(
        part="id",
        type="channel",
        q=channel_name,
        maxResults=1
    )
    
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['id']['channelId']
    else:
        return None

def main():
    CHANNEL_LIST_FILE = 'channel_names.txt'

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channel_names = read_channel_names(CHANNEL_LIST_FILE)

    channel_ids = {}
    for name in channel_names:
        channel_id = get_channel_id(youtube, name)
        if channel_id:
            channel_ids[name] = channel_id
            print(f"Channel ID for '{name}': {channel_id}")
        else:
            print(f"Could not find a channel ID for '{name}'")

    # Optionally, save the results to a file
    with open('channel_ids.txt', 'w') as f:
        for name, channel_id in channel_ids.items():
            f.write(f"{channel_id}\n")

if __name__ == "__main__":
    main()