import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import os
import re
from datetime import datetime
import config
from logger import logger

class SentimentAnalyzer:
    def __init__(self):
        # Twitter authentication
        self.client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET
        )
        # Create directory for charts if it doesn't exist
        if not os.path.exists('charts'):
            os.makedirs('charts')
    
    def clean_text(self, text):
        """Clean tweet text by removing links, special characters, etc."""
        if not text:
            return ""
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\@\w+|\#', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        return text
    
    def get_trending_topics(self, woeid=1):
        """Get trending topics for a location (default: worldwide)"""
        try:
            # Using API v1.1 for trends
            auth = tweepy.OAuth1UserHandler(
                config.TWITTER_API_KEY, 
                config.TWITTER_API_SECRET,
                config.TWITTER_ACCESS_TOKEN,
                config.TWITTER_ACCESS_SECRET
            )
            api = tweepy.API(auth)
            trends = api.get_place_trends(woeid)
            return [trend['name'] for trend in trends[0]['trends'] if not trend['name'].startswith('#')][:5]
        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return ["AI", "Python", "Machine Learning", "Data Science", "Technology"]
    
    def analyze_topic_sentiment(self, topic, count=100):
        """Analyze sentiment for a given topic"""
        logger.info(f"Analyzing sentiment for topic: {topic}")
        
        try:
            tweets = self.client.search_recent_tweets(
                query=f"{topic} lang:en -is:retweet", 
                max_results=count
            ).data
            
            if not tweets:
                logger.warning(f"No tweets found for topic: {topic}")
                return None, None
            
            # Process tweets
            data = []
            for tweet in tweets:
                clean_tweet = self.clean_text(tweet.text)
                if clean_tweet:
                    analysis = TextBlob(clean_tweet)
                    polarity = analysis.sentiment.polarity
                    subjectivity = analysis.sentiment.subjectivity
                    data.append([tweet.text, clean_tweet, polarity, subjectivity])
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=['Tweet', 'Clean Tweet', 'Polarity', 'Subjectivity'])
            
            # Generate chart
            chart_path = self.generate_sentiment_chart(df, topic)
            
            # Generate summary
            sentiment_summary = self.generate_sentiment_summary(df, topic)
            
            return sentiment_summary, chart_path
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return None, None
    
    def generate_sentiment_chart(self, df, topic):
        """Generate a sentiment distribution chart"""
        try:
            plt.figure(figsize=(10, 6))
            plt.hist(df['Polarity'], bins=20, color='blue', alpha=0.7)
            plt.axvline(x=df['Polarity'].mean(), color='red', linestyle='--', linewidth=2)
            plt.title(f'Sentiment Distribution for "{topic}"')
            plt.xlabel('Polarity (Negative → Positive)')
            plt.ylabel('Number of Tweets')
            
            # Add some metrics
            plt.annotate(f'Average: {df["Polarity"].mean():.2f}', 
                        xy=(0.7, 0.9), xycoords='axes fraction')
            plt.annotate(f'Tweets analyzed: {len(df)}', 
                        xy=(0.7, 0.85), xycoords='axes fraction')
            
            # Save chart
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'charts/sentiment_{topic.replace(" ", "_")}_{timestamp}.png'
            plt.savefig(filename)
            plt.close()
            
            return filename
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            return None
    
    def generate_sentiment_summary(self, df, topic):
        """Generate a text summary of sentiment analysis"""
        avg_polarity = df['Polarity'].mean()
        
        # Determine sentiment category
        if avg_polarity > 0.2:
            sentiment = "strongly positive"
        elif avg_polarity > 0:
            sentiment = "slightly positive"
        elif avg_polarity == 0:
            sentiment = "neutral"
        elif avg_polarity > -0.2:
            sentiment = "slightly negative"
        else:
            sentiment = "strongly negative"
        
        # Count sentiment distribution
        positive = (df['Polarity'] > 0).sum()
        neutral = (df['Polarity'] == 0).sum()
        negative = (df['Polarity'] < 0).sum()
        
        pos_percentage = (positive / len(df)) * 100
        neg_percentage = (negative / len(df)) * 100
        neu_percentage = (neutral / len(df)) * 100
        
        summary = (
            f"📊 Sentiment Analysis: #{topic.replace(' ', '')}\n\n"
            f"Public sentiment is {sentiment} (avg: {avg_polarity:.2f})\n"
            f"• 😊 Positive: {pos_percentage:.1f}%\n"
            f"• 😐 Neutral: {neu_percentage:.1f}%\n"
            f"• 😔 Negative: {neg_percentage:.1f}%\n\n"
            f"Based on analysis of {len(df)} tweets. #DataScience"
        )
        
        return summary 