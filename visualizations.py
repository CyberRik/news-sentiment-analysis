# visualizations.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import yfinance as yf
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def plot_sentiment_distribution(master_df):
    sentiment_counts = master_df.groupby(['Ticker', 'Sentiment']).size().reset_index(name='Count')
    fig, ax = plt.subplots(figsize=(6, 3))

    sns.barplot(
        data=sentiment_counts,
        x='Ticker',
        y='Count',
        hue='Sentiment',
        palette={'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'},
        ax=ax
    )

    # Adjust bar widths
    for patch in ax.patches:
        current_width = patch.get_width()
        patch.set_width(current_width * 0.6)
        patch.set_x(patch.get_x() + (current_width * 0.2))

    ax.set_xlabel('Ticker', fontsize=8)
    ax.set_ylabel('Count', fontsize=8)
    ax.tick_params(axis='x', labelsize=7, rotation=45)
    ax.tick_params(axis='y', labelsize=7)
    ax.set_title('Sentiment Distribution by Ticker', fontsize=10)
    ax.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7, title_fontsize=8)

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    ax.grid(axis='y', linestyle='--', alpha=0.5)
    return fig

def plot_sentiment_scores(top_df):
    max_title_length = 25
    top_df['Truncated_Title'] = top_df['Title'].apply(
        lambda x: x if len(x) <= max_title_length else x[:max_title_length] + '...'
    )

    fig_height = min(10, len(top_df) * 0.25)
    fig, ax = plt.subplots(figsize=(8, fig_height))

    sns.barplot(
        x='Score',
        y='Truncated_Title',
        data=top_df,
        hue='Ticker',
        dodge=False,
        palette='Set2',
        ax=ax
    )

    bar_height = 0.4
    for patch in ax.patches:
        patch.set_height(bar_height)

    ax.set_xlabel('Sentiment Score', fontsize=8)
    ax.set_ylabel('Article Title', fontsize=8)
    ax.set_title('Sentiment Scores by Article', fontsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.tick_params(axis='x', labelsize=8)
    ax.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    return fig

def plot_sentiment_vs_price(ticker, target_date, articles_df):
    # Define date range: 2 days before, 2 days after
    start_date = target_date - datetime.timedelta(days=2)
    end_date = target_date + datetime.timedelta(days=2)

    # Fetch stock price data
    stock_data = yf.download(ticker, start=start_date, end=end_date + datetime.timedelta(days=1))  # +1 to include end date
    stock_data = stock_data['Close'].reset_index()

    # Ensure date format compatibility
    stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.date

    # Filter and group sentiment data
    df = articles_df[articles_df['Ticker'] == ticker].copy()
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    sentiment_daily = df[df['Date'].between(start_date, end_date)].groupby('Date')['Score'].mean().reset_index()

    # Create a full date range
    full_range = pd.date_range(start=start_date, end=end_date).date
    sentiment_daily = sentiment_daily.set_index('Date').reindex(full_range).rename_axis('Date').reset_index()
    
    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot stock price
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price", color='tab:blue')
    ax1.plot(stock_data['Date'], stock_data['Close'], marker='o', color='tab:blue', label="Stock Price")
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Add vertical line for target date
    ax1.axvline(target_date, color='gray', linestyle='--', label="Target Date")

    # Plot sentiment on secondary axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Avg Sentiment Score", color='tab:red')
    ax2.plot(sentiment_daily['Date'], sentiment_daily['Score'], marker='s', linestyle='-', color='tab:red', label="Sentiment Score")
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Title
    plt.title(f"{ticker}: Sentiment vs Stock Price ({start_date} to {end_date})")
    fig.tight_layout()
    return fig