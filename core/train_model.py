import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    """
    Clean and preprocess text for ML training
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

def create_sample_dataset():
    """
    Create a sample dataset for training (in real scenario, you'd use actual data)
    """
    # Sample fake news texts (indicators of fake news)
    fake_texts = [
        "BREAKING: Shocking discovery that will change everything! You won't believe what happened next!",
        "Scientists discover miracle cure that big pharma doesn't want you to know about!",
        "This one weird trick will solve all your problems instantly!",
        "Celebrity spotted doing something outrageous - click here to see!",
        "Government conspiracy revealed - they've been hiding this from you!",
        "Amazing weight loss secret that doctors hate!",
        "This simple home remedy cures cancer in 24 hours!",
        "Shocking video shows aliens visiting Earth - real footage!",
        "Make money fast with this guaranteed method!",
        "This ancient secret will transform your life overnight!"
    ]
    
    # Sample real news texts (indicators of real news)
    real_texts = [
        "New study published in Nature journal shows promising results for renewable energy.",
        "Local government announces plans to improve public transportation infrastructure.",
        "Economic report indicates steady growth in manufacturing sector.",
        "Research team discovers new species of marine life in Pacific Ocean.",
        "Weather forecast predicts rain for the weekend with temperatures in the 60s.",
        "City council approves budget for new community center construction.",
        "Scientists develop new method for recycling plastic waste.",
        "Local business owner opens new restaurant downtown.",
        "School district announces new educational programs for students.",
        "Healthcare providers implement new safety protocols for patient care."
    ]
    
    # Create DataFrame
    data = []
    for text in fake_texts:
        data.append({'text': text, 'label': 'Fake'})
    for text in real_texts:
        data.append({'text': text, 'label': 'Real'})
    
    return pd.DataFrame(data)

def train_fake_news_model():
    """
    Train a fake news detection model
    """
    print("Creating sample dataset...")
    df = create_sample_dataset()
    
    print("Cleaning text data...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Split the data
    X = df['cleaned_text']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training TF-IDF vectorizer...")
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.9
    )
    
    # Fit and transform training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print("Training Logistic Regression model...")
    # Train the model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_tfidf, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_tfidf)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    print("Saving model and vectorizer...")
    joblib.dump(model, 'fake_news_model.joblib')
    joblib.dump(vectorizer, 'vectorizer.joblib')
    
    print("Model training completed!")
    return model, vectorizer

if __name__ == "__main__":
    train_fake_news_model() 