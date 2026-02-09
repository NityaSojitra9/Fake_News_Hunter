from newspaper import Article
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re

def extract_article_info(url):
    """
    Extract article information from a given URL using newspaper3k
    """
    try:
        # Download and parse the article
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()  # This extracts keywords, summary, etc.
        
        # Extract domain from URL
        domain = urlparse(url).netloc
        
        # Get publication date
        pub_date = article.publish_date
        
        # Get author (try multiple methods)
        author = article.authors[0] if article.authors else None
        
        # If no author found, try to extract from meta tags
        if not author:
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try different meta tags for author
                author_meta = soup.find('meta', {'name': 'author'}) or \
                             soup.find('meta', {'property': 'article:author'}) or \
                             soup.find('meta', {'name': 'twitter:creator'})
                
                if author_meta:
                    author = author_meta.get('content', '').strip()
            except:
                author = None
        
        return {
            'title': article.title or 'No title found',
            'content': article.text or 'No content found',
            'publication_date': pub_date,
            'author': author or 'Unknown',
            'source_domain': domain,
            'summary': article.summary,
            'keywords': article.keywords
        }
        
    except Exception as e:
        print(f"Error extracting article info: {str(e)}")
        # Return default values if extraction fails
        domain = urlparse(url).netloc
        return {
            'title': 'Error extracting title',
            'content': 'Error extracting content. Please check the URL.',
            'publication_date': None,
            'author': 'Unknown',
            'source_domain': domain,
            'summary': '',
            'keywords': []
        }

def clean_text(text):
    """
    Clean and preprocess text for ML analysis
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    return text.strip() 