from newspaper import Article

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text[:4000]
    except Exception as e:
        return f"Error: {e}"
