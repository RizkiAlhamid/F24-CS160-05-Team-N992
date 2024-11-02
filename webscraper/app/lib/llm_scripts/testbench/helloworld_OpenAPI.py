import requests
import os
import time
from app.lib.credentials import PERPLEXITY_API_KEY
from pathlib import Path


DATA_PATH = Path("./data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir(exist_ok=True)

# Perplexity API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"


def process_with_perplexity(prompt, max_retries=3, delay=5):
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instruct",  # This is a smaller model, adjust as needed
        "messages": [
            {"role": "system", "content": "Format your response as a JSON object with the following keys: logline, summary, tags, main_topic, key_points, sentiment"},
            {"role": "user", "content": prompt}
        ]
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            if "429" in str(e):  # Rate limit error
                if attempt < max_retries - 1:
                    print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Rate limit error after {max_retries} attempts: {str(e)}")
                    return f"Error: Rate limit exceeded. Please try again later."
            else:
                print(f"An error occurred: {str(e)}")
                return f"Error: {str(e)}"


def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            prompt = line.strip()
            if prompt:
                response = process_with_perplexity(prompt)
                outfile.write(f"Input: {prompt}\nOutput: {response}\n\n")
                print(response)


# Main execution
input_file = 'input.txt'
output_file = 'output.txt'


if not os.path.exists(input_file):
    print(f"Error: Input file '{input_file}' not found.")
else:
    process_file(input_file, output_file)
    print(f"Processing complete. Results written to {output_file}")
