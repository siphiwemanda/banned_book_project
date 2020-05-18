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
    db.create_all()


'''
Books Table
'''


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    blurb = db.Column(db.String)
    author = db.relationship('Authors', lazy=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    def __init__(self, title, blurb):
        self.title = title
        self.blurb = blurb

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
            'blurb': self.blurb}


'''
Authors Table
'''


class Authors(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

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


'''
countries Table
'''


class Countries(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String)
    book = db.relationship('Books', lazy=True)

    def __init__(self, country_name):
        self.country_name = country_name

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
            'country_name': self.country_name}


