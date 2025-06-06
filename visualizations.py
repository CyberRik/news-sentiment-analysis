# visualizations.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
