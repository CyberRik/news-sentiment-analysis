
# Stock News Sentiment Analysis

This repository provides an interactive web application built with **Streamlit** for performing sentiment analysis on stock news articles. The app analyzes news articles related to selected stock tickers and assesses sentiment using the **FinBERT** model for financial news sentiment analysis.

### Key Features:
- **Search for News Articles**: Search for stock news articles by stock ticker and date.
- **Sentiment Analysis**: Perform sentiment analysis on the articles to classify them as positive, negative, or neutral.
- **Visualization**: Display sentiment distribution and sentiment scores for the selected stock tickers.

## Technologies Used

- **Python**
- **Streamlit**: For the interactive user interface.
- **FinBERT**: A transformer model for sentiment analysis on financial texts.
- **BeautifulSoup**: For scraping news articles from Business Insider.
- **Matplotlib & Seaborn**: For visualizing sentiment distribution and sentiment scores.
- **YFinance**: For fetching stock ticker information.
- **Pandas**: For data manipulation and processing.
- **Requests**: For making HTTP requests to fetch articles.
- **Torch**: For model loading and processing.

## How to Run the App Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-news-sentiment-analysis.git
   ```

2. Navigate into the project directory:
   ```bash
   cd stock-news-sentiment-analysis
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Open your browser and go to `http://localhost:8501` to start using the Stock News Sentiment Analysis tool.

## Files in the Repository

- **`app.py`**: Main application file that runs the Streamlit app, handles user input, and displays results.
- **`sentiment_analyzer.py`**: Contains the sentiment analysis model loading and prediction functions using FinBERT.
- **`visualizations.py`**: Functions for visualizing sentiment distribution and sentiment scores.
- **`newsscraper.py`**: Functions for scraping news articles related to stock tickers from Business Insider.
- **`requirements.txt`**: List of required Python libraries for this project.
- **`README.md`**: Documentation for the repository.

## How the App Works

1. **Ticker Selection**: Users can input stock tickers and add them to the list of tickers to track.
2. **Search News**: After selecting a date, the app searches for news articles related to the selected tickers and date.
3. **Sentiment Analysis**: Each article is analyzed for sentiment using the FinBERT model, which classifies the article as positive, negative, or neutral.
4. **Visualization**:
   - **Sentiment Distribution**: A bar chart displaying the sentiment distribution for each stock ticker.
   - **Sentiment Scores**: A bar chart displaying the sentiment scores of the top articles for each ticker.

## Example Usage

1. Input stock tickers such as `AAPL`, `TSLA`, or `GOOG`.
2. Select a target date for the news search.
3. Click **Search News** to retrieve news articles for the selected tickers and date.
4. View the sentiment analysis results and visualizations for the selected tickers.

![Sentiment Distribution](images/sentiment_distribution.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this repository and submit pull requests for improvements or fixes. If you encounter any issues, please open an issue in the repository.

---

Made with ❤️ by [CyberRik]https://github.com/CyberRik)

