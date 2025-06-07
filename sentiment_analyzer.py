from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import streamlit as st

@st.cache_resource
def load_classifier():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return pipeline("text-classification", model=model, tokenizer=tokenizer)

def analyze_sentiment_batch(classifier, texts):
    results = classifier(texts, truncation=True)
    return [(r['label'], r['score']) for r in results]
