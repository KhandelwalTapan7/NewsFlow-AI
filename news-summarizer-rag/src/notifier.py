import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
from datetime import datetime
from typing import List, Dict
import os

class Notifier:
    def __init__(self):
        self.notification_queue = []
        self.is_running = False
        self.scheduler_thread = None
        print("📧 Notification system initialized")
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email notification"""
        try:
            # For testing, just print the email
            print(f"\n📧 [EMAIL] To: {to_email}")
            print(f"   Subject: {subject}")
            print(f"   Body: {body[:200]}...")
            
            # Uncomment this section for actual email sending
            """
            smtp_server = os.getenv('SMTP_HOST', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            sender_email = os.getenv('SMTP_USER')
            sender_password = os.getenv('SMTP_PASSWORD')
            
            if sender_email and sender_password:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                print(f"✅ Email sent to {to_email}")
                return True
            """
            return True
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False
    
    def send_console_notification(self, user_name: str, article_title: str, summary: str):
        """Print notification to console (for testing)"""
        print("\n" + "=" * 60)
        print(f"🔔 NOTIFICATION for {user_name}")
        print("=" * 60)
        print(f"📰 {article_title}")
        print(f"📝 {summary[:150]}...")
        print("=" * 60)
    
    def add_notification(self, user_id: str, user_name: str, article_title: str, summary: str, user_email: str = None):
        """Queue a notification for user"""
        self.notification_queue.append({
            'user_id': user_id,
            'user_name': user_name,
            'email': user_email,
            'title': article_title,
            'summary': summary,
            'timestamp': datetime.now()
        })
    
    def process_notifications(self):
        """Send all queued notifications"""
        if not self.notification_queue:
            return
        
        print(f"\n📨 Processing {len(self.notification_queue)} notifications...")
        
        for notif in self.notification_queue:
            # Always show in console
            self.send_console_notification(
                notif['user_name'],
                notif['title'],
                notif['summary']
            )
            
            # Send email if email is provided
            if notif.get('email'):
                subject = f"📰 News Alert: {notif['title'][:50]}"
                body = f"{notif['summary']}\n\nStay informed with News Summarizer!"
                self.send_email(notif['email'], subject, body)
        
        self.notification_queue.clear()
    
    def _scheduler_loop(self, interval_minutes: int):
        """Background thread loop for scheduled checks"""
        while self.is_running:
            time.sleep(interval_minutes * 60)
            if self.is_running:
                print(f"🕐 [{datetime.now().strftime('%H:%M:%S')}] Scheduled news check")
                self.process_notifications()
    
    def start_scheduler(self, interval_minutes: int = 30):
        """Start background scheduler for periodic checks"""
        self.is_running = True
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            args=(interval_minutes,),
            daemon=True
        )
        self.scheduler_thread.start()
        print(f"✅ Scheduler started (checks every {interval_minutes} minutes)")
    
    def stop_scheduler(self):
        """Stop the background scheduler"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        print("🛑 Scheduler stopped")