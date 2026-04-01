import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import DATA_DIR, ENABLE_PERSONALIZATION, MAX_USER_INTERESTS, DEFAULT_USER_INTERESTS
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from src.config.settings import DATA_DIR, ENABLE_PERSONALIZATION, MAX_USER_INTERESTS, DEFAULT_USER_INTERESTS

class UserPreferences:
    def __init__(self):
        self.users_file = DATA_DIR / "users.json"
        self.history_file = DATA_DIR / "history.json"
        self._load_data()
    
    def _load_data(self):
        """Load data from JSON files"""
        self.users = {}
        self.history = {}
        
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = {}
    
    def _save_data(self):
        """Save data to JSON files"""
        os.makedirs(DATA_DIR, exist_ok=True)
        
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def create_user(self, user_id: str, name: str, interests: List[str] = None) -> bool:
        """Create a new user profile"""
        if user_id in self.users:
            print(f"⚠️ User {user_id} already exists")
            return False
        
        if interests is None:
            interests = DEFAULT_USER_INTERESTS.copy()
        
        # Limit number of interests
        interests = interests[:MAX_USER_INTERESTS]
        
        self.users[user_id] = {
            'name': name,
            'interests': interests,
            'created_at': datetime.now().isoformat(),
            'notification_enabled': True,
            'preferences': {
                'auto_summarize': True,
                'summary_length': 'medium',  # short, medium, long
                'sources': ['NewsAPI', 'Guardian']
            }
        }
        self.history[user_id] = []
        self._save_data()
        print(f"✅ User '{name}' created with interests: {interests}")
        return True
    
    def update_interests(self, user_id: str, new_interests: List[str]) -> bool:
        """Update user's interests"""
        if user_id not in self.users:
            print(f"❌ User {user_id} not found")
            return False
        
        # Limit number of interests
        new_interests = new_interests[:MAX_USER_INTERESTS]
        
        self.users[user_id]['interests'] = new_interests
        self._save_data()
        print(f"✅ Updated interests for {self.users[user_id]['name']}: {new_interests}")
        return True
    
    def get_user_interests(self, user_id: str) -> List[str]:
        """Get user's preferred topics"""
        if not ENABLE_PERSONALIZATION:
            return DEFAULT_USER_INTERESTS
        
        if user_id in self.users:
            return self.users[user_id].get('interests', DEFAULT_USER_INTERESTS)
        return DEFAULT_USER_INTERESTS
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get all user preferences"""
        if user_id in self.users:
            return self.users[user_id].get('preferences', {})
        return {}
    
    def update_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences"""
        if user_id not in self.users:
            return False
        
        if 'preferences' not in self.users[user_id]:
            self.users[user_id]['preferences'] = {}
        
        self.users[user_id]['preferences'].update(preferences)
        self._save_data()
        return True
    
    def mark_seen(self, user_id: str, article_id: str, article_title: str):
        """Track which articles user has seen"""
        if user_id not in self.history:
            self.history[user_id] = []
        
        # Check if already seen
        if not any(h['id'] == article_id for h in self.history[user_id]):
            self.history[user_id].append({
                'id': article_id,
                'title': article_title,
                'seen_at': datetime.now().isoformat()
            })
            
            # Keep only last 500 items
            if len(self.history[user_id]) > 500:
                self.history[user_id] = self.history[user_id][-500:]
            
            self._save_data()
    
    def has_seen(self, user_id: str, article_id: str) -> bool:
        """Check if user has seen this article"""
        if user_id in self.history:
            return any(h['id'] == article_id for h in self.history[user_id])
        return False
    
    def filter_by_interests(self, articles: List[Dict], user_id: str) -> List[Dict]:
        """Filter articles based on user's interests"""
        if not ENABLE_PERSONALIZATION:
            return articles
        
        interests = self.get_user_interests(user_id)
        if not interests:
            return articles
        
        filtered = []
        for article in articles:
            # Check if article matches any interest
            title_lower = article.get('title', '').lower()
            desc_lower = article.get('description', '').lower()
            category = article.get('category', '').lower()
            
            for interest in interests:
                interest_lower = interest.lower()
                if (interest_lower in title_lower or 
                    interest_lower in desc_lower or 
                    interest_lower == category):
                    filtered.append(article)
                    break
        
        print(f"📊 Filtered {len(filtered)} articles from {len(articles)} based on interests: {interests}")
        return filtered
    
    def get_seen_articles(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get recently seen articles"""
        if user_id not in self.history:
            return []
        
        return self.history[user_id][-limit:]
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user profile"""
        if user_id in self.users:
            del self.users[user_id]
        if user_id in self.history:
            del self.history[user_id]
        self._save_data()
        print(f"✅ User {user_id} deleted")
        return True