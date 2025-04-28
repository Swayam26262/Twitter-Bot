import schedule
import time
import threading
import datetime
from logger import logger
import config

class TweetScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scheduler_thread = None
    
    def parse_schedule_times(self, time_str):
        """Parse schedule time string into list of time objects"""
        time_list = []
        for t in time_str.split(','):
            try:
                hour, minute = map(int, t.strip().split(':'))
                time_list.append(datetime.time(hour=hour, minute=minute))
            except Exception as e:
                logger.error(f"Error parsing time '{t}': {e}")
        return time_list
    
    def setup_schedule(self):
        """Set up scheduled tasks based on config"""
        logger.info("Setting up tweet schedule")
        
        # Schedule news posts
        if 'news' in config.POSTING_SCHEDULE:
            times = self.parse_schedule_times(config.POSTING_SCHEDULE['news'])
            for t in times:
                schedule.every().day.at(f"{t.hour:02d}:{t.minute:02d}").do(
                    self.bot.post_news
                )
                logger.info(f"Scheduled news post at {t.hour:02d}:{t.minute:02d}")
        
        # Schedule ML snippets
        if 'ml' in config.POSTING_SCHEDULE:
            times = self.parse_schedule_times(config.POSTING_SCHEDULE['ml'])
            for t in times:
                schedule.every().day.at(f"{t.hour:02d}:{t.minute:02d}").do(
                    self.bot.post_ml_snippet
                )
                logger.info(f"Scheduled ML snippet at {t.hour:02d}:{t.minute:02d}")
        
        # Schedule sentiment analysis
        if 'sentiment' in config.POSTING_SCHEDULE:
            times = self.parse_schedule_times(config.POSTING_SCHEDULE['sentiment'])
            for t in times:
                schedule.every().day.at(f"{t.hour:02d}:{t.minute:02d}").do(
                    self.bot.post_sentiment_analysis
                )
                logger.info(f"Scheduled sentiment analysis at {t.hour:02d}:{t.minute:02d}")
        
        # Schedule code tips (every Tuesday and Thursday)
        if 'code_tip' in config.POSTING_SCHEDULE:
            times = self.parse_schedule_times(config.POSTING_SCHEDULE.get('code_tip', '14:00'))
            for t in times:
                schedule.every().tuesday.at(f"{t.hour:02d}:{t.minute:02d}").do(
                    self.bot.post_code_tip
                )
                schedule.every().thursday.at(f"{t.hour:02d}:{t.minute:02d}").do(
                    self.bot.post_code_tip
                )
                logger.info(f"Scheduled code tips on Tuesday and Thursday at {t.hour:02d}:{t.minute:02d}")
        
        # Schedule interview questions (every Monday)
        if 'interview' in config.POSTING_SCHEDULE:
            times = self.parse_schedule_times(config.POSTING_SCHEDULE.get('interview', '10:00'))
            for t in times:
                schedule.every().monday.at(f"{t.hour:02d}:{t.minute:02d}").do(
                    self.bot.post_interview_question
                )
                logger.info(f"Scheduled interview questions on Monday at {t.hour:02d}:{t.minute:02d}")
        
        # Schedule weekly analytics (Sunday night)
        schedule.every().sunday.at("23:00").do(self.bot.generate_weekly_report)
        logger.info("Scheduled weekly analytics report on Sunday at 23:00")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("Starting scheduler loop")
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        logger.info("Scheduler loop stopped")
    
    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.setup_schedule()
        self.running = True
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        logger.info("Scheduler started in background thread")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.running:
            logger.warning("Scheduler is not running")
            return
        
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
        logger.info("Scheduler stopped") 