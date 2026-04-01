"""Configuration module for News Summarizer"""

from .settings import (
    # API Keys
    NEWS_API_KEY,
    GUARDIAN_API_KEY,
    NEWSDATA_IO_API_KEY,
    WORLD_NEWS_API_KEY,
    
    # Redis
    REDIS_URL,
    
    # Model Settings
    SUMMARIZATION_MODEL,
    USE_GPU,
    BATCH_SIZE,
    MODEL_CACHE_DIR,
    
    # Application Settings
    DEBUG,
    ENVIRONMENT,
    SECRET_KEY,
    
    # News Settings
    MAX_ARTICLES_PER_FETCH,
    DEFAULT_COUNTRY,
    DEFAULT_LANGUAGE,
    NEWS_CATEGORIES,
    
    # RAG Settings
    RAG_ENABLED,
    RAG_CONTEXT_WINDOW,
    
    # Logging
    LOG_LEVEL,
    LOG_FILE_PATH,
    
    # Validate config
    validate_config
)

__all__ = [
    'NEWS_API_KEY',
    'GUARDIAN_API_KEY',
    'NEWSDATA_IO_API_KEY',
    'WORLD_NEWS_API_KEY',
    'REDIS_URL',
    'SUMMARIZATION_MODEL',
    'USE_GPU',
    'BATCH_SIZE',
    'MODEL_CACHE_DIR',
    'DEBUG',
    'ENVIRONMENT',
    'SECRET_KEY',
    'MAX_ARTICLES_PER_FETCH',
    'DEFAULT_COUNTRY',
    'DEFAULT_LANGUAGE',
    'NEWS_CATEGORIES',
    'RAG_ENABLED',
    'RAG_CONTEXT_WINDOW',
    'LOG_LEVEL',
    'LOG_FILE_PATH',
    'validate_config'
]