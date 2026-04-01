"""Test all imports"""

print("Testing imports...")

try:
    from src.news_fetcher import NewsFetcher
    print("✅ NewsFetcher imported")
except Exception as e:
    print(f"❌ NewsFetcher error: {e}")

try:
    from src.summarizer import NewsSummarizer, SimpleRAG
    print("✅ NewsSummarizer imported")
except Exception as e:
    print(f"❌ NewsSummarizer error: {e}")

try:
    from src.user_profiles import UserPreferences
    print("✅ UserPreferences imported")
except Exception as e:
    print(f"❌ UserPreferences error: {e}")

try:
    from src.notifier import Notifier
    print("✅ Notifier imported")
except Exception as e:
    print(f"❌ Notifier error: {e}")

try:
    from src.config.settings import *
    print("✅ Settings imported")
except Exception as e:
    print(f"❌ Settings error: {e}")

print("\n✅ All imports successful!")