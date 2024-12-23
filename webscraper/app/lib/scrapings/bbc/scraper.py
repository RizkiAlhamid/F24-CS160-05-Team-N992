import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import math
import time
import logging
from ratelimit import limits, sleep_and_retry
from collections import deque
from pathlib import Path
from app.lib.logging import logging


DATA_PATH = Path("./data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir(exist_ok=True)


def is_valid_url(url):
    """Check if a URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def is_bbc_news_article(url):
    """Check if the URL is a BBC News article with the specific structure."""
    return url.startswith("https://www.bbc.com/news/articles/")


@sleep_and_retry
@limits(calls=5, period=1)  # Rate limit: 5 requests per second
def fetch_url(url):
    """Fetch URL content with rate limiting and retries."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None


def collect_hyperlinks(url):
    """Collect all hyperlinks from the given URL that match BBC News article format."""
    content = fetch_url(url)
    if not content:
        return []

    soup = BeautifulSoup(content, 'html.parser')
    
    links = []
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(url, a_tag['href'])
        if is_valid_url(link) and link.startswith("https://www.bbc.com/news/"):
            links.append(link)
    
    return list(set(links))  # Remove duplicates


def extract_page_info(soup, url):
    """Extract information from a BBC News article page."""
    page_info = {
        "url": url,
        "metadata": {
            "title": "",
            "author": "",
            "publication_date": "",
            "last_modified_date": "",
            "tags": [],
            "categories": []
        },
        "content": {
            "full_text": "",
            "paragraphs": [],
            "word_count": 0
        },
        "analytics": {
            "reading_time_minutes": 0
        }
    }

    # Extract title
    title_tag = soup.find('h1')
    if title_tag:
        page_info['metadata']['title'] = title_tag.get_text(strip=True)

    # Extract author
    author_tag = soup.find('div', class_='ssrcss-68pt20-Text-TextContributorName')
    if author_tag:
        page_info['metadata']['author'] = author_tag.get_text(strip=True)

    # Extract publication date
    time_tag = soup.find('time')
    if time_tag and 'datetime' in time_tag.attrs:
        page_info['metadata']['publication_date'] = time_tag['datetime']

    # Extract content
    content_div = soup.find('article')
    if content_div:
        paragraphs = content_div.find_all(['p', 'h2'])
        page_info['content']['paragraphs'] = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        page_info['content']['full_text'] = ' '.join(page_info['content']['paragraphs'])

    # Calculate word count
    page_info['content']['word_count'] = len(page_info['content']['full_text'].split())

    # Calculate reading time (assuming average reading speed of 200 words per minute)
    page_info['analytics']['reading_time_minutes'] = math.ceil(page_info['content']['word_count'] / 200)

    return page_info


def scrape_page(url):
    """Scrape a single BBC News article page."""
    content = fetch_url(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')
    return extract_page_info(soup, url)


def scrape_pages(start_url, max_pages=None):
    """Main web scraping function for BBC News articles."""
    scraped_pages = []
    visited_urls = set()
    urls_to_visit = deque([start_url])
    
    while urls_to_visit and (max_pages is None or len(scraped_pages) < max_pages):
        current_url = urls_to_visit.popleft()
        
        if current_url in visited_urls:
            continue
        
        visited_urls.add(current_url)
        
        # Collect links from the current page
        new_links = collect_hyperlinks(current_url)
        for link in new_links:
            if link not in visited_urls and link not in urls_to_visit:
                urls_to_visit.append(link)
        
        # If it's an article page, scrape it
        if is_bbc_news_article(current_url):
            page_info = scrape_page(current_url)
            if page_info:
                scraped_pages.append(page_info)
                logging.info(f"Scraped article: {current_url} ({len(scraped_pages)}/{max_pages if max_pages else 'unlimited'})")
        
        if len(scraped_pages) % 10 == 0:
            logging.info(f"Progress: {len(scraped_pages)} articles scraped, {len(urls_to_visit)} URLs in queue")

    return scraped_pages


def save_to_json(scraped_pages, output_file_path: Path):
    """Save scraped information to a JSON file."""
    try:
        # Ensure the directory exists
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON data to file
        with output_file_path.open('w', encoding='utf-8') as jsonfile:
            json.dump(scraped_pages, jsonfile, ensure_ascii=False, indent=2)
        
        logging.info(f"Scraped articles saved to {output_file_path}")
    except IOError as e:
        logging.error(f"Error saving scraped articles to {output_file_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while saving scraped articles: {repr(e)}")
        logging.exception("Exception details:")


def bbc_scraper(start_url, max_pages, output_file_path) -> Path:
    if output_file_path is None:
        output_file_path = DATA_PATH / "scraped_bbc_articles.json"

    start_time = time.time()
    scraped_pages = scrape_pages(start_url, max_pages)
    
    logging.info(f"Total articles scraped: {len(scraped_pages)}")
    logging.info(f"Time taken: {time.time() - start_time:.2f} seconds")

    # Save scraped pages to JSON
    save_to_json(scraped_pages, output_file_path)
    return output_file_path

