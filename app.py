import streamlit as st
import pandas as pd
import numpy as np
import datetime

from newsscraper import find_page_for_date, get_articles_by_page
from sentiment_analyzer import analyze_sentiment

st.title("Stock News sentiment analysis")

st.subheader("Step 1: Input")
ticker = st.text_input("Enter the stock ticker (e.g. AAPL, TSLA,etc)")
target_date = st.date_input("Enter the target date (MM/DD/YYYY)")

if st.button("Search news"):
    st.write(f"Searching news for {ticker} on {target_date.strftime('%m/%d/%Y')}")

    with st.spinner("Fetching articles..."):
        page_number = find_page_for_date(ticker, target_date.strftime('%m/%d/%Y'))

        if not page_number:
            st.error("No articles found for the given date.")
        else:
            articles = get_articles_by_page(ticker, page_number)

            data = []
            for date_str, title, source in articles:
                label , score = analyze_sentiment(title)
                data.append({
                    'Date': date_str,
                    'Title': title,
                    'Source': source,
                    'Sentiment': label,
                    'Score': score
                })

            df = pd.DataFrame(data)

                    



            


