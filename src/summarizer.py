import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
import json
from datetime import datetime
from typing import List, Dict
import torch

# Try to import transformers, but provide fallback
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not installed. Using basic summarization.")

from src.config.settings import (
    SUMMARIZATION_MODEL, USE_GPU, BATCH_SIZE, 
    MODEL_CACHE_DIR, RAG_ENABLED, RAG_CONTEXT_WINDOW
)

class NewsSummarizer:
    def __init__(self):
        print(f"🔄 Loading summarization model...")
        self.device = -1  # CPU
        self.model = None
        self.tokenizer = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                # Use a smaller model for faster loading
                model_name = "sshleifer/distilbart-cnn-12-6"
                print(f"   Using model: {model_name}")
                
                # Load tokenizer and model directly
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_name, 
                    cache_dir=MODEL_CACHE_DIR
                )
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_name,
                    cache_dir=MODEL_CACHE_DIR
                )
                
                # Move to GPU if available
                if USE_GPU and torch.cuda.is_available():
                    self.model = self.model.cuda()
                    self.device = 0
                    print(f"   Model loaded on GPU")
                else:
                    print(f"   Model loaded on CPU")
                
                print(f"✅ Model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Could not load transformer model: {e}")
                print("   Using basic summarization instead.")
                self.model = None
                self.tokenizer = None
        else:
            print("   Using basic summarization (install transformers for AI summaries)")
    
    def summarize_article(self, text: str, max_length: int = 150, min_length: int = 40) -> str:
        """Generate a concise summary of the article"""
        if not text or len(text) < 50:
            return "Content too short to summarize."
        
        # Clean the text
        text = text.strip().replace('\n', ' ')
        
        if self.model and self.tokenizer:
            try:
                # Truncate if too long
                inputs = self.tokenizer(
                    text, 
                    max_length=1024, 
                    truncation=True, 
                    return_tensors="pt"
                )
                
                # Move to GPU if needed
                if self.device == 0:
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                # Generate summary
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
                
                summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                return summary
            except Exception as e:
                print(f"⚠️ Summarization error: {e}")
                return self._basic_summarize(text, max_length)
        else:
            return self._basic_summarize(text, max_length)
    
    def _basic_summarize(self, text: str, max_length: int = 150) -> str:
        """Fallback basic summarization by extracting key sentences"""
        # Split into sentences
        sentences = text.replace('!', '.').replace('?', '.').split('. ')
        
        if len(sentences) <= 3:
            if len(text) > max_length:
                return text[:max_length] + "..."
            return text
        
        # Take first 2-3 sentences for news (most important info is at the beginning)
        summary = '. '.join(sentences[:3])
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        return summary
    
    def batch_summarize(self, articles: List[Dict], max_length: int = 150) -> List[Dict]:
        """Summarize multiple articles"""
        summaries = []
        
        for idx, article in enumerate(articles, 1):
            print(f"📝 Summarizing {idx}/{len(articles)}: {article.get('title', 'Untitled')[:50]}...")
            
            # Get content to summarize
            content = article.get('content') or article.get('description', '')
            summary = self.summarize_article(content, max_length)
            
            summaries.append({
                'id': article.get('id'),
                'title': article.get('title'),
                'summary': summary,
                'category': article.get('category'),
                'source': article.get('source'),
                'url': article.get('url'),
                'published_at': article.get('published_at')
            })
        
        return summaries

class SimpleRAG:
    """Simple Retrieval-Augmented Generation for context"""
    def __init__(self):
        self.context_memory = []
        self.context_file = "data/rag_context.json"
        self._load_context()
    
    def _load_context(self):
        """Load saved context from file"""
        try:
            os.makedirs("data", exist_ok=True)
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context_memory = json.load(f)
                print(f"✅ Loaded {len(self.context_memory)} historical contexts")
        except Exception as e:
            print(f"⚠️ Could not load context: {e}")
    
    def _save_context(self):
        """Save context to file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self.context_memory[-100:], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save context: {e}")
    
    def add_to_context(self, article_summary: str, category: str, title: str = ""):
        """Store summarized articles for future context"""
        self.context_memory.append({
            'category': category,
            'title': title,
            'summary': article_summary,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 100 items
        if len(self.context_memory) > 100:
            self.context_memory = self.context_memory[-100:]
        
        self._save_context()
    
    def retrieve_context(self, category: str, limit: int = 3) -> List[Dict]:
        """Retrieve relevant historical context for a category"""
        relevant = [item for item in self.context_memory if item['category'] == category]
        return relevant[-limit:] if relevant else []
    
    def augment_summary(self, current_summary: str, category: str, title: str = "") -> str:
        """Add historical context to current summary"""
        if not RAG_ENABLED:
            return current_summary
        
        context = self.retrieve_context(category, RAG_CONTEXT_WINDOW)
        if not context:
            return current_summary
        
        # Build context string
        context_parts = []
        for ctx in context[:3]:  # Limit to 3 for brevity
            ctx_summary = ctx['summary'][:100]
            context_parts.append(f"• Previously: {ctx_summary}")
        
        if context_parts:
            context_text = "\n".join(context_parts)
            return f"{context_text}\n\n📰 Current Update:\n{current_summary}"
        
        return current_summary