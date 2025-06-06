import requests
from bs4 import BeautifulSoup
import datetime

def get_articles_by_page(ticker: str, page: int):
    url = f'https://markets.businessinsider.com/news/{ticker.lower()}-stock?p={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = []
    for article in soup.find_all('div', class_='latest-news__story'):
        date_str = article.find('time', class_='latest-news__date').get('datetime')
        title = article.find('a', class_='news-link').text.strip()
        source = article.find('span', class_='latest-news__source').text.strip()
        articles.append((date_str, title, source))
    return articles

def find_page_for_date(ticker, target_date, max_pages=200):
    target_date = datetime.datetime.strptime(target_date, '%m/%d/%Y')
    left, right = 1, max_pages

    while left <= right:
        mid = (left + right) // 2
        articles = get_articles_by_page(ticker, mid)
        dates = [datetime.datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p') for date, _, _ in articles]

        if not dates:
            right = mid - 1
            continue

        if any(d.date() == target_date.date() for d in dates):
            return mid

        if dates[0].date() > target_date.date():
            left = mid + 1
        elif dates[-1].date() < target_date.date():
            right = mid - 1

    return None
