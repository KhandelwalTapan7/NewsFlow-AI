import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.news_fetcher import NewsFetcher
from src.summarizer import NewsSummarizer, SimpleRAG
from src.user_profiles import UserPreferences
from src.notifier import Notifier
from src.config.settings import DEBUG, ENABLE_PERSONALIZATION, RAG_ENABLED as RAG_ENABLED_SETTING

class NewsSummarizerApp:
    def __init__(self):
        print("\n" + "=" * 70)
        print("🚀 REAL-TIME NEWS SUMMARIZER WITH RAG")
        print("=" * 70)
        
        print("\n📡 Initializing components...")
        self.fetcher = NewsFetcher()
        self.summarizer = NewsSummarizer()
        self.rag_enabled = RAG_ENABLED_SETTING
        self.rag = SimpleRAG() if self.rag_enabled else None
        self.users = UserPreferences()
        self.notifier = Notifier()
        
        # Create demo user
        self.demo_user_id = "demo_user_001"
        if self.demo_user_id not in self.users.users:
            self.users.create_user(
                self.demo_user_id, 
                "Demo User", 
                ["technology", "business", "health", "sports"]
            )
        
        print("✅ All components ready!\n")
    
    def get_personalized_news(self, user_id: str, limit: int = 10) -> list:
        """Get news tailored to user's interests"""
        print("\n🔍 Fetching news...")
        
        # Get user interests
        interests = self.users.get_user_interests(user_id)
        print(f"📌 Your interests: {', '.join(interests)}")
        
        # Fetch news for each interest
        all_articles = []
        for interest in interests[:3]:  # Limit to 3 interests for speed
            print(f"  • Searching for '{interest}' news...")
            articles = self.fetcher.search_by_topic(interest, days_back=3, page_size=5)
            all_articles.extend(articles)
        
        # Remove duplicates
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # Filter out seen articles
        new_articles = []
        for article in unique_articles[:limit]:
            if not self.users.has_seen(user_id, article['id']):
                new_articles.append(article)
        
        print(f"\n📰 Found {len(new_articles)} new articles for you!")
        return new_articles
    
    def get_top_headlines(self, limit: int = 10) -> list:
        """Get top headlines without personalization"""
        print("\n🌍 Fetching top headlines...")
        articles = self.fetcher.fetch_from_newsapi(page_size=limit)
        if not articles:
            articles = self.fetcher.fetch_from_guardian(page_size=limit)
        print(f"📰 Found {len(articles)} top headlines")
        return articles
    
    def search_news(self, query: str, limit: int = 10) -> list:
        """Search news by topic"""
        print(f"\n🔎 Searching for '{query}'...")
        articles = self.fetcher.search_by_topic(query, days_back=7, page_size=limit)
        print(f"📰 Found {len(articles)} articles")
        return articles
    
    def display_summaries(self, articles: list, user_id: str, show_context: bool = True):
        """Display summarized articles to user"""
        if not articles:
            print("\n📭 No articles found!")
            return
        
        print("\n" + "=" * 70)
        print(f"📰 YOUR PERSONALIZED NEWS DIGEST")
        print("=" * 70)
        
        # Summarize articles
        summarized = self.summarizer.batch_summarize(articles, max_length=120)
        
        for idx, summary_data in enumerate(summarized, 1):
            print(f"\n{'─' * 70}")
            print(f"📌 {idx}. {summary_data['title']}")
            print(f"   📍 Source: {summary_data['source']}")
            print(f"   🏷️  Category: {summary_data['category']}")
            
            # Get summary
            current_summary = summary_data['summary']
            
            # Add RAG context if enabled
            if self.rag and show_context and self.rag_enabled:
                enhanced_summary = self.rag.augment_summary(
                    current_summary, 
                    summary_data['category'],
                    summary_data['title']
                )
                print(f"\n   📝 {enhanced_summary}")
                
                # Store in RAG memory
                self.rag.add_to_context(
                    current_summary, 
                    summary_data['category'],
                    summary_data['title']
                )
            else:
                print(f"\n   📝 {current_summary}")
            
            print(f"\n   🔗 Read more: {summary_data['url'][:80]}...")
            
            # Mark as seen
            self.users.mark_seen(user_id, summary_data['id'], summary_data['title'])
            
            # Add notification if article is important (optional)
            if "breaking" in summary_data['title'].lower() or "urgent" in summary_data['title'].lower():
                user_name = self.users.users.get(user_id, {}).get('name', 'User')
                self.notifier.add_notification(
                    user_id,
                    user_name,
                    summary_data['title'],
                    current_summary[:100]
                )
        
        # Process any pending notifications
        self.notifier.process_notifications()
        
        print(f"\n{'=' * 70}")
        print(f"✅ Displayed {len(summarized)} articles")
        print(f"💡 Tip: Use option 2 to search for specific topics")
        print(f"{'=' * 70}")
    
    def show_user_stats(self, user_id: str):
        """Show user statistics"""
        user = self.users.users.get(user_id, {})
        seen = self.users.get_seen_articles(user_id)
        
        print("\n" + "=" * 50)
        print("📊 YOUR STATISTICS")
        print("=" * 50)
        print(f"👤 Name: {user.get('name', 'Unknown')}")
        print(f"🎯 Interests: {', '.join(user.get('interests', []))}")
        print(f"📖 Articles read: {len(seen)}")
        print(f"🔔 Notifications: {'Enabled' if user.get('notification_enabled', True) else 'Disabled'}")
        print(f"🧠 RAG Context: {'Enabled' if self.rag_enabled else 'Disabled'}")
        
        if seen:
            print(f"\n📚 Recently read:")
            for item in seen[-5:]:
                print(f"  • {item['title'][:60]}...")
        print("=" * 50)
    
    def update_interactive_preferences(self):
        """Interactive preference update"""
        print("\n" + "=" * 50)
        print("🎯 UPDATE YOUR PREFERENCES")
        print("=" * 50)
        
        current = self.users.get_user_interests(self.demo_user_id)
        print(f"\nCurrent interests: {', '.join(current)}")
        
        print("\nAvailable topics:")
        topics = ["technology", "politics", "business", "health", "sports", "science", "entertainment"]
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
        
        print("\nEnter topics (comma-separated, e.g., 'technology,sports'):")
        choice = input("👉 Your choice: ").strip()
        
        if choice:
            new_interests = [t.strip().lower() for t in choice.split(',')]
            valid_interests = [t for t in new_interests if t in topics]
            
            if valid_interests:
                self.users.update_interests(self.demo_user_id, valid_interests)
                print("✅ Preferences updated!")
            else:
                print("❌ Invalid topics. Please choose from the list.")
    
    def toggle_rag(self):
        """Toggle RAG context on/off"""
        self.rag_enabled = not self.rag_enabled
        if self.rag_enabled and not self.rag:
            self.rag = SimpleRAG()
        print(f"\n{'✅' if self.rag_enabled else '❌'} RAG context is now {'ENABLED' if self.rag_enabled else 'DISABLED'}")
    
    def run_interactive_mode(self):
        """Run the application in interactive mode"""
        while True:
            print("\n" + "=" * 50)
            print("📋 MAIN MENU")
            print("=" * 50)
            print("1. 📰 Get personalized news feed")
            print("2. 🔍 Search news by topic")
            print("3. 🌍 View top headlines (all)")
            print("4. 🎯 Update my interests")
            print("5. 📊 View my statistics")
            print(f"6. {'🔴' if self.rag_enabled else '⚫'} Toggle RAG context (currently {'ON' if self.rag_enabled else 'OFF'})")
            print("7. 🚪 Exit")
            print("=" * 50)
            
            choice = input("\n👉 Choose option (1-7): ").strip()
            
            if choice == '1':
                articles = self.get_personalized_news(self.demo_user_id, limit=8)
                self.display_summaries(articles, self.demo_user_id, show_context=self.rag_enabled)
                
            elif choice == '2':
                query = input("🔍 Enter search topic: ").strip()
                if query:
                    articles = self.search_news(query, limit=8)
                    self.display_summaries(articles, self.demo_user_id, show_context=False)
            
            elif choice == '3':
                articles = self.get_top_headlines(limit=10)
                self.display_summaries(articles, self.demo_user_id, show_context=False)
            
            elif choice == '4':
                self.update_interactive_preferences()
            
            elif choice == '5':
                self.show_user_stats(self.demo_user_id)
            
            elif choice == '6':
                self.toggle_rag()
            
            elif choice == '7':
                print("\n👋 Thank you for using News Summarizer!")
                print("📰 Stay informed! Goodbye!\n")
                break
            
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\n⏎ Press Enter to continue...")

def main():
    """Main entry point"""
    try:
        app = NewsSummarizerApp()
        
        # Start background scheduler for notifications
        app.notifier.start_scheduler(interval_minutes=30)
        
        # Run interactive mode
        app.run_interactive_mode()
        
        # Cleanup
        app.notifier.stop_scheduler()
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()