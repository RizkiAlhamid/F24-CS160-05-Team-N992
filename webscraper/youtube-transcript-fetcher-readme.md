# YouTube Transcript Fetcher

This Python script fetches transcripts from the most recent non-Short videos of specified YouTube channels. It also retrieves general channel information and manages API quota usage.

## Features

- Fetches channel information (title, description, subscriber count, etc.)
- Retrieves transcripts from the 5 most recent non-Short videos for each channel
- Ignores YouTube Shorts
- Manages YouTube API quota usage
- Saves data in JSON format

## Prerequisites

- Python 3.6 or higher
- A Google Cloud Project with the YouTube Data API v3 enabled
- A YouTube API key

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages:

   ```bash
   pip install google-api-python-client youtube_transcript_api python-dotenv google-cloud-resource-manager
   ```

3. Create a `.env` file in the same directory as the script with the following content:

   ```
   YOUTUBE_API_KEY=your_actual_api_key
   GOOGLE_CLOUD_PROJECT_ID=your_project_id
   ```

   Replace `your_actual_api_key` with your YouTube API key and `your_project_id` with your Google Cloud Project ID.

4. Create a file named `channel_ids.txt` in the same directory as the script. Add the YouTube channel IDs you want to process, one per line.

## Usage

Run the script with:

```bash
python fetch_transcripts.py
```

The script will:
1. Read channel IDs from `channel_ids.txt`
2. For each channel:
   - Fetch channel information
   - Retrieve the 5 most recent non-Short videos
   - Download transcripts for these videos
3. Save the data in JSON files in a `channel_data` directory

## Output

For each processed channel, a JSON file is created in the `channel_data` directory. The file name is `{channel_id}_data.json`. Each file contains:

- Channel information (ID, title, description, subscriber count, etc.)
- Data for up to 5 recent videos, including:
  - Video ID
  - Title
  - Published date
  - Full transcript text

## API Quota Management

The script checks the remaining quota before processing each channel. If the quota falls below a specified threshold (default is 1000 units), the script will stop executing to prevent quota exhaustion.

## Notes

- Ensure you comply with YouTube's terms of service and API usage policies.
- The script uses additional quota to check video duration for filtering out Shorts. Monitor your quota usage in the Google Cloud Console.
- Transcripts may not be available for all videos. The script will log when it can't fetch a transcript.

## Troubleshooting

- If you encounter quota errors, wait until your quota resets or request a quota increase from Google.
- Ensure your API key has the necessary permissions and that the YouTube Data API is enabled in your Google Cloud project.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or bug fixes.

## License

[Specify your chosen license here]
