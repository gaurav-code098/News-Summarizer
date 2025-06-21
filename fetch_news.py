import feedparser

RSS_FEEDS = {
    "NDTV": "https://feeds.feedburner.com/ndtvnews-india-news",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Indian Express": "https://indianexpress.com/section/india/feed/",
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "CNN World": "http://rss.cnn.com/rss/edition_world.rss",
    "Reuters World": "http://feeds.reuters.com/Reuters/worldNews",
    "The Guardian World": "https://www.theguardian.com/world/rss",
    "NY Times World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
}

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
