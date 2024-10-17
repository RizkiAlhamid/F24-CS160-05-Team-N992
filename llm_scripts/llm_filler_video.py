import os
import json
import argparse
import requests
import time
from typing import List, Dict, Any

# Perplexity API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"

def process_with_perplexity(transcript: str, max_retries=3, delay=5):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Analyze the following video transcript and provide a logline, summary, tags, main topic, key points, and sentiment. Transcript: {transcript[:1000]}..."
    
    data = {
        "model": "llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "Format your response as a JSON object with the following keys: logline, summary, tags, main_topic, key_points, sentiment"},
            {"role": "user", "content": prompt}
        ]
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            return json.loads(result['choices'][0]['message']['content'])
        
        except requests.exceptions.RequestException as e:
            if "429" in str(e):  # Rate limit error
                if attempt < max_retries - 1:
                    print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Rate limit error after {max_retries} attempts: {str(e)}")
                    return {}
            else:
                print(f"An error occurred: {str(e)}")
                return {}

def update_video_info(video: Dict[str, Any]) -> Dict[str, Any]:
    transcript = video.get('transcript', '')
    perplexity_result = process_with_perplexity(transcript)
    
    # Update the video dictionary with new information
    video.update({
        'logline': perplexity_result.get('logline', ''),
        'summary': perplexity_result.get('summary', ''),
        'tags': perplexity_result.get('tags', ''),
        'main_topic': perplexity_result.get('main_topic', ''),
        'key_points': perplexity_result.get('key_points', ''),
        'sentiment': perplexity_result.get('sentiment', ''),
    })
    
    print(f"Updated video: {video.get('vid', 'Unknown ID')}")
    return video

def process_json_file(input_file: str, output_file: str):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
        
        if isinstance(data, list):
            # Process only the first element for testing
            if data:
                data[0] = update_video_info(data[0])
            updated_data = data
        elif isinstance(data, dict):
            if 'videos' in data and data['videos']:
                # Process only the first video for testing
                data['videos'][0] = update_video_info(data['videos'][0])
            else:
                # Assume it's a single video object
                updated_data = update_video_info(data)
        else:
            raise ValueError("Unexpected JSON structure")
        
        with open(output_file, 'w') as file:
            json.dump(updated_data, file, indent=2)
        
        print(f"Processing complete. Updated file: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Update JSON file with video analysis from Perplexity API.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    args = parser.parse_args()

    process_json_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

# To process all videos instead of just the first one:
# 1. In the process_json_file function, replace:
#    if data:
#        data[0] = update_video_info(data[0])
#    updated_data = data
# With:
#    updated_data = [update_video_info(video) for video in data]
#
# 2. Similarly, replace:
#    if 'videos' in data and data['videos']:
#        data['videos'][0] = update_video_info(data['videos'][0])
# With:
#    if 'videos' in data:
#        data['videos'] = [update_video_info(video) for video in data['videos']]
#
# These changes will process all videos in the JSON file instead of just the first one.
