import tweepy
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API credentials from the environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Print (for debugging purposes; avoid printing sensitive info in production)
print(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN)

# Twitter handles
handles = [
    "cryptolyxe", "0xpepesso", "punk1685", "evecoins", "0xaegon_nft", "roaringkitty",
    "dipbandit", "mrwangdotprofit", "traderag_", "notanicecat69", "ztrader369",
    "alpinestar17", "ghost61occ", "smileycapital", "tonythebullbtc", "mrpurplenft",
    "jones__trader", "cryptoyusaku"
]

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def clean_text(text):
    """Remove URLs, mentions, hashtags, and special characters from text."""
    text = re.sub(r"http\S+|@\S+|#\S+|[^A-Za-z0-9 ]", "", text)
    return text.lower()

def fetch_tweets(handle, max_results=50):
    """Fetch tweets from a specific handle."""
    try:
        tweets = client.get_users_tweets(
            id=client.get_user(username=handle).data.id,
            max_results=max_results
        )
        return [clean_text(tweet.text) for tweet in tweets.data] if tweets.data else []
    except Exception as e:
        print(f"Error fetching tweets for {handle}: {e}")
        return []

def analyze_tweets(tweets):
    """Analyze tokens and narratives from tweets."""
    stop_words = set(stopwords.words("english"))
    all_words = []

    for tweet in tweets:
        tokens = word_tokenize(tweet)
        filtered_tokens = [word for word in tokens if word not in stop_words]
        all_words.extend(filtered_tokens)

    # Get most common words
    word_counts = Counter(all_words)
    return word_counts.most_common(20)

if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")
    
    results = {}

    for handle in handles:
        print(f"Fetching tweets for {handle}...")
        tweets = fetch_tweets(handle)
        print(f"Analyzing tweets for {handle}...")
        results[handle] = analyze_tweets(tweets)
    
    # Save results to a CSV file
    df = pd.DataFrame.from_dict(results, orient="index").transpose()
    df.to_csv("twitter_analysis.csv", index=False)

    print("Analysis complete. Results saved to twitter_analysis.csv.")