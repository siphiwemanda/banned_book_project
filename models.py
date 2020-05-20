from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Books Table
'''


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    synopsis = db.Column(db.String)
    banned = db.relationship('Banned', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    book_cover = db.Column(db.String)

    def __init__(self, title, synopsis, countries_book_banned, author_id, book_cover):
        self.title = title
        self.synopsis = synopsis
        self.author = author_id
        self.country_id = countries_book_banned
        self.book_cover = book_cover

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'synopsis': self.synopsis,
            'author': self.author_id,
            'countries': self.countries_book_banned,
            'book_cover': self.book_cover
        }


'''
Authors Table
'''


class Authors(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    book = db.relationship('Books', lazy=True)

    def __init__(self, author_name):
        self.author_name = author_name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.author_name}


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    banned = db.relationship('Banned', lazy=True)

    def __init__(self, country):
        self.country = country

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'country': self.country}


class Banned(db.Model):
    __tablename__ = "banned_details"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
