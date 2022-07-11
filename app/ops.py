from mongoengine import NotUniqueError, ValidationError
from pymongo.errors import DuplicateKeyError

from app.models import Book, Comments, Genre, Author, User
from app.scrape import get_description, get_coverImage, get_genre, get_otherEditons, get_otherEditonsCovers, \
    get_seriesList, get_seriesListCovers, get_username, get_reviewDate, get_rating, get_review


def get_index():
    with open('files/index.txt', mode='r') as file:
        try:
            index = int(file.readline())
            return index
        except FileNotFoundError or ValueError:
            return 0
            pass


def get_collection_index():
    try:
        return Book.objects.order_by('-id').first()['id']
    except TypeError:
        return 1


def save_index():
    with open('files/index.txt', mode='w') as file:
        file.write(str(get_collection_index() + 1))


def create(bs, row, book_url):
    # Creating Book Object
    bookObj = create_book(
        bs, row, book_url
    )

    save_index()
    try:
        bookObj.save()
    except DuplicateKeyError and NotUniqueError:
        print("Book Exists")
        pass
    except ValidationError:
        print(bookObj.description)
        pass

    try:
        add_author(row)
        add_genre(get_genre(bs), row)
        add_comments(bs, row)
    except DuplicateKeyError and NotUniqueError as e:
        print(e)
        pass
    except ValidationError as e:
        print(e)
        pass


def create_book(bs, row, book_url):
    book = Book(
        bookID=row['bookID'],
        title=row['title'],
        authors=row['authors'],
        average_rating=row['average_rating'],
        isbn=row['isbn'],
        isbn13=row['isbn13'],
        language_code=row['language_code'],
        num_pages=row['num_pages'],
        ratings_count=row['ratings_count'],
        text_reviews_count=row['text_reviews_count'],
        publication_date=row['publication_date'],
        publisher=row['publisher'],
        url=book_url,
        description=get_description(bs),
        coverImage=get_coverImage(bs),
        genre=get_genre(bs),
        other_editions=get_otherEditons(bs),
        other_editions_covers=get_otherEditonsCovers(bs),
        series_list=get_seriesList(bs),
        series_list_cover=get_seriesListCovers(bs)
    )

    return book


def add_comments(bs, row):
    count = 0
    while True:
        username = get_username(bs, count)
        date = get_reviewDate(bs, count)
        rating = get_rating(bs, count)
        review = get_review(bs, count)

        comment = Comments(
            bookID=row['bookID'],
            date=date,
            rating=rating,
            username=username,
            review=review
        )
        comment.save()
        try:
            user = User(
                username=username,
                password=genrate_pass()
            )
            user.save()
        except DuplicateKeyError and NotUniqueError:
            pass

        count += 1
        if count >= 10:
            break


def add_genre(genre_list, row):
    for i in genre_list:
        genre_n = i
        try:
            genre = Genre(
                name=genre_n,
                books=[row['bookID']]
            )
            genre.save()
        except DuplicateKeyError and NotUniqueError:
            gen = Genre.objects(name=genre_n).first()
            gen.books.append(row['bookID'])
            gen.save()
            continue


def add_author(row):
    try:
        auth = Author(
            name=row['authors'],
            books=[row['bookID']]
        )
        auth.save()
    except DuplicateKeyError and NotUniqueError:
        au = Author.objects(name=row['authors']).first()
        au.books.append(row['bookID'])
        au.save()


def genrate_pass():
    import random

    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '.*$#@!&%'
    all = lower + upper + numbers + symbols
    lenghth = 8
    return "".join(random.sample(all, lenghth))
