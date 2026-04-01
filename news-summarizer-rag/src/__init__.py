"""News Summarizer RAG Application"""

__version__ = "1.0.0"
__author__ = "News Summarizer Team"

# Import main modules for easy access
from .news_fetcher import NewsFetcher
from .summarizer import NewsSummarizer, SimpleRAG
from .user_profiles import UserPreferences
from .notifier import Notifier

__all__ = [
    'NewsFetcher',
    'NewsSummarizer', 
    'SimpleRAG',
    'UserPreferences',
    'Notifier'
]