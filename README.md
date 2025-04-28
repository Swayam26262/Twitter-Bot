# Advanced Twitter Bot for Tech Content

A professional Twitter bot that automatically posts tech news, machine learning code snippets, programming tips, and sentiment analysis on trending topics.

## Features

- **Multi-category News Posting**: Automatically fetches and posts news from various tech-related RSS feeds
- **ML Code Snippets**: Shares educational code snippets about machine learning and data science
- **Sentiment Analysis**: Analyzes Twitter sentiment on trending topics and posts visualized results
- **Content Database**: Maintains a content database with various types of tech-related content
- **Automated Scheduling**: Posts content on customizable schedules
- **SQLite Database**: Tracks all posted tweets and engagement metrics
- **Analytics**: Generates detailed performance reports with visualizations
- **Advanced Logging**: Comprehensive logging system for monitoring and debugging
- **Unit Tests**: Thorough test suite for all components

## Architecture

The project follows a modular design with clear separation of concerns:

- `bot.py` - Main Twitter bot class and command-line interface
- `config.py` - Configuration settings and environment variables
- `database.py` - SQLite database for storing tweet history and analytics
- `logger.py` - Logging configuration
- `scheduler.py` - Automated scheduling of tweets
- `sentiment.py` - Sentiment analysis of trending topics
- `content_generator.py` - Generation of ML snippets and code tips
- `analytics.py` - Performance tracking and report generation
- `test_bot.py` - Unit tests

## Getting Started

### Prerequisites

- Python 3.8+
- Twitter Developer Account with API v2 access

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Swayam26262/Twitter-Bot
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:

Create a `.env` file in the project root with the following:

```
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

### Usage

The bot can be run in different modes:

#### Post a Single Tweet

```bash
# Post tech news
python bot.py run --type news --category tech

# Post ML snippet
python bot.py run --type ml

# Post coding tip
python bot.py run --type code_tip

# Post interview question
python bot.py run --type interview

# Post sentiment analysis on trending topic
python bot.py run --type sentiment
```

#### Run Scheduled Mode

```bash
python bot.py schedule
```

This will start the scheduler, which will post tweets according to the schedule defined in `config.py`.

#### Generate Analytics Report

```bash
python bot.py report
```

#### Interactive Mode

```bash
python bot.py post
```

#### Run Tests

```bash
python -m pytest test_bot.py
```

## Customization

You can customize the bot by modifying the following:

- **News Sources**: Add or modify RSS feeds in `config.py`
- **Tweet Schedule**: Adjust posting times in `config.py`
- **Content Database**: Add new content to the JSON files in the `content` directory
- **Hashtags**: Modify hashtags for each category in `config.py`

## Technical Details

- Uses Twitter API v2 through the Tweepy library
- Implements sentiment analysis using TextBlob
- Generates visualizations with Matplotlib
- Stores data in SQLite database
- Schedules posts using the Schedule library
- Implements proper error handling and retry mechanisms
- Comprehensive logging for monitoring and debugging

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Tweepy](https://www.tweepy.org/)
- [TextBlob](https://textblob.readthedocs.io/)
- [Schedule](https://schedule.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)
- [Feedparser](https://feedparser.readthedocs.io/) 