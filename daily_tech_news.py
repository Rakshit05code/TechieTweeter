import os
import requests
import tweepy
import time
import random
import re
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / 'tech_news_log.txt'
load_dotenv(BASE_DIR / '.env')

# API keys (set these in your .env file)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
X_API_KEY = os.getenv('X_API_KEY')
X_API_KEY_SECRET = os.getenv('X_API_KEY_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')

# Emoji mapping for common tech keywords
EMOJI_MAP = {
    "ai": "🤖",
    "artificial intelligence": "🤖",
    "robot": "🤖",
    "tech": "💻",
    "software": "💻",
    "hardware": "🖥️",
    "startup": "🚀",
    "innovation": "💡",
    "gadget": "📱",
    "mobile": "📱",
    "phone": "📱",
    "apple": "🍎",
    "google": "🔍",
    "microsoft": "🪟",
    "amazon": "🛒",
    "space": "🌌",
    "science": "🔬",
    "internet": "🌐",
    "security": "🔒",
    "cyber": "🛡️",
    "blockchain": "⛓️",
    "crypto": "💰",
    "bitcoin": "🪙",
}

def log_message(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def fetch_tech_news(retries=3):
    # Shuffle page to get random news (NewsAPI has multiple pages)
    page = random.randint(1, 5)
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={NEWS_API_KEY}&pageSize=10&page={page}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data['status'] != 'ok':
                raise ValueError(f"News API error: {data.get('message')}")
            return data['articles']
        except Exception as e:
            log_message(f"Error fetching news (attempt {attempt+1}/{retries}): {str(e)}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))  # Exponential backoff
    log_message("Failed to fetch news after retries. Skipping post.")
    return None

def truncate_text(text, max_length):
    if len(text) <= max_length:
        return text
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    if last_space == -1:
        return truncated + '...'
    return truncated[:last_space] + '...'

def extract_hashtags(text, max_tags=3):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = {"the", "and", "for", "with", "from", "about", "this", "that", "new", "latest", "today"}
    keywords = [w for w in words if w not in stopwords]
    hashtags = []
    for w in keywords:
        tag = f"#{w.capitalize()}"
        if tag not in hashtags:
            hashtags.append(tag)
        if len(hashtags) >= max_tags:
            break
    return " ".join(hashtags)

def format_post(articles):
    post = "📰 Daily Tech News:\n"
    random.shuffle(articles)  # Shuffle so you don’t always get same ordering
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'No title')
        description = article.get('description', '')
        snippet = truncate_text(f"{title} - {description}", 200)
        url = article.get('url', '')

        # Pick an emoji based on keywords
        emoji = "📰"
        for key, em in EMOJI_MAP.items():
            if key in snippet.lower():
                emoji = em
                break

        # Generate hashtags dynamically
        hashtags = extract_hashtags(snippet)

        line = f"{i}️⃣ {emoji} {snippet} 🔗 {url} {hashtags}\n"
        if len(post + line) > 280:
            break
        post += line

    return post.strip()

def post_to_x(text, retries=3):
    client = tweepy.Client(
        bearer_token=X_BEARER_TOKEN,
        consumer_key=X_API_KEY,
        consumer_secret=X_API_KEY_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET
    )
    for attempt in range(retries):
        try:
            response = client.create_tweet(text=text)
            log_message(f"Tweet posted: {response.data['id']}")
            return True
        except Exception as e:
            log_message(f"Error posting to X (attempt {attempt+1}/{retries}): {str(e)}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
    log_message("Failed to post after retries.")
    return False

if __name__ == "__main__":
    articles = fetch_tech_news()
    if articles:
        post_text = format_post(articles)
        post_to_x(post_text)
    else:
        log_message("No news fetched; no post made.")
