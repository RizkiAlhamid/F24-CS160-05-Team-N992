import json
import argparse
import logging
import os
from dotenv import load_dotenv
import anthropic
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API keys from environment variables

# Initialize API clients
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
openai.api_key = OPENAI_API_KEY

def process_with_claude(text):
    prompt = f"""
    Analyze the following news article and provide:
    1. A logline (a one-sentence summary of the article)
    2. A concise summary (max 3 sentences)
    3. 5 relevant tags
    4. The main topic discussed
    5. Key points (max 5 bullet points)
    6. Sentiment (positive, negative, or neutral)

    Article text:
    {text}

    Format your response as a JSON object with the following keys:
    logline, summary, tags, main_topic, key_points, sentiment
    """

    response = anthropic_client.completions.create(
        model="claude-2.1",
        prompt=prompt,
        max_tokens_to_sample=1000,
    )

    return json.loads(response.completion)

def process_with_openai(text):
    prompt = f"""
    Analyze the following news article and provide:
    1. A logline (a one-sentence summary of the article)
    2. A concise summary (max 3 sentences)
    3. 5 relevant tags
    4. The main topic discussed
    5. Key points (max 5 bullet points)
    6. Sentiment (positive, negative, or neutral)

    Article text:
    {text}

    Format your response as a JSON object with the following keys:
    logline, summary, tags, main_topic, key_points, sentiment
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes news articles."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

def summarize_articles(input_file, output_file, api="claude"):
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    summarized_articles = []

    for article in articles:
        logging.info(f"Processing article: {article['url']}")
        
        if api == "claude":
            llm_analysis = process_with_claude(article['content']['full_text'])
        elif api == "openai":
            llm_analysis = process_with_openai(article['content']['full_text'])
        else:
            raise ValueError("Invalid API choice. Use 'claude' or 'openai'.")

        summarized_article = {
            "url": article['url'],
            "metadata": article['metadata'],
            "analytics": article['analytics'],
            "llm_analysis": llm_analysis
        }

        summarized_articles.append(summarized_article)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summarized_articles, f, ensure_ascii=False, indent=2)

    logging.info(f"Summarized articles saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="LLM Summarizer for BBC News Articles")
    parser.add_argument("input_file", help="Input JSON file containing scraped BBC articles")
    parser.add_argument("output_file", help="Output JSON file for summarized articles")
    parser.add_argument("--api", choices=["claude", "openai"], default="claude", help="Choose the API to use for summarization (default: claude)")

    args = parser.parse_args()

    summarize_articles(args.input_file, args.output_file, args.api)

if __name__ == "__main__":
    main()
