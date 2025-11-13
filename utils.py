import requests
from bs4 import BeautifulSoup

# --- NEW: Import the newspaper library ---
from newspaper import Article, Config

def extract_text_from_url(url: str) -> str:
    """
    Fetches text from a URL using the newspaper3k library,
    which is much more robust against modern news sites.
    """
    try:
        # --- 1. Set up configuration (to act like a browser) ---
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # --- 2. Create the Article object ---
        article = Article(url, config=config)
        
        # --- 3. Download and parse the article ---
        article.download()
        article.parse()
        
        # --- 4. Return the clean text ---
        return article.text
    
    except Exception as e:
        print(f"--- NEWSPAPER3K FAILED to extract text from {url}. Error: {e} ---")
        # Fallback to our old, simple scraper (just in case)
        try:
            headers = {'User-Agent': config.browser_user_agent}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200: return None
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all('p')
            if not paragraphs: return None
            article_text = " ".join([p.get_text(strip=True) for p in paragraphs])
            return article_text
        except Exception as e2:
            print(f"--- SIMPLE SCRAPER ALSO FAILED. Error: {e2} ---")
            return None
