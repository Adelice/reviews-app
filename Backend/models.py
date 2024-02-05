from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from sqlalchemy.orm import relationship
from datetime import datetime
 
db = SQLAlchemy()
  
def get_uuid():
    return uuid4().hex
  
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    firstname = db.Column(db.String(150), nullable=False)  
    lastname = db.Column(db.String(150), nullable=False)   
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)  
    password = db.Column(db.Text, nullable=False) 
    birthday = db.Column(db.Date, nullable=False) 

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'


class Categories(db.Model):
    __tablename__ = 'all_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(50))

    movies = relationship('Movie', backref='categories', lazy='dynamic')
    books = relationship('Book', backref='categories', lazy='dynamic')
    hotels = relationship('Hotel', backref='categories', lazy='dynamic')
    reviews = relationship('Review', backref='categories', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
        }


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    published_date = db.Column(db.String(50))
    page_count = db.Column(db.Integer)
    thumbnail_url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey(
        'all_categories.id'))

    reviews = relationship('Review', back_populates='book', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'published_date': self.published_date,
            'page_count': self.page_count,
            'thumbnail_url': self.thumbnail_url,
            'category': 'book',
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
        }


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    review_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'review_id': self.review_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'is_read': self.is_read,
        }


class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    rating = db.Column(db.Float)
    photo_url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey(
        'all_categories.id'))

    reviews = relationship('Review', back_populates='hotel', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'hotel',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'rating': self.rating,
            'photo_url': self.photo_url,
            'category': 'hotel',
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    rating = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'all_categories.id'))

    book_id = db.Column(db.String(255), db.ForeignKey('books.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    hotel_id = db.Column(db.String(255), db.ForeignKey('hotels.id'))

    book = db.relationship('Book', back_populates='reviews')
    movie = db.relationship('Movie', back_populates='reviews')
    hotel = db.relationship('Hotel', back_populates='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'book_id': self.book_id,
            'movie_id': self.movie_id,
            'hotel_id': self.hotel_id,
            'category_id': self.category_id
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.String(4))
    description = db.Column(db.Text)
    poster_url = db.Column(db.String(255))

    category_id = db.Column(db.Integer, db.ForeignKey(
        'all_categories.id'))

    reviews = relationship('Review', back_populates='movie', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'movie',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'description': self.description,
            'poster_url': self.poster_url,
            'category': 'movie',
        }
