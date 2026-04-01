# test_redis.py
import redis
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Try without password first
    r = redis.from_url(os.getenv('REDIS_URL'))
    r.ping()
    print("✅ Redis connection successful!")
except Exception as e:
    print(f"❌ Redis connection failed: {e}")
    print("\nYou might need to add password to REDIS_URL")
    print("Format: redis://default:your_password@host:port")