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


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    synopsis = db.Column(db.String)
    banned = db.relationship('Banned_book', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    book_cover = db.Column(db.String)

    def __init__(self, title, synopsis, book_cover):
        self.title = title
        self.synopsis = synopsis
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
            'book_cover': self.book_cover
        }


'''
Authors Table
'''


class Writer(db.Model):
    __tablename__ = "writer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    dob = db.Column(db.Date)
    about = db.Column(db.String)
    book = db.relationship('Book', lazy=True)

    def __init__(self, name, dob, about):
        self.name = name
        self.dob = dob
        self.about = about

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
            'name': self.author_name,
            'dob': self.dob,
            'about': self.about
        }


class Countries(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    banned = db.relationship('Banned_book', lazy=True)

    def __init__(self, name):
        self.name = name

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
            'country': self.name}


class Banned_book(db.Model):
    __tablename__ = "banned_book"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    reason_given = db.Column(db.String)

    def __init__(self, start_date, end_date, reason_given):
        self.start_date = start_date
        self.end_date = end_date
        self.reason_given = reason_given

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
            'end_date': self.end_date,
            'reason_given': self.reason_given
        }
