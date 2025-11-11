import feedparser

RSS_FEEDS = {
    "NDTV": "https://feeds.feedburner.com/ndtvnews-india-news",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Indian Express": "https://indianexpress.com/section/india/feed/",
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "The Guardian World": "https://www.theguardian.com/world/rss",
    "NY Times World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Reuters Top News": "http://feeds.reuters.com/reuters/topNews",
    "TechCrunch": "https://techcrunch.com/feed/",
  
}
import streamlit as st
import feedparser
from typing import List, Dict

# Your original RSS_FEEDS dictionary
# I'm adding Reuters for a "breaking news" example



def parse_feed(feed_url: str, limit: int) -> List[Dict]:
    """Helper function to parse a feed and return a list of article dicts."""
    feed = feedparser.parse(feed_url)
    articles = []
    
    # Use min() to avoid errors if the feed has fewer articles than the limit
    num_articles = min(len(feed.entries), limit)
    
    for entry in feed.entries[:num_articles]:
        articles.append({
            'title': entry.title,
            'summary': entry.summary,
            'link': entry.link,
            # .get() is safer, in case 'published' doesn't exist
            'published': entry.get('published', 'No date') 
        })
    return articles

# --- NEW CACHED FUNCTIONS ---

@st.cache_data(ttl="5m") # 5 Minute Cache
def fetch_breaking_news(feed_url: str) -> List[Dict]:
    """Fetches top 5 breaking news articles with a 5-minute cache."""
    print(f"--- FETCHING BREAKING NEWS (5 min TTL) from {feed_url} ---")
    return parse_feed(feed_url, limit=7)

@st.cache_data(ttl="30m") # 30 Minute Cache
def fetch_general_news(feed_url: str) -> List[Dict]:
    """Fetches top 15 general news articles with a 30-minute cache."""
    print(f"--- FETCHING GENERAL NEWS (30 min TTL) from {feed_url} ---")
    return parse_feed(feed_url, limit=15)

def get_articles(feed_url, max_articles=10):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "published": entry.get("published", ""),
        })
    return articles
