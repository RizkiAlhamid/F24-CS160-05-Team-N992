import json
from pathlib import Path
from app.lib.credentials import PERPLEXITY_API_KEY
import requests
import time
from app.lib.logging import logging

DATA_PATH = Path("./data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir(exist_ok=True)

# Perplexity API endpoint
API_URL = "https://api.perplexity.ai/chat/completions"


def summarize_articles(input_file, persona: dict):
    if not Path(input_file).exists():
        logging.error(f"Input file '{input_file}' not found.")
        return

    # read the json in input file
    try:
        with open(input_file, "r") as f:
            articles = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from '{input_file}': {e}")
        return

    # Ensure the file contains a list of articles
    if not isinstance(articles, list):
        logging.error(f"Input file '{input_file}' must contain a list of articles.")
        return

    # process each article 
    for article in articles:
        content = article.get("content", {}).get("full_text", "")
        title = article.get("metadata", {}).get("title", "untitled").replace(" ", "_")

        if not content:
            logging.warning(f"No content found for article titled '{title}'. Skipping.")
            continue

        prompt = f"""
            You are {persona}. Summarize the following article for your audience:
            {content}
            """

        try:
            result = process_with_perplexity(prompt)
        except Exception as e:
            logging.error(f"Error processing article '{title}': {e}")
            continue
        # Add the summary back to the article
        article["summary"] = result

        # Save summarized article
        output_path = DATA_PATH / f"{title}.json"
        save_summarized_article(article, output_path)

    logging.info("All articles processed.")


def process_with_perplexity(prompt, max_retries=3, delay=5):
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "Format your response as a summary based of your persona."},
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


def save_summarized_article(article, output_path):
    """Save articles to a JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(article, file, ensure_ascii=False, indent=2)
        logging.info(f"Saved summarized article to {output_path}")
    except Exception as e:
        logging.error(f"Error saving article to {output_path}: {e}")
