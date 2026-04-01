import re
from typing import Optional, Any

def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not url or not isinstance(url, str):
        return False
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))

def validate_text(text: str, min_length: int = 10, max_length: int = 10000) -> bool:
    """Validate text content"""
    if not text or not isinstance(text, str):
        return False
    text = text.strip()
    return min_length <= len(text) <= max_length

def validate_api_key(key: str, prefix: Optional[str] = None, min_length: int = 16) -> bool:
    """Validate API key format"""
    if not key or not isinstance(key, str):
        return False
    if prefix and not key.startswith(prefix):
        return False
    return len(key) >= min_length

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>{}()\[\]\\;]', '', text)
    return text.strip()

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    return bool(email_pattern.match(email))

def validate_date(date_string: str) -> bool:
    """Validate date string format"""
    if not date_string:
        return False
    try:
        from datetime import datetime
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except:
        return False

def is_valid_json(data: Any) -> bool:
    """Check if data is valid JSON"""
    try:
        import json
        json.dumps(data)
        return True
    except:
        return False