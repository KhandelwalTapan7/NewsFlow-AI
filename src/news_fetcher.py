import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import hashlib
import time

class NewsFetcher:
    def __init__(self):
        # Load API keys from environment
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.guardian_api_key = os.getenv('GUARDIAN_API_KEY')
        self.newsdata_io_key = os.getenv('NEWSDATA_IO_API_KEY')
        self.world_news_key = os.getenv('WORLD_NEWS_API_KEY')
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'NewsSummarizer/1.0'})
        
        print(f"\n📡 News Sources Configured:")
        print(f"  ✅ NewsAPI: {'Yes' if self.news_api_key else 'No'}")
        print(f"  ✅ Guardian: {'Yes' if self.guardian_api_key else 'No'}")
        print(f"  ✅ NewsData.io: {'Yes' if self.newsdata_io_key else 'No'}")
        print(f"  ✅ World News: {'Yes' if self.world_news_key else 'No'}")
    
    def fetch_from_newsapi(self, category: Optional[str] = None, page_size: int = 15) -> List[Dict]:
        """Fetch articles from NewsAPI"""
        if not self.news_api_key:
            return []
            
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': 'us',
            'apiKey': self.news_api_key,
            'pageSize': page_size
        }
        
        if category and category != 'general':
            params['category'] = category
            
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', []):
                    if article.get('title') and article.get('description'):
                        articles.append(self._normalize_article(article, 'NewsAPI'))
                return articles
        except Exception as e:
            print(f"  ⚠️ NewsAPI error: {e}")
        return []
    
    def fetch_from_guardian(self, section: Optional[str] = None, page_size: int = 15) -> List[Dict]:
        """Fetch articles from The Guardian API"""
        if not self.guardian_api_key:
            return []
            
        url = "https://content.guardianapis.com/search"
        params = {
            'api-key': self.guardian_api_key,
            'page-size': page_size,
            'show-fields': 'headline,bodyText,trailText,thumbnail',
            'order-by': 'newest'
        }
        
        if section:
            params['section'] = section
            
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for result in data.get('response', {}).get('results', []):
                    fields = result.get('fields', {})
                    article = {
                        'title': fields.get('headline', result.get('webTitle', '')),
                        'description': fields.get('trailText', ''),
                        'content': fields.get('bodyText', '')[:2000],
                        'url': result.get('webUrl', ''),
                        'source': 'The Guardian',
                        'published_at': result.get('webPublicationDate', ''),
                        'category': result.get('sectionName', 'general').lower()
                    }
                    if article['title'] and article['description']:
                        articles.append(self._normalize_article(article, 'Guardian'))
                return articles
        except Exception as e:
            print(f"  ⚠️ Guardian error: {e}")
        return []
    
    def fetch_from_newsdata_io(self, category: Optional[str] = None, page_size: int = 15) -> List[Dict]:
        """Fetch articles from NewsData.io API"""
        if not self.newsdata_io_key:
            return []
            
        url = "https://newsdata.io/api/1/news"
        params = {
            'apikey': self.newsdata_io_key,
            'country': 'us',
            'size': page_size,
            'language': 'en'
        }
        
        if category and category != 'general':
            params['category'] = category
            
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    articles = []
                    for article in data.get('results', []):
                        normalized = {
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'content': article.get('content', '') or article.get('description', ''),
                            'url': article.get('link', ''),
                            'source': article.get('source_id', 'NewsData.io'),
                            'published_at': article.get('pubDate', ''),
                            'category': article.get('category', ['general'])[0] if article.get('category') else 'general'
                        }
                        if normalized['title'] and normalized['description']:
                            articles.append(self._normalize_article(normalized, 'NewsData.io'))
                    return articles
        except Exception as e:
            print(f"  ⚠️ NewsData.io error: {e}")
        return []
    
    def fetch_from_world_news_api(self, category: Optional[str] = None, page_size: int = 15) -> List[Dict]:
        """Fetch articles from World News API"""
        if not self.world_news_key:
            return []
            
        url = "https://api.worldnewsapi.com/search-news"
        params = {
            'api-key': self.world_news_key,
            'number': page_size,
            'language': 'en',
            'sort': 'publish-time',
            'sort-direction': 'DESC'
        }
        
        if category and category != 'general':
            params['source-country'] = 'us'
            
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('news', []):
                    normalized = {
                        'title': article.get('title', ''),
                        'description': article.get('summary', '') or article.get('text', ''),
                        'content': article.get('text', '')[:2000],
                        'url': article.get('url', ''),
                        'source': article.get('source', 'World News'),
                        'published_at': article.get('published_date', ''),
                        'category': category or 'general'
                    }
                    if normalized['title'] and normalized['description']:
                        articles.append(self._normalize_article(normalized, 'World News API'))
                return articles
        except Exception as e:
            print(f"  ⚠️ World News API error: {e}")
        return []
    
    def fetch_all_news(self, category: Optional[str] = None, page_size: int = 20) -> List[Dict]:
        """Fetch news from ALL configured sources"""
        all_articles = []
        
        print(f"\n🔍 Fetching news from all sources...")
        
        # Fetch from each source
        sources = [
            ('NewsAPI', self.fetch_from_newsapi),
            ('Guardian', self.fetch_from_guardian),
            ('NewsData.io', self.fetch_from_newsdata_io),
            ('World News', self.fetch_from_world_news_api)
        ]
        
        for name, fetch_func in sources:
            try:
                articles = fetch_func(category, page_size)
                if articles:
                    all_articles.extend(articles)
                    print(f"  ✅ {name}: {len(articles)} articles")
                else:
                    print(f"  ⚠️ {name}: No articles")
            except Exception as e:
                print(f"  ❌ {name}: Error - {e}")
        
        # Remove duplicates based on title similarity
        unique_articles = []
        seen_titles = set()
        
        for article in all_articles:
            title_lower = article['title'].lower()
            # Check if similar title exists
            similar = False
            for seen_title in seen_titles:
                if self._is_similar(title_lower, seen_title):
                    similar = True
                    break
            if not similar:
                seen_titles.add(title_lower)
                unique_articles.append(article)
        
        print(f"\n📊 Total: {len(unique_articles)} unique articles from {len(all_articles)} raw")
        return unique_articles[:page_size * 2]
    
    def search_by_topic(self, query: str, days_back: int = 7, page_size: int = 20) -> List[Dict]:
        """Search across ALL sources"""
        all_articles = []
        
        print(f"\n🔎 Searching for '{query}' across all sources...")
        
        # Search in NewsAPI
        if self.news_api_key:
            try:
                url = "https://newsapi.org/v2/everything"
                from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
                params = {
                    'q': query,
                    'from': from_date,
                    'sortBy': 'relevancy',
                    'apiKey': self.news_api_key,
                    'pageSize': page_size,
                    'language': 'en'
                }
                response = self.session.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for article in data.get('articles', []):
                        if article.get('title') and article.get('description'):
                            all_articles.append(self._normalize_article(article, 'NewsAPI'))
                    print(f"  ✅ NewsAPI: {len(data.get('articles', []))} results")
            except Exception as e:
                print(f"  ⚠️ NewsAPI search error: {e}")
        
        # Search in Guardian
        if self.guardian_api_key:
            try:
                url = "https://content.guardianapis.com/search"
                params = {
                    'q': query,
                    'api-key': self.guardian_api_key,
                    'page-size': page_size,
                    'show-fields': 'headline,bodyText,trailText',
                    'order-by': 'relevance'
                }
                response = self.session.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for result in data.get('response', {}).get('results', []):
                        fields = result.get('fields', {})
                        article = {
                            'title': fields.get('headline', result.get('webTitle', '')),
                            'description': fields.get('trailText', ''),
                            'content': fields.get('bodyText', '')[:2000],
                            'url': result.get('webUrl', ''),
                            'source': 'The Guardian',
                            'published_at': result.get('webPublicationDate', '')
                        }
                        if article['title'] and article['description']:
                            all_articles.append(self._normalize_article(article, 'Guardian'))
                    print(f"  ✅ Guardian: {len(data.get('response', {}).get('results', []))} results")
            except Exception as e:
                print(f"  ⚠️ Guardian search error: {e}")
        
        # Remove duplicates
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        print(f"\n📊 Found {len(unique_articles)} unique articles")
        return unique_articles[:page_size]
    
    def _normalize_article(self, article: Dict, source: str) -> Dict:
        """Normalize article format"""
        article_id = hashlib.md5(
            f"{article.get('url', '')}{article.get('title', '')}".encode()
        ).hexdigest()
        
        content = article.get('content') or article.get('description', '')
        if content and len(content) > 500:
            content = content[:500] + "..."
        
        category = self._categorize_article(article)
        
        return {
            'id': article_id,
            'title': article.get('title', 'No title'),
            'description': article.get('description', ''),
            'content': content,
            'url': article.get('url', ''),
            'source': source,
            'published_at': article.get('published_at') or article.get('publishedAt', ''),
            'category': category,
            'fetched_at': datetime.now().isoformat()
        }
    
    def _categorize_article(self, article: Dict) -> str:
        """Categorize article based on keywords"""
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        text = f"{title} {description}"
        
        categories = {
            'technology': ['tech', 'ai', 'software', 'app', 'digital', 'computer', 'data', 'algorithm'],
            'politics': ['election', 'government', 'congress', 'president', 'minister', 'vote', 'policy'],
            'business': ['stock', 'market', 'economy', 'business', 'company', 'finance', 'investment'],
            'health': ['health', 'covid', 'vaccine', 'medical', 'hospital', 'disease', 'treatment'],
            'sports': ['sport', 'football', 'basketball', 'soccer', 'tennis', 'cricket', 'match'],
            'science': ['science', 'research', 'study', 'discovery', 'space', 'climate', 'environment'],
            'entertainment': ['movie', 'film', 'music', 'celebrity', 'hollywood', 'entertainment']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        return 'general'
    
    def _is_similar(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Check if two titles are similar"""
        words1 = set(title1.split())
        words2 = set(title2.split())
        if not words1 or not words2:
            return False
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union > threshold