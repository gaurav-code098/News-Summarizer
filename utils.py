from newspaper import Article

# def extract_text_from_url(url):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         return article.text[:4000]
#     except Exception as e:
#         return f"Error: {e}"
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str) -> str:
    """
    Fetches text from a URL.
    This new version is smarter:
    1. It uses a User-Agent to identify as a browser.
    2. It only gets text from <p> paragraph tags.
    """
    try:
        # Set a User-Agent to pretend we are a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Failed to fetch {url}, status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all paragraph tags <p>
        # This is a much cleaner way to get article text
        paragraphs = soup.find_all('p')
        
        if not paragraphs:
            # Fallback if no <p> tags are found (less likely)
            print(f"Warning: No <p> tags found at {url}. Skipping.")
            return None

        # Join the text from all paragraphs
        article_text = " ".join([p.get_text(strip=True) for p in paragraphs])
        
        return article_text
    
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None