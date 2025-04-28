import sqlite3
import os
import datetime
from config import DB_FILENAME

class TweetDatabase:
    def __init__(self):
        self.db_file = DB_FILENAME
        self.init_db()
    
    def init_db(self):
        """Initialize the database if it doesn't exist"""
        if not os.path.exists(self.db_file):
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            # Create tweets table
            c.execute('''
            CREATE TABLE tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT,
                content TEXT,
                category TEXT,
                post_time TIMESTAMP,
                engagement_likes INTEGER DEFAULT 0,
                engagement_retweets INTEGER DEFAULT 0
            )
            ''')
            
            # Create analytics table
            c.execute('''
            CREATE TABLE analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                posts_count INTEGER,
                avg_engagement REAL
            )
            ''')
            
            conn.commit()
            conn.close()
    
    def add_tweet(self, tweet_id, content, category):
        """Add a new tweet to the database"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        current_time = datetime.datetime.now()
        c.execute('''
        INSERT INTO tweets (tweet_id, content, category, post_time)
        VALUES (?, ?, ?, ?)
        ''', (tweet_id, content, category, current_time))
        
        conn.commit()
        conn.close()
    
    def update_engagement(self, tweet_id, likes, retweets):
        """Update engagement metrics for a tweet"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        c.execute('''
        UPDATE tweets
        SET engagement_likes = ?, engagement_retweets = ?
        WHERE tweet_id = ?
        ''', (likes, retweets, tweet_id))
        
        conn.commit()
        conn.close()
    
    def get_tweet_history(self, limit=10):
        """Get the most recent tweets"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''
        SELECT * FROM tweets
        ORDER BY post_time DESC
        LIMIT ?
        ''', (limit,))
        
        result = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return result
    
    def get_category_stats(self):
        """Get stats on tweet performance by category"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''
        SELECT category, 
               COUNT(*) as tweet_count,
               AVG(engagement_likes + engagement_retweets) as avg_engagement
        FROM tweets
        GROUP BY category
        ''')
        
        result = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return result 