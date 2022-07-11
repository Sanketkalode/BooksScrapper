import requests
from bs4 import BeautifulSoup

url = 'https://www.goodreads.com/book/show/9.Unauthorized_Harry_Potter_Book_Seven_News'

response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

test = bs.find_all('div', {'class', 'review'})
name = test[1].find('a', {'class': 'left imgcol'})
date = test[1].find('a', {'class': 'reviewDate createdAt right'})
rating = test[1].find('span',{'class':'staticStars notranslate'})
review = test[1].find('div',{'class':'reviewText stacked'})
review = review.find_all('span')

# print(test[1])

print(name['title'])
print(date.text)
print(rating['title'])
print(review[0].text)


# from mongoengine import connect
#
# from app.models import Book
#
# connect(db='BooksDB', host='localhost', port=27017)
#
# book = Book.objects(bookID='1').first()
# # for i in book:
# #     print(i.title)
# print(book.bookID)