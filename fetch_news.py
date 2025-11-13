import streamlit as st
import feedparser
from typing import List, Dict

# --- 1. NEW: Added YouTube Channel Feed ---
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
    
    # --- This is the new feed for YouTube Shorts ---
    "NDTV_Youtube": "https://www.youtube.com/feeds/videos.xml?channel_id=UCZg-fVlKMg8f-j1nL6ly-uA"
}

def parse_feed(feed_url: str, limit: int) -> List[Dict]:
    """Helper function to parse a feed and return a list of article dicts."""
    feed = feedparser.parse(feed_url)
    articles = []
    
    num_articles = min(len(feed.entries), limit)
    
    for entry in feed.entries[:num_articles]:
        articles.append({
            'title': entry.title,
            'summary': entry.summary,
            'link': entry.link,
            'published': entry.get('published', 'No date') 
        })
    return articles

# --- (Cached Functions: fetch_breaking_news & fetch_general_news are unchanged) ---

@st.cache_data(ttl="5m") # 5 Minute Cache
def fetch_breaking_news(feed_url: str) -> List[Dict]:
    """Fetches top 5 breaking news articles with a 5-minute cache."""
    print(f"--- FETCHING BREAKING NEWS (5 min TTL) from {feed_url} ---")
    return parse_feed(feed_url, limit=5)

@st.cache_data(ttl="30m") # 30 Minute Cache
def fetch_general_news(feed_url: str) -> List[Dict]:
    """Fetches top 15 general news articles with a 30-minute cache."""
    print(f"--- FETCHING GENERAL NEWS (30 min TTL) from {feed_url} ---")
    return parse_feed(feed_url, limit=15)


# --- 2. NEW: Special function just for YouTube Shorts ---

# In fetch_news.py

# ... (all your other code, including fetch_breaking_news and fetch_general_news) ...

# --- THIS IS THE FINAL, UPDATED FUNCTION ---
@st.cache_data(ttl="30m") # 30 Minute Cache
def fetch_youtube_shorts(feed_url: str, limit: int = 12) -> List[Dict]:
    """
    Fetches videos from a YouTube RSS feed, filters for shorts by
    checking the *thumbnail dimensions* (vertical = short),
    and returns their title, link, and thumbnail.
    """
    print(f"--- FETCHING YOUTUBE SHORTS (30 min TTL) from {feed_url} ---")
    feed = feedparser.parse(feed_url)
    shorts = []
    
    for entry in feed.entries:
        try:
            # --- THIS IS THE RELIABLE CHECK ---
            # We check the thumbnail dimensions.
            # A short is always vertical (height > width).
            
            if 'media_thumbnail' in entry and entry.media_thumbnail:
                thumbnail = entry.media_thumbnail[0]
                
                # Check if dimension data is available
                if 'height' in thumbnail and 'width' in thumbnail:
                    height = int(thumbnail['height'])
                    width = int(thumbnail['width'])
                    
                    if height > width: 
                        # It's a vertical video, so it's a Short!
                        shorts.append({
                            'title': entry.title,
                            'link': entry.link,
                            'thumbnail': thumbnail['url'] 
                        })
        
        except Exception as e:
            # Log the error but continue
            print(f"Could not parse video entry: {entry.title}. Error: {e}")

        # Stop once we have enough shorts
        if len(shorts) >= limit:
            break
            
    return shorts
