from mongoengine import Document, LongField, StringField, FloatField, IntField, DateTimeField, URLField, ListField, \
    SequenceField


class Book(Document):
    id = SequenceField(primary_key=True)
    bookID = LongField(required=True, unique=True)
    title = StringField(required=True)
    authors = StringField(required=True)
    average_rating = FloatField(required=True, max_value=5)
    isbn = StringField(required=True, unique=True, max_length=13)
    isbn13 = LongField(required=True, unique=True, max_length=13)
    language_code = StringField(required=True)
    num_pages = IntField(required=True)
    ratings_count = LongField(required=True)
    text_reviews_count = LongField(required=True)
    publication_date = DateTimeField(required=True)
    publisher = StringField(required=True)
    description = StringField(required=True)
    url = URLField(required=True)
    coverImage = URLField(required=True)
    genre = ListField(null=[])
    other_editions = ListField(null=[])
    other_editions_covers = ListField(URLField(), null=[])
    series_list = ListField(null=[])
    series_list_cover = ListField(URLField(), null=[])


class Comments(Document):
    id = SequenceField(primary_key=True)
    bookID = LongField(required=True)
    date = DateTimeField(required=True)
    rating = IntField(required=True)
    username = StringField(required=True)
    review = StringField(required=True)


class Genre(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True, unique=True)
    books = ListField(null=[])


class Author(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True, unique=True)
    books = ListField(null=[])


class User(Document):
    id = SequenceField(primary_key=True)
    username = StringField(required=True, unique=True, max_length=20)
    password = StringField(required=True, max_length=8)
