import os
import json
import argparse
from typing import List, Dict, Any

def parse_json_files(folder_path: str) -> List[Dict[str, Any]]:
    all_videos = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                cid = data.get('CID', '')
                channel = data.get('channel', '')
                
                for video in data.get('videos', []):
                    video_data = {
                        'CID': cid,
                        'channel': channel,
                        'vid': video.get('vid', ''),
                        'title': video.get('title', ''),
                        'published_at': video.get('published_at', ''),
                        'logline':(''),
                        'summary':(''),
                        'tags':(''),
                        'main_topic':(''),
                        'key_points':(''),
                        'sentiment':(''),
                        'transcript': video.get('transcript', '')

                    }
                    all_videos.append(video_data)
    
    return all_videos

def main():
    parser = argparse.ArgumentParser(description="Parse JSON files and create a single consolidated JSON file for all videos.")
    parser.add_argument("input_folder", help="Path to the folder containing input JSON files")
    parser.add_argument("output_file", help="Path to the output JSON file")
    args = parser.parse_args()

    try:
        all_videos = parse_json_files(args.input_folder)
        
        with open(args.output_file, 'w') as output_file:
            json.dump(all_videos, output_file, indent=2)
        
        print(f"Processing complete. Created file: {args.output_file}")
        print(f"Total videos processed: {len(all_videos)}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()