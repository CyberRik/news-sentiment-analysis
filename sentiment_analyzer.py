from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def analyze_sentiment(text):
    result = classifier(text)
    return result[0]['label'], result[0]['score']
