import streamlit as st
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from newsscraper import find_page_for_date, get_articles_by_page
from sentiment_analyzer import analyze_sentiment
import yfinance as yf

st.set_page_config(page_title="Stock News Sentiment Analysis", layout="wide")
sns.set_theme(style="whitegrid")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #FFFFFF;'>Stock News Sentiment Analysis</h1>",
    unsafe_allow_html=True
)

# Input Section (full width)
st.markdown("### 📥 Input")
tickers_input = st.text_input("Stock Tickers (comma-separated, e.g. AAPL, TSLA, MSFT)", value="")
target_date = st.date_input("Target Date", value=None)

if st.button("🔍 Search News"):
    if not target_date:
        st.warning("Please select a date before searching.")
    else:
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
        master_df = pd.DataFrame()

        for ticker in tickers:
            try:
                company_name = yf.Ticker(ticker).info.get('shortname', " ")
            except Exception as e:
                st.error(f"Error fetching data for {ticker}: {e}")
                continue

            if company_name:
                display_name = f"{ticker} - {company_name}"
            else:
                display_name = ticker

            st.markdown(f"**Searching news for {display_name} on {target_date.strftime('%m/%d/%Y')}**")
            with st.spinner(f"Fetching articles for {ticker}..."):
                page_number = find_page_for_date(ticker, target_date.strftime('%m/%d/%Y'))
                if not page_number:
                    st.warning(f"No articles found for {ticker} on {target_date.strftime('%m/%d/%Y')}.")
                    continue

                articles = get_articles_by_page(ticker, page_number)
                data = []
                for date_str, title, source in articles:
                    try:
                        label, score = analyze_sentiment(title)
                    except Exception as e:
                        st.error(f"Error analyzing sentiment for article '{title}': {e}")
                        label, score = "Unknown", 0.0
                    data.append({
                        'Ticker': ticker,
                        'Date': date_str,
                        'Title': title,
                        'Source': source,
                        'Sentiment': label,
                        'Score': score
                    })

                ticker_df = pd.DataFrame(data)
                master_df = pd.concat([master_df, ticker_df], ignore_index=True)

        if master_df.empty:
            st.error("No articles found for any of the provided tickers.")
        else:
            st.markdown("## 📊 Sentiment Analysis Results")

            # Summary stats
            st.markdown("### 📈 Summary Statistics")
            summary = master_df.groupby('Ticker')['Sentiment'].value_counts().unstack().fillna(0)
            st.dataframe(summary)

            tab1, tab2, tab3 = st.tabs(["📰 News Articles", "📊 Sentiment Distribution", "📈 Sentiment Scores"])

            with tab1:
                st.markdown("### 📰 News Articles")
                st.dataframe(master_df, height=400)

            with tab2:
                st.markdown("### 📊 Sentiment Distribution by Ticker")
                sentiment_counts = master_df.groupby(['Ticker', 'Sentiment']).size().reset_index(name='Count')
                fig1, ax1 = plt.subplots(figsize=(8, 4))
                sns.barplot(
                    data=sentiment_counts,
                    x='Ticker',
                    y='Count',
                    hue='Sentiment',
                    palette={'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
                )
                ax1.set_title('Sentiment Distribution by Ticker', fontsize=14)
                ax1.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
                st.pyplot(fig1)

            with tab3:
                st.markdown("### 📈 Sentiment Scores by Article")
                max_title_length = 50
                master_df['Truncated_Title'] = master_df['Title'].apply(
                    lambda x: x if len(x) <= max_title_length else x[:max_title_length] + '...'
                )
                fig_height = min(10, len(master_df) * 0.25)
                fig2, ax2 = plt.subplots(figsize=(8, fig_height))
                sns.barplot(
                    x='Score',
                    y='Truncated_Title',
                    data=master_df,
                    hue='Ticker',
                    dodge=False,
                    palette='Set2'
                )
                ax2.set_xlabel('Sentiment Score', fontsize=10)
                ax2.set_ylabel('Article Title', fontsize=10)
                ax2.set_title('Sentiment Scores by Article', fontsize=14)
                ax2.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                st.pyplot(fig2)
