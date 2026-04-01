import os
from dotenv import load_dotenv
from pathlib import Path
import json

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"

# Create directories if they don't exist
for dir_path in [DATA_DIR, LOGS_DIR, MODELS_DIR]:
    dir_path.mkdir(exist_ok=True)

# ============================================
# API KEYS
# ============================================
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
NEWSDATA_IO_API_KEY = os.getenv("NEWSDATA_IO_API_KEY")
WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")

# ============================================
# REDIS CONFIGURATION
# ============================================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# ============================================
# MODEL CONFIGURATION
# ============================================
SUMMARIZATION_MODEL = os.getenv("SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
USE_GPU = os.getenv("USE_GPU", "false").lower() == "true"
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 4))
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", str(MODELS_DIR / "cache"))

# Embedding Model for RAG
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "chromadb")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(DATA_DIR / "chroma_db"))

# ============================================
# APPLICATION SETTINGS
# ============================================
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
API_VERSION = os.getenv("API_VERSION", "v1")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

# CORS Settings
CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:8000"]'))
CORS_METHODS = json.loads(os.getenv("CORS_METHODS", '["GET", "POST", "PUT", "DELETE"]'))
CORS_HEADERS = json.loads(os.getenv("CORS_HEADERS", '["Authorization", "Content-Type"]'))

# Rate Limiting
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", 60))

# ============================================
# NEWS FETCHING CONFIGURATION
# ============================================
MAX_ARTICLES_PER_FETCH = int(os.getenv("MAX_ARTICLES_PER_FETCH", 50))
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "us")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", 30))
NEWS_CACHE_TTL = int(os.getenv("NEWS_CACHE_TTL", 3600))

# Categories to track
NEWS_CATEGORIES = os.getenv("NEWS_CATEGORIES", "general,business,technology,entertainment,health,science,sports").split(",")

# Historical data
HISTORICAL_DAYS_BACK = int(os.getenv("HISTORICAL_DAYS_BACK", 7))
ENABLE_HISTORICAL_CONTEXT = os.getenv("ENABLE_HISTORICAL_CONTEXT", "true").lower() == "true"

# ============================================
# DATABASE SETTINGS
# ============================================
USE_MONGODB = os.getenv("USE_MONGODB", "false").lower() == "true"
USE_POSTGRES = os.getenv("USE_POSTGRES", "false").lower() == "true"

# ============================================
# PERSONALIZATION
# ============================================
ENABLE_PERSONALIZATION = os.getenv("ENABLE_PERSONALIZATION", "true").lower() == "true"
MAX_USER_INTERESTS = int(os.getenv("MAX_USER_INTERESTS", 5))
DEFAULT_USER_INTERESTS = os.getenv("DEFAULT_USER_INTERESTS", "technology,business,health,sports").split(",")

# ============================================
# RAG SETTINGS
# ============================================
RAG_ENABLED = os.getenv("RAG_ENABLED", "true").lower() == "true"
RAG_CONTEXT_WINDOW = int(os.getenv("RAG_CONTEXT_WINDOW", 5))
RAG_SIMILARITY_THRESHOLD = float(os.getenv("RAG_SIMILARITY_THRESHOLD", 0.6))
RAG_MAX_CONTEXT_LENGTH = int(os.getenv("RAG_MAX_CONTEXT_LENGTH", 500))

# ============================================
# NOTIFICATIONS
# ============================================
SMTP_ENABLED = os.getenv("SMTP_ENABLED", "false").lower() == "true"
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"
PUSH_NOTIFICATION_ENABLED = os.getenv("PUSH_NOTIFICATION_ENABLED", "false").lower() == "true"

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "text")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", str(LOGS_DIR / "app.log"))

# ============================================
# PERFORMANCE
# ============================================
ASYNC_PROCESSING_ENABLED = os.getenv("ASYNC_PROCESSING_ENABLED", "false").lower() == "true"
ENABLE_REDIS_CACHE = os.getenv("ENABLE_REDIS_CACHE", "true").lower() == "true"
CACHE_DEFAULT_TTL = int(os.getenv("CACHE_DEFAULT_TTL", 300))

# ============================================
# SECURITY
# ============================================
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 24))

# ============================================
# TESTING
# ============================================
TESTING_MODE = os.getenv("TESTING_MODE", "false").lower() == "true"
MOCK_NEWS_API = os.getenv("MOCK_NEWS_API", "false").lower() == "true"

def validate_config():
    """Validate critical configuration"""
    errors = []
    
    if not NEWS_API_KEY and not GUARDIAN_API_KEY:
        errors.append("No news API key found. Set NEWS_API_KEY or GUARDIAN_API_KEY")
    
    if DEBUG and ENVIRONMENT == "production":
        errors.append("DEBUG mode should be False in production")
    
    if errors:
        for error in errors:
            print(f"⚠️  Config Warning: {error}")
        return False
    return True

# Print configuration on startup (only in debug mode)
if DEBUG:
    print("📋 Configuration loaded:")
    print(f"  • Environment: {ENVIRONMENT}")
    print(f"  • Debug mode: {DEBUG}")
    print(f"  • News API: {'✅' if NEWS_API_KEY else '❌'}")
    print(f"  • Guardian API: {'✅' if GUARDIAN_API_KEY else '❌'}")
    print(f"  • Redis: {'✅' if REDIS_URL else '❌'}")
    print(f"  • Summarization Model: {SUMMARIZATION_MODEL}")
    print(f"  • RAG Enabled: {RAG_ENABLED}")