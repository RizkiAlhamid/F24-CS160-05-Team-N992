import json
import re
from collections import Counter
from pathlib import Path
from app.lib.logging import logging


DATA_PATH = Path("./data")
if not DATA_PATH.exists():
    DATA_PATH.mkdir(exist_ok=True)

# List of environmental keywords
ENVIRONMENTAL_KEYWORDS = [
    "climate change", "global warming", "renewable energy", "sustainability", "carbon emissions",
    "greenhouse gas", "pollution", "conservation", "biodiversity", "recycling", "environmental",
    "ecology", "green energy", "solar power", "wind power", "fossil fuels", "deforestation",
    "ocean acidification", "ozone layer", "eco-friendly", "carbon", "renewable resources",
    "sustainable development", "wildlife conservation", "organic farming", "air quality",
    "water conservation", "energy efficiency", "green technology", "environmental protection",
    "environmental degradation", "climate finance", "greenhouse effect", "carbon trading", "air pollution control",
    "water scarcity", "sustainable consumption", "low-emission development", "alternative energy", 
    "ecological footprint", "green infrastructure", "nature conservation", "sustainable fisheries",
    "energy transition", "environmental regulations", "environmental innovation", "biodiversity protection", 
    "natural capital", "waste-to-energy", "fossil fuel divestment", "environmental footprint analysis", 
    "environmental justice movement", "climate governance", "environmental assessment", "marine biodiversity", 
    "eco-innovation", "habitat restoration", "sustainable transportation", "cultural heritage conservation", 
    "environmental reporting", "ecosystem degradation", "responsible tourism", "biodiversity hotspots", 
    "greenhouse gas inventory", "clean air", "environmental stewardship", "green bonds", "climate vulnerability", 
    "sustainable water management", "carbon-neutral technology", "environmental hazards", "natural climate solutions", 
    "land use change", "sustainable energy", "environmental remediation", "disaster resilience", 
    "flood mitigation", "land conservation", "carbon pricing", "eco-certification", "climate-smart agriculture", 
    "environmental audits", "marine ecosystems", "permaculture", "sustainable investment", "water management", 
    "environmental disasters", "green energy transition", "urban resilience", "ecological restoration", 
    "environmental transparency", "sustainable innovation", "carbon emissions reduction", "low-carbon transportation", 
    "zero-emission technologies", "energy independence", "green manufacturing", "conservation policy", 
    "sustainable mining", "sustainable finance", "plastic waste reduction", "environmental NGOs", "environmental subsidies", 
    "biodiversity conservation strategies", "food sustainability", "environmental data", "renewable fuel", 
    "green recovery", "environmental performance", "sustainable infrastructure", "renewable resource management", 
    "smart cities", "biodiversity restoration", "green finance", "sustainable energy development", 
    "environmental certifications", "natural resource management", "eco-design", "environmental accountability"
]


def load_articles(filename):
    """Load articles from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading articles from {filename}: {e}")
        return []


def save_articles(articles, filename):
    """Save articles to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(articles, file, ensure_ascii=False, indent=2)
        logging.info(f"Saved {len(articles)} articles to {filename}")
    except Exception as e:
        logging.error(f"Error saving articles to {filename}: {e}")


def is_environmental_article(article, threshold=1):
    """
    Determine if an article is environmentally themed based on keyword occurrence.
    
    Args:
    article (dict): The article to analyze.
    threshold (int): Minimum number of unique environmental keywords to classify as environmental.

    Returns:
    bool: True if the article is environmental, False otherwise.
    """
    content = article['content']['full_text'].lower()
    
    # Count unique environmental keywords
    keyword_count = sum(1 for keyword in ENVIRONMENTAL_KEYWORDS if keyword in content)
    
    return keyword_count >= threshold


def extract_environmental_keywords(article):
    """
    Extract and count environmental keywords from an article.
    
    Args:
    article (dict): The article to analyze.

    Returns:
    dict: A dictionary of environmental keywords and their counts.
    """
    content = article['content']['full_text'].lower()
    keyword_counts = Counter()
    
    for keyword in ENVIRONMENTAL_KEYWORDS:
        count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content))
        if count > 0:
            keyword_counts[keyword] = count
    
    return dict(keyword_counts)


def filter_environmental_articles(input_file, output_file):
    """
    Filter environmental articles from the input file and save them to the output file.
    
    Args:
    input_file (str): Path to the input JSON file.
    output_file (str): Path to the output JSON file for environmental articles.
    """
    articles = load_articles(input_file)
    environmental_articles = []

    for article in articles:
        if is_environmental_article(article):
            # Add environmental keywords to the article
            article['environmental_keywords'] = extract_environmental_keywords(article)
            environmental_articles.append(article)
            logging.info(f"Environmental article found: {article['metadata']['title']}")

    save_articles(environmental_articles, output_file)


if __name__ == "__main__":
    input_file = "scraped_bbc_articles.json"
    output_file = "environment.json"
    
    logging.info(f"Starting to filter environmental articles from {input_file}")
    filter_environmental_articles(input_file, output_file)
    logging.info("Filtering complete")
