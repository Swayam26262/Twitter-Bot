import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# News sources
NEWS_SOURCES = {
    'tech': 'https://techcrunch.com/feed/',
    'ai': 'https://feeds.feedburner.com/kdnuggets-data-mining-analytics',
    'programming': 'https://dev.to/feed/',
    'cybersecurity': 'https://feeds.feedburner.com/TheHackersNews'
}

# Tweet settings
MAX_TWEET_LENGTH = 280
HASHTAGS = {
    'tech': ['#TechNews', '#Technology'],
    'ai': ['#AI', '#MachineLearning', '#DataScience'],
    'programming': ['#Programming', '#Coding', '#DevLife'],
    'cybersecurity': ['#CyberSecurity', '#InfoSec', '#Security']
}

# Scheduling settings
POSTING_SCHEDULE = {
    'news': '10:00,15:00,20:00',  # Post news at 10 AM, 3 PM, and 8 PM
    'ml': '12:00',                # Post ML snippet at noon
    'sentiment': '18:00'          # Post sentiment analysis at 6 PM
}

# Database settings
DB_FILENAME = 'tweet_history.db'

# Logging settings
LOG_FILENAME = 'bot.log'
LOG_LEVEL = 'INFO' 