# test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Testing environment variables...")
print(f"✅ NEWS_API_KEY: {os.getenv('NEWS_API_KEY')[:10]}...")
print(f"✅ GUARDIAN_API_KEY: {os.getenv('GUARDIAN_API_KEY')[:10]}...")
print(f"✅ REDIS_URL: {os.getenv('REDIS_URL')[:50]}...")
print(f"✅ SUMMARIZATION_MODEL: {os.getenv('SUMMARIZATION_MODEL')}")
print(f"✅ DEBUG mode: {os.getenv('DEBUG')}")

# Test NewsAPI connection
import requests

news_key = os.getenv('NEWS_API_KEY')
if news_key:
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}"
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ NewsAPI connection successful!")
    else:
        print(f"❌ NewsAPI error: {response.status_code}")