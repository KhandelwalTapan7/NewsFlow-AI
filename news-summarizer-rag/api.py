import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uvicorn
import hashlib
import jwt
import secrets

# Import your modules
from src.news_fetcher import NewsFetcher
from src.summarizer import NewsSummarizer, SimpleRAG
from src.user_profiles import UserPreferences
from src.config.settings import RAG_ENABLED, DEBUG

# JWT Configuration
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Initialize FastAPI app
app = FastAPI(
    title="News Summarizer API",
    description="Real-time News Summarizer with RAG - Aggregates from 4 News Sources",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"  # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
print("\n" + "="*60)
print("📡 Initializing News Summarizer API")
print("="*60)

fetcher = NewsFetcher()
summarizer = NewsSummarizer()
rag = SimpleRAG() if RAG_ENABLED else None
users = UserPreferences()

print("\n✅ API Ready!")
print("="*60 + "\n")

# ============================================
# Category Keywords for Better Filtering
# ============================================

CATEGORY_KEYWORDS = {
    'sports': [
        'sport', 'football', 'basketball', 'soccer', 'tennis', 'cricket', 'baseball',
        'nba', 'nfl', 'mlb', 'nhl', 'olympic', 'athlete', 'match', 'tournament',
        'world cup', 'championship', 'premier league', 'la liga', 'serie a',
        'bundesliga', 'super bowl', 'world series', 'stanley cup', 'grand slam'
    ],
    'technology': [
        'tech', 'ai', 'artificial intelligence', 'software', 'app', 'digital',
        'computer', 'data', 'algorithm', 'startup', 'coding', 'programming',
        'internet', 'cyber', 'gadget', 'smartphone', 'iphone', 'android'
    ],
    'politics': [
        'election', 'government', 'congress', 'senate', 'president', 'minister',
        'prime minister', 'vote', 'policy', 'political', 'parliament', 'democracy'
    ],
    'business': [
        'stock', 'market', 'economy', 'business', 'company', 'startup', 'finance',
        'investment', 'profit', 'revenue', 'banking', 'corporate', 'ceo'
    ],
    'health': [
        'health', 'medical', 'covid', 'vaccine', 'hospital', 'disease', 'treatment',
        'virus', 'pandemic', 'doctor', 'medicine', 'fitness', 'wellness'
    ],
    'science': [
        'science', 'research', 'study', 'scientist', 'discovery', 'space', 'climate',
        'environment', 'physics', 'biology', 'chemistry', 'astronomy', 'nasa'
    ],
    'entertainment': [
        'movie', 'film', 'music', 'celebrity', 'hollywood', 'bollywood', 'entertainment',
        'actor', 'actress', 'streaming', 'netflix', 'disney', 'spotify'
    ]
}

# ============================================
# Helper Functions
# ============================================

def filter_articles_by_category(articles: List[Dict], category: str) -> List[Dict]:
    """Filter articles by category using keywords"""
    if not articles:
        return []
    
    category_lower = category.lower()
    keywords = CATEGORY_KEYWORDS.get(category_lower, [category_lower])
    
    filtered = []
    
    for article in articles:
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        article_category = article.get('category', '').lower()
        
        is_match = False
        
        if article_category == category_lower:
            is_match = True
        
        if not is_match:
            text = f"{title} {description}"
            for keyword in keywords:
                if keyword in text:
                    is_match = True
                    break
        
        if is_match:
            article['category'] = category_lower
            filtered.append(article)
    
    return filtered

# ============================================
# Request/Response Models
# ============================================

class InterestUpdate(BaseModel):
    interests: List[str]

class SummaryRequest(BaseModel):
    article_id: str
    content: str
    user_id: str
    rag_enabled: bool = True

class MarkReadRequest(BaseModel):
    article_id: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    interests: List[str] = []

# ============================================
# Authentication Endpoints
# ============================================

@app.post("/api/v1/auth/signup")
async def signup(request: SignupRequest):
    """User signup"""
    try:
        print(f"\n📝 Signup attempt: {request.email}")
        
        user_id = hashlib.md5(request.email.lower().encode()).hexdigest()
        
        if user_id in users.users:
            print(f"   ❌ User already exists: {request.email}")
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Email already registered"}
            )
        
        hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
        
        users.create_user(user_id, request.name, request.interests)
        
        users.users[user_id]['email'] = request.email.lower()
        users.users[user_id]['password'] = hashed_password
        users.users[user_id]['created_at'] = datetime.now().isoformat()
        
        users._save_data()
        
        token = jwt.encode(
            {
                'user_id': user_id,
                'email': request.email,
                'name': request.name,
                'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
            },
            SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )
        
        print(f"   ✅ User created successfully: {request.name}")
        
        return JSONResponse(content={
            "success": True,
            "token": token,
            "user": {
                "id": user_id,
                "name": request.name,
                "email": request.email,
                "interests": request.interests
            }
        })
    
    except Exception as e:
        print(f"❌ Signup error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/v1/auth/login")
async def login(request: LoginRequest):
    """User login"""
    try:
        print(f"\n🔐 Login attempt: {request.email}")
        
        user_id = hashlib.md5(request.email.lower().encode()).hexdigest()
        
        if user_id not in users.users:
            print(f"   ❌ User not found: {request.email}")
            return JSONResponse(
                status_code=401,
                content={"success": False, "error": "Invalid email or password"}
            )
        
        hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
        stored_password = users.users[user_id].get('password')
        
        if not stored_password or stored_password != hashed_password:
            print(f"   ❌ Invalid password for: {request.email}")
            return JSONResponse(
                status_code=401,
                content={"success": False, "error": "Invalid email or password"}
            )
        
        users.users[user_id]['last_login'] = datetime.now().isoformat()
        users._save_data()
        
        token = jwt.encode(
            {
                'user_id': user_id,
                'email': request.email,
                'name': users.users[user_id].get('name'),
                'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
            },
            SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )
        
        print(f"   ✅ Login successful: {users.users[user_id].get('name')}")
        
        return JSONResponse(content={
            "success": True,
            "token": token,
            "user": {
                "id": user_id,
                "name": users.users[user_id].get('name'),
                "email": request.email,
                "interests": users.users[user_id].get('interests', [])
            }
        })
    
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/v1/auth/verify")
async def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return JSONResponse(content={
            "success": True,
            "valid": True,
            "user": {
                "id": payload.get('user_id'),
                "name": payload.get('name'),
                "email": payload.get('email')
            }
        })
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"success": False, "error": "Token expired"}
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={"success": False, "error": "Invalid token"}
        )

# ============================================
# News Endpoints
# ============================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "News Summarizer API",
        "version": "1.0.0",
        "status": "running",
        "rag_enabled": RAG_ENABLED,
        "sources": ["NewsAPI", "Guardian", "NewsData.io", "World News API"],
        "categories": list(CATEGORY_KEYWORDS.keys()),
        "endpoints": {
            "auth": {
                "signup": "/api/v1/auth/signup",
                "login": "/api/v1/auth/login",
                "verify": "/api/v1/auth/verify"
            },
            "news": {
                "personalized": "/api/v1/news/personalized/{user_id}",
                "all": "/api/v1/news/all",
                "category": "/api/v1/news/category/{category}",
                "search": "/api/v1/news/search?q={query}"
            }
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "rag_enabled": RAG_ENABLED,
        "services": {
            "news_fetcher": "ok",
            "summarizer": "ok",
            "rag": "ok" if rag else "disabled",
            "users": "ok"
        }
    }

@app.get("/api/v1/news/all")
async def get_all_news(category: Optional[str] = None, limit: int = 50):
    """Get news from ALL 4 sources combined"""
    try:
        print(f"\n📰 Fetching news from ALL sources...")
        
        articles = fetcher.fetch_all_news(page_size=limit)
        
        if category and category != 'all':
            print(f"   Filtering by category: {category}")
            articles = filter_articles_by_category(articles, category)
        
        print(f"✅ Total articles: {len(articles)}")
        
        return JSONResponse(content={
            "success": True,
            "articles": articles[:limit],
            "count": len(articles),
            "sources": ["NewsAPI", "Guardian", "NewsData.io", "World News API"],
            "category": category if category else "all",
            "rag_enabled": RAG_ENABLED
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/v1/news/category/{category}")
async def get_news_by_category(category: str, limit: int = 50):
    """Get news by category with proper filtering"""
    try:
        print(f"\n📂 Fetching {category} news from all sources...")
        
        articles = fetcher.fetch_all_news(page_size=limit * 2)
        filtered_articles = filter_articles_by_category(articles, category)
        
        print(f"✅ Found {len(filtered_articles)} {category} articles")
        
        return JSONResponse(content={
            "success": True,
            "articles": filtered_articles[:limit],
            "count": len(filtered_articles),
            "category": category,
            "sources": ["NewsAPI", "Guardian", "NewsData.io", "World News API"],
            "rag_enabled": RAG_ENABLED
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/v1/news/personalized/{user_id}")
async def get_personalized_news(user_id: str, limit: int = 30):
    """Get personalized news based on user interests"""
    try:
        interests = users.get_user_interests(user_id)
        
        if not interests:
            interests = ["technology", "business", "health", "sports"]
        
        print(f"\n🎯 Personalized news for {user_id}")
        print(f"   Interests: {', '.join(interests)}")
        
        all_articles = []
        
        for interest in interests[:4]:
            print(f"   🔍 Searching for '{interest}'...")
            articles = fetcher.search_by_topic(interest, days_back=3, page_size=15)
            filtered = filter_articles_by_category(articles, interest)
            all_articles.extend(filtered)
            print(f"      Found {len(filtered)} relevant articles")
        
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        new_articles = []
        for article in unique_articles[:limit]:
            if not users.has_seen(user_id, article.get('id')):
                new_articles.append(article)
        
        print(f"\n📊 Results: {len(new_articles)} new articles")
        
        return JSONResponse(content={
            "success": True,
            "articles": new_articles,
            "count": len(new_articles),
            "interests": interests,
            "rag_enabled": RAG_ENABLED
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/v1/news/search")
async def search_news(q: str, days: int = 7, limit: int = 30):
    """Search news across ALL sources"""
    try:
        if not q or q.strip() == "":
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Search query cannot be empty"}
            )
        
        print(f"\n🔎 Searching for: '{q}'")
        articles = fetcher.search_by_topic(q, days_back=days, page_size=limit)
        
        return JSONResponse(content={
            "success": True,
            "articles": articles,
            "count": len(articles),
            "query": q,
            "rag_enabled": RAG_ENABLED
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/v1/user/{user_id}/interests")
async def update_interests(user_id: str, interest_update: InterestUpdate):
    """Update user interests"""
    try:
        interests = interest_update.interests
        
        if not interests:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Interests cannot be empty"}
            )
        
        if len(interests) > 5:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Maximum 5 interests allowed"}
            )
        
        success = users.update_interests(user_id, interests)
        
        if success:
            print(f"✅ Updated interests for {user_id}: {interests}")
            return JSONResponse(content={
                "success": True,
                "message": "Interests updated successfully",
                "interests": interests
            })
        else:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found"}
            )
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/v1/user/{user_id}/stats")
async def get_user_stats(user_id: str):
    """Get user statistics"""
    try:
        user = users.users.get(user_id, {})
        seen = users.get_seen_articles(user_id)
        
        return JSONResponse(content={
            "success": True,
            "totalRead": len(seen),
            "interests": user.get('interests', []),
            "ragEnabled": RAG_ENABLED,
            "lastUpdated": seen[-1]['seen_at'] if seen else datetime.now().isoformat(),
            "userName": user.get('name', 'User')
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/v1/summarize")
async def summarize_article(request: SummaryRequest):
    """Generate summary for an article"""
    try:
        if not request.content or len(request.content) < 50:
            return JSONResponse(content={
                "success": True,
                "summary": "Content too short to summarize."
            })
        
        print(f"📝 Generating summary...")
        
        summary = summarizer.summarize_article(request.content, max_length=150)
        
        if request.rag_enabled and rag:
            category = "general"
            content_lower = request.content.lower()
            
            for cat, keywords in CATEGORY_KEYWORDS.items():
                if any(keyword in content_lower for keyword in keywords):
                    category = cat
                    break
            
            enhanced_summary = rag.augment_summary(summary, category, request.article_id)
            rag.add_to_context(summary, category, request.article_id)
            
            return JSONResponse(content={
                "success": True,
                "summary": enhanced_summary,
                "rag_used": True,
                "category": category
            })
        
        return JSONResponse(content={
            "success": True,
            "summary": summary,
            "rag_used": False
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/v1/user/{user_id}/mark-read")
async def mark_article_read(user_id: str, request: MarkReadRequest):
    """Mark article as read"""
    try:
        users.mark_seen(user_id, request.article_id, "")
        return JSONResponse(content={
            "success": True,
            "message": "Article marked as read"
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/v1/settings/toggle-rag")
async def toggle_rag():
    """Toggle RAG feature"""
    global RAG_ENABLED
    try:
        new_state = not RAG_ENABLED
        import src.config.settings
        src.config.settings.RAG_ENABLED = new_state
        
        print(f"🔄 RAG toggled: {'ON' if new_state else 'OFF'}")
        
        return JSONResponse(content={
            "success": True,
            "ragEnabled": new_state,
            "message": f"RAG {'enabled' if new_state else 'disabled'}"
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

# ============================================
# Run the application
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting News Summarizer API Server")
    print("="*60)
    print(f"📍 Server URL: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🔍 Health Check: http://localhost:8000/health")
    print(f"⚙️  RAG Status: {'ENABLED' if RAG_ENABLED else 'DISABLED'}")
    print("="*60 + "\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )