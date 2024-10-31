import os
import json
import anthropic
import openai
from dotenv import load_dotenv


load_dotenv()


# Load API keys from environment variables


# Initialize API clients
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
openai.api_key = OPENAI_API_KEY


def process_transcript(transcript, api="claude"):
    if api == "claude":
        return process_with_claude(transcript)
    elif api == "openai":
        return process_with_openai(transcript)
    else:
        raise ValueError("Invalid API choice. Use 'claude' or 'openai'.")


def process_with_claude(transcript):
    prompt = f"""
    Analyze the following video transcript and provide:
    1. A logline (a one-sentence summary of the video content)
    2. A concise summary (max 3 sentences)
    3. 5 relevant tags
    4. The main topic discussed
    5. Key points (max 5 bullet points)
    6. Sentiment (positive, negative, or neutral)

    Transcript:
    {transcript}

    Format your response as a JSON object with the following keys:
    logline, summary, tags, main_topic, key_points, sentiment
    """

    response = anthropic_client.completions.create(
        model="claude-2.1",
        prompt=prompt,
        max_tokens_to_sample=1000,
    )

    return json.loads(response.completion)


def process_with_openai(transcript):
    prompt = f"""
    Analyze the following video transcript and provide:
    1. A logline (a one-sentence summary of the video content)
    2. A concise summary (max 3 sentences)
    3. 5 relevant tags
    4. The main topic discussed
    5. Key points (max 5 bullet points)
    6. Sentiment (positive, negative, or neutral)

    Transcript:
    {transcript}

    Format your response as a JSON object with the following keys:
    logline, summary, tags, main_topic, key_points, sentiment
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes video transcripts."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)


def process_channel_data(input_file, output_file, api="claude"):
    with open(input_file, 'r', encoding='utf-8') as f:
        channel_data = json.load(f)

    summarized_videos = []

    for video in channel_data['videos']:
        if video['transcript']:
            llm_analysis = process_transcript(video['transcript'], api)
            summarized_video = {
                "url": f"https://www.youtube.com/watch?v={video['id']}",
                "metadata": {
                    "title": video['title'],
                    "author": channel_data['title'],
                    "publication_date": video['published_at'],
                    "description": video.get('description', '')
                },
                "analytics": {
                    "view_count": video.get('view_count', 0),
                    "like_count": video.get('like_count', 0),
                    "comment_count": video.get('comment_count', 0)
                },
                "llm_analysis": llm_analysis
            }
            summarized_videos.append(summarized_video)
        else:
            print(f"No transcript available for video: {video['title']}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summarized_videos, f, ensure_ascii=False, indent=2)


def main():
    input_directory = 'channel_data'
    output_directory = 'processed_channel_data'
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('_data.json'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f"processed_{filename}")
            
            print(f"Processing {filename}...")
            process_channel_data(input_file, output_file, api="claude")  # Change to "openai" if preferred
            print(f"Processed data saved to {output_file}")


if __name__ == "__main__":
    main()
