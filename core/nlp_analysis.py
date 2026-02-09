import joblib
import re
from textblob import TextBlob
import spacy
from urllib.parse import urlparse
import requests

# Load spaCy model (will download if not available)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def clean_text_for_ml(text):
    """
    Clean text for ML prediction
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def predict_fake_news(text):
    """
    Predict if text is fake news using trained model
    """
    try:
        # Load the trained model and vectorizer
        model = joblib.load('fake_news_model.joblib')
        vectorizer = joblib.load('vectorizer.joblib')
        
        # Clean the text
        cleaned_text = clean_text_for_ml(text)
        
        # Transform text using the vectorizer
        text_vectorized = vectorizer.transform([cleaned_text])
        
        # Make prediction
        prediction = model.predict(text_vectorized)[0]
        confidence = max(model.predict_proba(text_vectorized)[0])
        
        return prediction, confidence
        
    except Exception as e:
        print(f"Error in ML prediction: {str(e)}")
        # Fallback to simple heuristics
        return predict_fake_news_heuristic(text)

def predict_fake_news_heuristic(text):
    """
    Simple heuristic-based fake news detection
    """
    if not text:
        return "Unknown", 0.5
    
    text_lower = text.lower()
    
    # Indicators of fake news
    fake_indicators = [
        'breaking', 'shocking', 'miracle', 'secret', 'conspiracy',
        'you won\'t believe', 'click here', 'one weird trick',
        'doctors hate', 'big pharma', 'government hiding',
        'guaranteed', 'overnight', 'instant', 'cure cancer',
        'aliens', 'ancient secret', 'transform your life'
    ]
    
    # Indicators of real news
    real_indicators = [
        'study', 'research', 'published', 'journal', 'scientists',
        'government announces', 'local', 'official', 'report',
        'according to', 'experts say', 'data shows', 'analysis'
    ]
    
    fake_score = sum(1 for indicator in fake_indicators if indicator in text_lower)
    real_score = sum(1 for indicator in real_indicators if indicator in text_lower)
    
    if fake_score > real_score:
        confidence = min(0.9, 0.5 + (fake_score * 0.1))
        return "Fake", confidence
    elif real_score > fake_score:
        confidence = min(0.9, 0.5 + (real_score * 0.1))
        return "Real", confidence
    else:
        return "Uncertain", 0.5

def analyze_sentiment(text):
    """
    Analyze sentiment using TextBlob
    """
    if not text:
        return "Neutral", 0.0
    
    try:
        blob = TextBlob(text)
        # Some linters may not recognize .polarity, but it is a valid property of TextBlob's sentiment
        sentiment_score = float(getattr(blob.sentiment, 'polarity', 0.0))
        
        if sentiment_score > 0.1:
            sentiment = "Positive"
        elif sentiment_score < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return sentiment, sentiment_score
        
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        return "Neutral", 0.0

def extract_entities(text):
    """
    Extract named entities using spaCy
    """
    if not text:
        return []
    
    try:
        doc = nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        
        return entities[:10]  # Limit to top 10 entities
        
    except Exception as e:
        print(f"Error in entity extraction: {str(e)}")
        return []

def get_trust_score(domain):
    """
    Get trust score for a domain (simplified version)
    """
    if not domain:
        return "Unknown"
    
    # Known trusted domains
    trusted_domains = [
        'reuters.com', 'ap.org', 'bbc.com', 'cnn.com', 'nytimes.com',
        'washingtonpost.com', 'npr.org', 'pbs.org', 'abcnews.go.com',
        'cbsnews.com', 'nbcnews.com', 'foxnews.com', 'usatoday.com'
    ]
    
    # Known unreliable domains
    unreliable_domains = [
        'infowars.com', 'breitbart.com', 'naturalnews.com',
        'beforeitsnews.com', 'veteranstoday.com', 'whatreallyhappened.com'
    ]
    
    domain_lower = domain.lower()
    
    if domain_lower in trusted_domains:
        return "High"
    elif domain_lower in unreliable_domains:
        return "Low"
    else:
        return "Medium"

def analyze_article(text, url=None):
    """
    Complete article analysis combining all NLP techniques
    """
    if not text:
        return {
            'prediction': 'Unknown',
            'confidence': 0.0,
            'sentiment': 'Neutral',
            'sentiment_score': 0.0,
            'entities': [],
            'trust_score': 'Unknown'
        }
    
    # Get domain for trust score
    domain = urlparse(url).netloc if url else None
    
    # Run all analyses
    prediction, confidence = predict_fake_news(text)
    sentiment, sentiment_score = analyze_sentiment(text)
    entities = extract_entities(text)
    trust_score = get_trust_score(domain)
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'sentiment': sentiment,
        'sentiment_score': sentiment_score,
        'entities': entities,
        'trust_score': trust_score
    } 