import json
import requests
import time
import re
from typing import Dict, Any
from app.lib.credentials import PERPLEXITY_API_KEY

# Perplexity API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"

def create_persona_prompt(persona: Dict[str, Any]) -> str:
    prompt = f"You are {persona['name']}, a {persona['species']} who is an {persona['occupation']}.\n"
    prompt += f"You reside in {persona['residence']}.\n"
    
    # Add personality traits
    prompt += "Your personality traits are:\n"
    for trait, description in persona['personality'].items():
        prompt += f"- {trait.replace('_', ' ').capitalize()}: {description}\n"
    
    # Add background
    prompt += f"\nYour background: {persona['background']['history']}\n"
    prompt += f"Your motivation: {persona['background']['motivation']}\n"
    
    # Add goals
    prompt += "\nYour goals are:\n"
    for goal, description in persona['goals'].items():
        prompt += f"- {goal.replace('_', ' ').capitalize()}: {description}\n"
    
    return prompt


def process_with_perplexity(transcript: str, persona: Dict[str, Any], max_retries=3, delay=5) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    persona_prompt = create_persona_prompt(persona)
    
    prompt = f"{persona_prompt}\n\nPlease analyze the following video transcript in your persona and provide a response. Analyze the following video transcript and provide a logline, summary (that takes about 3 minutes to read), tags, main topic, key points, and sentiment. Format your response as a JSON object with the following keys: logline, summary, tags, main_topic, key_points, sentiment. Transcript: {transcript[:1000]}..."
    
    data = {
        "model": "llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "You must respond with a valid JSON object."},
            {"role": "user", "content": prompt}
        ]
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            # Print the raw API response for debugging
            print("Raw API response:", result)
            
            content = result['choices'][0]['message']['content']
            
            # Print the content for debugging
            print("Content to be parsed:", content)
            
            # Try to parse the entire content as JSON
            try:
                parsed_content = json.loads(content)
                return parsed_content
            except json.JSONDecodeError:
                # If parsing fails, try to extract JSON using regex
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    try:
                        parsed_content = json.loads(json_match.group())
                        return parsed_content
                    except json.JSONDecodeError:
                        print("Failed to parse extracted JSON content.")
                
                # If all parsing attempts fail, create a structured response
                print("Creating structured response from raw content.")
                return {
                    "logline": content[:100] + "...",  # First 100 characters as logline
                    "summary": content,
                    "tags": "",
                    "main_topic": "",
                    "key_points": "",
                    "sentiment": ""
                }
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"API request failed. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"API request failed after {max_retries} attempts: {str(e)}")
                return {
                    "logline": "",
                    "summary": "",
                    "tags": "",
                    "main_topic": "",
                    "key_points": "",
                    "sentiment": ""
                }
    return {}


def process_video(video: Dict[str, Any], persona: Dict[str, Any]) -> Dict[str, Any]:
    transcript = video.get('transcript', '')
    perplexity_result = process_with_perplexity(transcript, persona)
    
    # Update the video dictionary with new information
    video.update({
        'logline': perplexity_result.get('logline', ''),
        'summary': perplexity_result.get('summary', ''),
        'tags': perplexity_result.get('tags', ''),
        'main_topic': perplexity_result.get('main_topic', ''),
        'key_points': perplexity_result.get('key_points', ''),
        'sentiment': perplexity_result.get('sentiment', ''),
    })
    
    print(f"Processed video: {video.get('vid', 'Unknown ID')}")
    return video
