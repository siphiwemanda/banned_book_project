import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from models import setup_db, Books, Countries, Authors


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')

        return response

    @app.route('/')
    def get_books():
        books = Books.query.all()
        books_dictionary = {}
        for book in books:
            books_dictionary[book.id] = book.title

        ##if len(books_dictionary) == 0:
        ##  abort(404)

        return jsonify({
            'success': True,
            'books': books_dictionary
        })

    @app.route('/countries')
    def get_countries():
        countries = Countries.query.all()
        countries_dictionary = {}
        for country in countries:
            countries_dictionary[country.id] = country.country_name

        return jsonify({
            'success': True,
            'country': countries_dictionary
        })

    @app.route('/authors')
    def get_authors():
        authors = Authors.query.all()
        authors_dictionary = {}
        for author in authors:
            authors_dictionary[author.id] = author.author_name

        return jsonify({
            'success': True,
            'author': authors_dictionary
        })

    @app.route('/Addbook', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_book = body.get('title')
        new_blurb = body.get('blurb')

        try:

            book = Books(title=new_book, blurb=new_blurb)
            book.insert()
        finally:

            return jsonify({
                'success': True,
                'created': book.title
            })

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
