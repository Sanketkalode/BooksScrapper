import pandas as pd
import requests
from bs4 import BeautifulSoup
from mongoengine import connect

from app.ops import get_index, create
from app.scrape import get_bookUrl


def main(counter):
    books = pd.read_csv('files/books.csv', error_bad_lines=False)
    url = 'https://www.goodreads.com/book/show/'
    connect(db='BooksDB', host='3.95.164.183', port=27016)
    book_index = get_index()
    count = 0

    for index, row in books.iterrows():
        try:
            if index >= book_index:
                print('Visiting: ', row['title'])
                book_url = get_bookUrl(url, row['bookID'], row['title'])
                response = requests.get(book_url)
                bs = BeautifulSoup(response.text, 'html.parser')
                create(bs, row, book_url)
                count=1

            if count == counter:
                break

        except Exception as e:
            print(row['title'])
            print(e.with_traceback())
            pass
