import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from src.config.settings import LOG_LEVEL, LOG_FILE_PATH
except ImportError:
    LOG_LEVEL = "INFO"
    LOG_FILE_PATH = "logs/app.log"

def setup_logger(name: str = "news_summarizer") -> logging.Logger:
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        log_dir = Path(LOG_FILE_PATH).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not create log file: {e}")
    
    return logger

# Create default logger
logger = setup_logger()

def log_error(error: Exception, context: str = ""):
    """Log an error with context"""
    logger.error(f"{context}: {str(error)}", exc_info=True)

def log_info(message: str):
    """Log info message"""
    logger.info(message)

def log_debug(message: str):
    """Log debug message"""
    logger.debug(message)

def log_warning(message: str):
    """Log warning message"""
    logger.warning(message)