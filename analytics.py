import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import tweepy
from database import TweetDatabase
from logger import logger
import config

class TwitterAnalytics:
    def __init__(self):
        self.db = TweetDatabase()
        
        # Twitter authentication
        self.client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET
        )
        
        # Create directory for analytics if it doesn't exist
        if not os.path.exists('analytics'):
            os.makedirs('analytics')
    
    def update_engagement_metrics(self):
        """Fetch and update engagement metrics for recent tweets"""
        try:
            # Get recent tweets from database
            recent_tweets = self.db.get_tweet_history(limit=20)
            
            for tweet in recent_tweets:
                tweet_id = tweet['tweet_id']
                
                # Get tweet metrics from Twitter API
                response = self.client.get_tweet(
                    id=tweet_id,
                    tweet_fields=['public_metrics']
                )
                
                if response and response.data:
                    metrics = response.data.public_metrics
                    likes = metrics.get('like_count', 0)
                    retweets = metrics.get('retweet_count', 0)
                    
                    # Update database
                    self.db.update_engagement(tweet_id, likes, retweets)
                    logger.info(f"Updated engagement for tweet {tweet_id}: {likes} likes, {retweets} retweets")
            
            logger.info(f"Engagement metrics updated for {len(recent_tweets)} tweets")
            
        except Exception as e:
            logger.error(f"Error updating engagement metrics: {e}")
    
    def generate_category_report(self):
        """Generate performance report by category"""
        try:
            # Get stats by category
            category_stats = self.db.get_category_stats()
            
            if not category_stats:
                logger.warning("No category stats available for report")
                return None
            
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(category_stats)
            
            # Generate bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(df['category'], df['avg_engagement'], color='skyblue')
            plt.xlabel('Category')
            plt.ylabel('Average Engagement (Likes + Retweets)')
            plt.title('Tweet Performance by Category')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save chart
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f'analytics/category_performance_{timestamp}.png'
            plt.savefig(filename)
            plt.close()
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating category report: {e}")
            return None
    
    def generate_weekly_report(self):
        """Generate weekly performance report"""
        try:
            # Update engagement metrics
            self.update_engagement_metrics()
            
            # Get recent tweets
            recent_tweets = self.db.get_tweet_history(limit=30)
            
            if not recent_tweets:
                logger.warning("No tweets available for weekly report")
                return "No tweets available for analysis this week."
            
            # Convert to DataFrame
            df = pd.DataFrame(recent_tweets)
            
            # Convert post_time to datetime
            df['post_time'] = pd.to_datetime(df['post_time'])
            
            # Filter last 7 days
            one_week_ago = datetime.now() - timedelta(days=7)
            df_week = df[df['post_time'] > one_week_ago]
            
            if df_week.empty:
                logger.warning("No tweets in the last 7 days for weekly report")
                return "No tweets posted in the last 7 days."
            
            # Calculate total engagement
            df_week['total_engagement'] = df_week['engagement_likes'] + df_week['engagement_retweets']
            
            # Generate charts
            self._generate_weekly_charts(df_week)
            
            # Generate text summary
            total_tweets = len(df_week)
            total_engagement = df_week['total_engagement'].sum()
            avg_engagement = df_week['total_engagement'].mean()
            best_category = df_week.groupby('category')['total_engagement'].mean().idxmax()
            best_tweet_idx = df_week['total_engagement'].idxmax()
            best_tweet = df_week.loc[best_tweet_idx]
            
            report = (
                f"📊 Weekly Twitter Performance Report\n\n"
                f"• Tweets posted: {total_tweets}\n"
                f"• Total engagement: {total_engagement}\n"
                f"• Average engagement per tweet: {avg_engagement:.2f}\n"
                f"• Best performing category: {best_category}\n"
                f"• Best performing tweet: {best_tweet['content'][:50]}...\n"
                f"  ({best_tweet['engagement_likes']} likes, {best_tweet['engagement_retweets']} retweets)\n\n"
                f"See analytics folder for detailed charts."
            )
            
            logger.info("Weekly report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Error generating weekly report: {e}")
            return f"Error generating weekly report: {str(e)}"
    
    def _generate_weekly_charts(self, df_week):
        """Generate charts for weekly report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            
            # Chart 1: Daily tweet count
            plt.figure(figsize=(10, 6))
            df_week['date'] = df_week['post_time'].dt.date
            daily_counts = df_week.groupby('date').size()
            daily_counts.plot(kind='bar', color='skyblue')
            plt.xlabel('Date')
            plt.ylabel('Number of Tweets')
            plt.title('Tweets Posted per Day')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'analytics/daily_tweet_count_{timestamp}.png')
            plt.close()
            
            # Chart 2: Category distribution
            plt.figure(figsize=(10, 6))
            category_counts = df_week['category'].value_counts()
            category_counts.plot(kind='pie', autopct='%1.1f%%')
            plt.title('Tweet Category Distribution')
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig(f'analytics/category_distribution_{timestamp}.png')
            plt.close()
            
            # Chart 3: Engagement by day of week
            plt.figure(figsize=(10, 6))
            df_week['day_of_week'] = df_week['post_time'].dt.day_name()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            engagement_by_day = df_week.groupby('day_of_week')['total_engagement'].mean().reindex(day_order)
            engagement_by_day.plot(kind='bar', color='lightgreen')
            plt.xlabel('Day of Week')
            plt.ylabel('Average Engagement')
            plt.title('Engagement by Day of Week')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'analytics/engagement_by_day_{timestamp}.png')
            plt.close()
            
            logger.info("Weekly charts generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating weekly charts: {e}") 