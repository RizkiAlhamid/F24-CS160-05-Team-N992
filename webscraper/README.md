# BBC News Environmental Article Scraper

This project consists of two Python scripts that work together to scrape BBC News articles and filter them for environmental content. It's designed to help researchers and analysts gather data on environmental news coverage from BBC.

## Components

1. `harpy.py`: A web scraper for BBC News articles.
2. `eaf.py`: An environmental article filter.

## Features

- Scrapes BBC News articles from a given starting URL
- Respects rate limiting to avoid overloading the BBC website
- Filters scraped articles for environmental content
- Extracts and counts environmental keywords from articles
- Saves both raw scraped data and filtered environmental articles as JSON files

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4
  - ratelimit

You can install the required packages using:
`pip install requests beautifulsoup4 ratelimit`

## Usage

### Step 1: Scrape BBC News Articles

Run the `harpy.py` script to scrape BBC News articles:

Example: python harpy.py https://www.bbc.com/news --max_pages 100 --output scraped_bbc_articles.json

Arguments:
- `start_url`: The starting URL for the web scraper (https://www.bbc.com/news)
- `--max_pages`: (Optional) Maximum number of pages to scrape
- `--output`: (Optional) Output JSON file name (default: scraped_bbc_articles.json)

### Step 2: Filter Environmental Articles

After scraping, use the `eaf.py` script to filter the articles for environmental content:

python eaf.py

This will read the `scraped_bbc_articles.json` file and produce an `environment.json` file containing only the environmental articles.

## Output

- `scraped_bbc_articles.json`: Contains all scraped BBC News articles.
- `environment.json`: Contains only the articles identified as environmental, with added environmental keyword data.

## Customization

You can modify the `ENVIRONMENTAL_KEYWORDS` list in `eaf.py` to adjust the criteria for identifying environmental articles.
