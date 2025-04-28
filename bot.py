import os
import argparse
import time
import random
import tweepy
import feedparser
from datetime import datetime

# Internal modules
import config
from logger import logger
from database import TweetDatabase
from content_generator import ContentGenerator
from sentiment import SentimentAnalyzer
from scheduler import TweetScheduler
from analytics import TwitterAnalytics

class TwitterBot:
    def __init__(self):
        logger.info("Initializing Twitter Bot")
        
        # Initialize the Twitter client
        self.client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET
        )
        
        # Initialize helper modules
        self.db = TweetDatabase()
        self.content_generator = ContentGenerator()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.analytics = TwitterAnalytics()
        
        # Initialize scheduler (pass self to allow scheduling bot methods)
        self.scheduler = TweetScheduler(self)
        
        logger.info("Twitter Bot initialized successfully")
    
    def fetch_news(self, category='tech'):
        """Fetch latest news from RSS feed based on category"""
        logger.info(f"Fetching {category} news")
        
        if category not in config.NEWS_SOURCES:
            logger.error(f"Invalid news category: {category}")
            return None
        
        feed_url = config.NEWS_SOURCES[category]
        feed = feedparser.parse(feed_url)
        entries = feed.entries
        
        if not entries:
            logger.warning(f"No entries found in {category} feed")
            return None
        
        # Get random article from the 5 most recent
        article = random.choice(entries[:5])
        title = article.title
        link = article.link
        
        # Select random hashtags for this category
        hashtags = ' '.join(random.sample(config.HASHTAGS.get(category, []), 
                                          min(2, len(config.HASHTAGS.get(category, [])))))
        
        return f"{title} {link} {hashtags}"
    
    def post_tweet(self, text, category='general'):
        """Post a tweet and log it to the database"""
        if not text:
            logger.warning("Cannot post empty tweet")
            return None
        
        # Check tweet length
        if len(text) > config.MAX_TWEET_LENGTH:
            logger.warning(f"Tweet exceeds maximum length ({len(text)} characters)")
            text = text[:config.MAX_TWEET_LENGTH - 3] + "..."
        
        try:
            # Post tweet using Twitter API v2
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            logger.info(f"Tweet posted successfully! ID: {tweet_id}")
            
            # Save to database
            self.db.add_tweet(tweet_id, text, category)
            
            return tweet_id
        
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None
    
    def post_news(self, category='tech'):
        """Post a news tweet"""
        logger.info(f"Posting {category} news")
        news_text = self.fetch_news(category)
        
        if news_text:
            return self.post_tweet(news_text, category=category)
        else:
            logger.warning(f"No news content to post for {category}")
            return None
    
    def post_ml_snippet(self):
        """Post an ML code snippet"""
        logger.info("Posting ML snippet")
        ml_snippet = self.content_generator.generate_ml_snippet()
        return self.post_tweet(ml_snippet, category='ml')
    
    def post_code_tip(self):
        """Post a coding tip"""
        logger.info("Posting code tip")
        code_tip = self.content_generator.generate_code_tip()
        return self.post_tweet(code_tip, category='code_tip')
    
    def post_interview_question(self):
        """Post an interview question"""
        logger.info("Posting interview question")
        question = self.content_generator.generate_interview_question()
        return self.post_tweet(question, category='interview')
    
    def post_sentiment_analysis(self):
        """Post sentiment analysis for a trending topic"""
        logger.info("Posting sentiment analysis")
        
        # Get trending topics
        topics = self.sentiment_analyzer.get_trending_topics()
        if not topics:
            logger.warning("No trending topics found")
            return None
        
        # Choose a random topic
        topic = random.choice(topics)
        logger.info(f"Selected trending topic: {topic}")
        
        # Analyze sentiment
        sentiment_text, chart_path = self.sentiment_analyzer.analyze_topic_sentiment(topic)
        
        if sentiment_text:
            return self.post_tweet(sentiment_text, category='sentiment')
        else:
            logger.warning(f"Could not generate sentiment analysis for {topic}")
            return None
    
    def generate_weekly_report(self):
        """Generate weekly analytics report"""
        logger.info("Generating weekly analytics report")
        report = self.analytics.generate_weekly_report()
        
        if report:
            logger.info("Weekly report generated")
            
            # You could send this report via email or post a summary as a tweet
            # For now, we'll just log it
            logger.info(report)
        
        return report
    
    def start_scheduler(self):
        """Start the tweet scheduler"""
        logger.info("Starting tweet scheduler")
        self.scheduler.start()
    
    def stop_scheduler(self):
        """Stop the tweet scheduler"""
        logger.info("Stopping tweet scheduler")
        self.scheduler.stop()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Twitter Bot for CS and Tech content')
    parser.add_argument('action', choices=['run', 'post', 'schedule', 'report', 'test'], 
                        help='Action to perform')
    parser.add_argument('--type', choices=['news', 'ml', 'code_tip', 'interview', 'sentiment'],
                        help='Type of content to post')
    parser.add_argument('--category', help='News category to use', default='tech')
    
    return parser.parse_args()

def main():
    """Main entry point for the bot"""
    args = parse_args()
    bot = TwitterBot()
    
    if args.action == 'run':
        # Run a single task
        if args.type == 'news':
            bot.post_news(args.category)
        elif args.type == 'ml':
            bot.post_ml_snippet()
        elif args.type == 'code_tip':
            bot.post_code_tip()
        elif args.type == 'interview':
            bot.post_interview_question()
        elif args.type == 'sentiment':
            bot.post_sentiment_analysis()
        else:
            logger.error(f"Unknown content type: {args.type}")
    
    elif args.action == 'post':
        # Interactive mode to post a custom tweet
        text = input("Enter tweet text: ")
        category = input("Enter category: ")
        bot.post_tweet(text, category)
    
    elif args.action == 'schedule':
        # Start scheduler in daemon mode
        bot.start_scheduler()
        
        # Keep the script running
        try:
            logger.info("Scheduler running. Press Ctrl+C to stop...")
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            bot.stop_scheduler()
    
    elif args.action == 'report':
        # Generate analytics report
        bot.generate_weekly_report()
    
    elif args.action == 'test':
        # Run a test of each functionality
        logger.info("Testing bot functionality")
        bot.post_news()
        bot.post_ml_snippet()
        bot.post_sentiment_analysis()

if __name__ == "__main__":
    main() 