import re
from datetime import datetime
from typing import List, Dict, Optional
from collections import Counter

def clean_text(text: str) -> str:
    """Clean text by removing extra spaces and special characters"""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\']', '', text)
    return text.strip()

def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract important keywords from text"""
    if not text:
        return []
    
    # Remove punctuation and convert to lowercase
    text = text.lower().translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
    words = text.split()
    
    # Remove common stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
    }
    words = [w for w in words if w not in stopwords and len(w) > 3]
    
    # Get most common words
    word_counts = Counter(words)
    return [word for word, count in word_counts.most_common(max_keywords)]

def format_date(date_string: str) -> str:
    """Format date string to readable format"""
    if not date_string:
        return "Recently"
    
    try:
        # Handle different date formats
        date_string = date_string.replace('Z', '+00:00')
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        try:
            from dateutil import parser
            dt = parser.parse(date_string)
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            return "Recently"

def group_by_category(articles: List[Dict]) -> Dict[str, List[Dict]]:
    """Group articles by category"""
    grouped = {}
    for article in articles:
        category = article.get('category', 'general')
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(article)
    return grouped

def get_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Calculate estimated reading time in minutes"""
    if not text:
        return 0
    word_count = len(text.split())
    return max(1, (word_count + words_per_minute - 1) // words_per_minute)

def remove_duplicates(articles: List[Dict], key: str = 'url') -> List[Dict]:
    """Remove duplicate articles based on a key"""
    seen = set()
    unique = []
    for article in articles:
        value = article.get(key)
        if value and value not in seen:
            seen.add(value)
            unique.append(article)
    return unique

def sort_by_date(articles: List[Dict], reverse: bool = True) -> List[Dict]:
    """Sort articles by publication date"""
    def get_date(article):
        date_str = article.get('published_at', '')
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.min
    
    return sorted(articles, key=get_date, reverse=reverse)