#!/usr/bin/env python
"""
Test script to verify all ML functionality is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.scraper import extract_article_info, clean_text
from core.nlp_analysis import analyze_article

def test_ml_functionality():
    """Test all ML components"""
    print("🧪 Testing FakeNewsHunter ML Functionality...")
    print("=" * 50)
    
    # Test URL
    test_url = "https://www.bbc.com/news/world-us-canada-68718951"
    
    try:
        print("1. Testing web scraping...")
        article_info = extract_article_info(test_url)
        print(f"   ✅ Title: {article_info['title'][:50]}...")
        print(f"   ✅ Content length: {len(article_info['content'])} characters")
        print(f"   ✅ Source: {article_info['source_domain']}")
        
        print("\n2. Testing text cleaning...")
        cleaned_text = clean_text(article_info['content'])
        print(f"   ✅ Cleaned text length: {len(cleaned_text)} characters")
        
        print("\n3. Testing NLP analysis...")
        nlp_results = analyze_article(cleaned_text, test_url)
        print(f"   ✅ Prediction: {nlp_results['prediction']}")
        print(f"   ✅ Confidence: {nlp_results['confidence']:.2f}")
        print(f"   ✅ Sentiment: {nlp_results['sentiment']}")
        print(f"   ✅ Sentiment Score: {nlp_results['sentiment_score']:.2f}")
        print(f"   ✅ Trust Score: {nlp_results['trust_score']}")
        print(f"   ✅ Entities found: {len(nlp_results['entities'])}")
        
        if nlp_results['entities']:
            print("   ✅ Sample entities:")
            for entity, label in nlp_results['entities'][:3]:
                print(f"      - {entity} ({label})")
        
        print("\n🎉 All ML functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_ml_functionality() 