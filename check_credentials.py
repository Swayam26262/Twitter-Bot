import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_credentials():
    print("Checking Twitter API credentials...")

    # Get credentials from environment variables
    credentials = {
        "TWITTER_BEARER_TOKEN": os.getenv('TWITTER_BEARER_TOKEN'),
        "TWITTER_API_KEY": os.getenv('TWITTER_API_KEY'),
        "TWITTER_API_SECRET": os.getenv('TWITTER_API_SECRET'),
        "TWITTER_ACCESS_TOKEN": os.getenv('TWITTER_ACCESS_TOKEN'),
        "TWITTER_ACCESS_SECRET": os.getenv('TWITTER_ACCESS_SECRET')
    }

    # Check if all credentials are present
    missing = [key for key, value in credentials.items() if not value]
    if missing:
        print(f"❌ Missing credentials: {', '.join(missing)}")
        return False

    # Check credential lengths to ensure they're valid
    for key, value in credentials.items():
        if value and len(value) < 10:  # A simple validity check
            print(f"❌ Suspiciously short credential: {key}")
            return False

    # Try to verify credentials
    try:
        # Initialize Twitter client
        client = tweepy.Client(
            bearer_token=credentials["TWITTER_BEARER_TOKEN"],
            consumer_key=credentials["TWITTER_API_KEY"],
            consumer_secret=credentials["TWITTER_API_SECRET"],
            access_token=credentials["TWITTER_ACCESS_TOKEN"],
            access_token_secret=credentials["TWITTER_ACCESS_SECRET"]
        )
        
        # Test connection by getting own user info
        user_info = client.get_me()
        if user_info and user_info.data:
            print(f"✅ Authentication successful!")
            print(f"Connected as: @{user_info.data.username}")
            
            # Check write permissions
            print("Checking write permissions...")
            # We don't actually post, just check the scope
            auth = tweepy.OAuth1UserHandler(
                credentials["TWITTER_API_KEY"],
                credentials["TWITTER_API_SECRET"],
                credentials["TWITTER_ACCESS_TOKEN"],
                credentials["TWITTER_ACCESS_SECRET"]
            )
            api = tweepy.API(auth)
            
            # Check app permissions
            # Note: This is an approximation as v2 doesn't have a direct way to check this
            try:
                rate_limits = api.rate_limit_status()
                if "/statuses/update" in str(rate_limits):
                    print("✅ Write permissions appear to be available")
                else:
                    print("⚠️ Write permissions might be missing - check app permissions in Twitter Developer Portal")
            except:
                print("⚠️ Could not check write permissions - verify in Twitter Developer Portal")
                
            return True
        else:
            print("❌ Authentication failed. Valid credentials but couldn't retrieve user info.")
            return False
    
    except tweepy.TweepyException as e:
        print(f"❌ Authentication error: {e}")
        if "401" in str(e):
            print("   This is usually due to incorrect credentials or expired tokens.")
        elif "403" in str(e):
            print("   This is usually due to lack of permissions. Check your app permissions in Twitter Developer Portal.")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    check_credentials()
    print("\nTroubleshooting tips:")
    print("1. Make sure your .env file exists and has all required credentials")
    print("2. Check that your app has 'Read and Write' permissions in Twitter Developer Portal")
    print("3. Your account may be restricted if it's new or has violated Twitter's policies")
    print("4. You might need to regenerate your access tokens in Twitter Developer Portal") 