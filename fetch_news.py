import streamlit as st
import feedparser
from typing import List, Dict

RSS_FEEDS = {
    "NDTV": "https://feeds.feedburner.com/ndtvnews-india-news",
    "Times of India": "https://timesofindia.indimes.com/rssfeeds/-2128936835.cms",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Indian Express": "https://indianexpress.com/section/india/feed/",
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "The Guardian World": "https://www.theguardian.com/world/rss",
    "NY Times World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Reuters Top News": "http://feeds.reuters.com/reuters/topNews",
    "TechCrunch": "https://techcrunch.com/feed/",
    "Financial_Express": "httpss://www.financialexpress.com/feed/",
}

# In fetch_news.py

def parse_feed(feed_url: str, limit: int) -> List[Dict]:
    """Helper function to parse a feed and return a list of article dicts."""
    feed = feedparser.parse(feed_url)
    articles = []
    
    if not feed.entries:
        print(f"--- WARNING: No entries found in feed: {feed_url} ---")
        return [] # Return empty list immediately
        
    # Use min() to avoid errors if the feed has fewer articles than the limit
    num_to_fetch = min(len(feed.entries), limit)
    
    for entry in feed.entries[:num_to_fetch]:
        try:
            # --- THIS IS THE FIX ---
            # We now use .get() for *everything* to prevent crashes
            # If a field is missing, it uses a fallback (e.g., 'No Title')
            
            title = entry.get('title', 'No Title Provided')
            link = entry.get('link', '#') # '#' is a safe fallback link
            summary = entry.get('summary', entry.get('description', ''))
            published = entry.get('published', 'No date')
            
            articles.append({
                'title': title,
                'summary': summary,
                'link': link,
                'published': published
            })
        except Exception as e:
            # This will catch any unexpected errors with a single article
            # and allow the loop to continue.
            print(f"--- ERROR: Skipping malformed article. Error: {e} ---")
            continue # Go to the next article
            
    return articles

@st.cache_data(ttl="5m") # 5 Minute Cache
def fetch_breaking_news(feed_url: str) -> List[Dict]:
    """Fetches top 5 breaking news articles with a 5-minute cache."""
    print(f"--- FETCHING BREAKING NEWS (5 min TTL) from {feed_url} ---")
    return parse_feed(feed_url, limit=10)

@st.cache_data(ttl="30m") # 30 Minute Cache
def fetch_general_news(feed_url: str) -> List[Dict]:
    """Fetches top 15 general news articles with a 30-minute cache."""
    print(f"--- FETCHING GENERAL NEWS (30 min TTL) from {feed_url} ---")
    return parse_feed(feed_url, limit=15)
