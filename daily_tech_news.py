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
    "ai": ["🤖", "🧠", "⚡"],
    "artificial intelligence": ["🤖", "🧠"],
    "robot": ["🤖", "🦾"],
    "tech": ["💻", "📡", "🖥️"],
    "software": ["💻", "🛠️"],
    "hardware": ["🖥️", "⌨️", "🖱️"],
    "startup": ["🚀", "🌱"],
    "innovation": ["💡", "✨"],
    "gadget": ["📱", "⌚"],
    "mobile": ["📱", "📶"],
    "phone": ["📱"],
    "apple": ["🍎", "📱"],
    "google": ["🔍", "🌐"],
    "microsoft": ["🪟", "💻"],
    "amazon": ["🛒", "📦"],
    "space": ["🌌", "🛰️", "🚀"],
    "science": ["🔬", "🧪"],
    "internet": ["🌐", "📡"],
    "security": ["🔒", "🛡️"],
    "cyber": ["🛡️", "💻"],
    "blockchain": ["⛓️", "📊"],
    "crypto": ["💰", "🪙"],
    "bitcoin": ["🪙", "₿"]
}

def log_message(message):
    with open(LOG_FILE, 'a', encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def fetch_tech_news(retries=3):
    page = random.randint(1, 5)  # Get random news page
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
                time.sleep(5 * (attempt + 1))
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

def pick_emoji(text):
    for key, emojis in EMOJI_MAP.items():
        if key in text.lower():
            return random.choice(emojis)
    return random.choice(["📰", "✨", "🔥", "⚡", "🌐"])  # fallback emojis

def format_post(article):
    title = article.get('title', 'No title')
    description = article.get('description', '')
    snippet = truncate_text(f"{title} - {description}", 200)
    url = article.get('url', '')
    image_url = article.get('urlToImage', None)

    emoji = pick_emoji(snippet)
    hashtags = extract_hashtags(snippet)

    post = f"{emoji} {snippet}\n🔗 {url}\n{hashtags}"
    return post, image_url

def post_to_x(text, image_url=None, retries=3):
    client = tweepy.Client(
        bearer_token=X_BEARER_TOKEN,
        consumer_key=X_API_KEY,
        consumer_secret=X_API_KEY_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET
    )
    for attempt in range(retries):
        try:
            if image_url:
                # Download image and upload to Twitter
                img_data = requests.get(image_url, timeout=10).content
                with open("temp.jpg", "wb") as f:
                    f.write(img_data)

                auth = tweepy.OAuth1UserHandler(
                    X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
                )
                api = tweepy.API(auth)
                media = api.media_upload("temp.jpg")
                response = client.create_tweet(text=text, media_ids=[media.media_id])
            else:
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
        random.shuffle(articles)  # pick random article to vary content
        article = articles[0]  
        post_text, image_url = format_post(article)
        post_to_x(post_text, image_url=image_url)
    else:
        log_message("No news fetched; no post made.")
