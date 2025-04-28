import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
from datetime import datetime

# Make sure the bot modules are importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from content_generator import ContentGenerator
from sentiment import SentimentAnalyzer
from database import TweetDatabase
from logger import logger

class TestContentGenerator(unittest.TestCase):
    def setUp(self):
        self.content_generator = ContentGenerator()
    
    def test_ml_snippet_generation(self):
        """Test ML snippet generation"""
        snippet = self.content_generator.generate_ml_snippet()
        self.assertIsNotNone(snippet)
        self.assertIsInstance(snippet, str)
        self.assertGreater(len(snippet), 50)
    
    def test_code_tip_generation(self):
        """Test code tip generation"""
        tip = self.content_generator.generate_code_tip()
        self.assertIsNotNone(tip)
        self.assertIsInstance(tip, str)
        self.assertGreater(len(tip), 50)
    
    def test_interview_question_generation(self):
        """Test interview question generation"""
        question = self.content_generator.generate_interview_question()
        self.assertIsNotNone(question)
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 50)


class TestSentimentAnalyzer(unittest.TestCase):
    @patch('sentiment.SentimentAnalyzer.clean_text')
    def test_text_cleaning(self, mock_clean_text):
        """Test tweet text cleaning"""
        analyzer = SentimentAnalyzer()
        
        # Set up the mock
        mock_clean_text.return_value = "cleaned text"
        
        # Call the method
        result = analyzer.clean_text("some @user #hashtag http://t.co/link text")
        
        # Assert the result
        self.assertEqual(result, "cleaned text")
    
    @patch('tweepy.Client')
    def test_trending_topics_fallback(self, mock_client):
        """Test trending topics fallback values on error"""
        # Set up the mock to raise exception
        analyzer = SentimentAnalyzer()
        analyzer.client = mock_client
        mock_client.get_place_trends.side_effect = Exception("API error")
        
        # Call method and check for fallback values
        topics = analyzer.get_trending_topics()
        self.assertIsInstance(topics, list)
        self.assertTrue(all(isinstance(t, str) for t in topics))
        self.assertGreaterEqual(len(topics), 3)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a test database file
        self.original_db_filename = config.DB_FILENAME
        config.DB_FILENAME = "test_tweets.db"
        self.db = TweetDatabase()
    
    def tearDown(self):
        # Remove test database
        config.DB_FILENAME = self.original_db_filename
        if os.path.exists("test_tweets.db"):
            os.remove("test_tweets.db")
    
    def test_add_tweet(self):
        """Test adding a tweet to the database"""
        # Add a tweet
        tweet_id = "1234567890"
        content = "Test tweet content"
        category = "test"
        self.db.add_tweet(tweet_id, content, category)
        
        # Get and check the tweet
        tweets = self.db.get_tweet_history(limit=1)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0]['tweet_id'], tweet_id)
        self.assertEqual(tweets[0]['content'], content)
        self.assertEqual(tweets[0]['category'], category)
    
    def test_update_engagement(self):
        """Test updating engagement metrics"""
        # Add a tweet
        tweet_id = "1234567890"
        content = "Test tweet content"
        category = "test"
        self.db.add_tweet(tweet_id, content, category)
        
        # Update engagement
        likes = 10
        retweets = 5
        self.db.update_engagement(tweet_id, likes, retweets)
        
        # Check that engagement was updated
        tweets = self.db.get_tweet_history(limit=1)
        self.assertEqual(tweets[0]['engagement_likes'], likes)
        self.assertEqual(tweets[0]['engagement_retweets'], retweets)


if __name__ == '__main__':
    unittest.main() 