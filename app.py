import streamlit as st
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from newsscraper import find_page_for_date, get_articles_by_page
from sentiment_analyzer import analyze_sentiment
import yfinance as yf
from visualizations import plot_sentiment_distribution, plot_sentiment_scores

st.set_page_config(page_title="Stock News Sentiment Analysis", layout="wide")
sns.set_theme(style="whitegrid")

st.markdown(
    "<h1 style='text-align: center; color: #FFFFFF;'>Stock News Sentiment Analysis</h1>",
    unsafe_allow_html=True
)

st.markdown("### 📥 Input")

if 'ticker_list' not in st.session_state:
    st.session_state.ticker_list = []

new_ticker = st.text_input("Enter Stock Ticker:", "")

if st.button("Add Ticker"):
    if new_ticker:
        st.session_state.ticker_list.append(new_ticker.strip().upper())
        st.rerun()

st.markdown("#### Selected Tickers:")
if st.session_state.ticker_list:
    st.markdown(", ".join([f"`{ticker}`" for ticker in st.session_state.ticker_list]))
else:
    st.info("No tickers added yet.")

if st.button("Clear Tickers"):
    st.session_state.ticker_list = []
    st.rerun()

tickers = st.session_state.ticker_list
target_date = st.date_input("Target Date (in YYYY/MM/DD)", value=None)

if st.button("🔍 Search News"):
    if not target_date:
        st.warning("Please select a date before searching.")
    else:
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

            st.markdown("### 📈 Summary Statistics")
            summary = master_df.groupby('Ticker')['Sentiment'].value_counts().unstack().fillna(0)
            st.dataframe(summary)

            tab1, tab2, tab3 = st.tabs(["📰 News Articles", "📊 Sentiment Distribution", "📈 Sentiment Scores"])

            with tab1:
                st.markdown("### 📰 News Articles")
                st.dataframe(master_df, height=400)

            with tab2:
                st.markdown("### 📊 Sentiment Distribution by Ticker")
                fig1 = plot_sentiment_distribution(master_df)
                st.pyplot(fig1)

                with tab3:
                    st.markdown("### 📈 Sentiment Scores by Article")

                    if (master_df['Ticker'].nunique() > 1):
                        top_dfs = []
                        for ticker in master_df['Ticker'].unique():
                            ticker_df = master_df[master_df['Ticker'] == ticker]
                            top_ticker_df = ticker_df.sort_values(by='Score', ascending=False).head(20)
                            top_dfs.append(top_ticker_df)
                        top_df = pd.concat(top_dfs, ignore_index=True)
                    else:
                        top_df = master_df.sort_values(by='Score', ascending=False).head(20)

                    fig2 = plot_sentiment_scores(top_df)
                    st.pyplot(fig2)