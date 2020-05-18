import os
from flask import Flask, jsonify, abort
from flask_cors import CORS

from models import setup_db, Books


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
        #return books

        return jsonify({
            'success': True,
            'books': books_dictionary
        })

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
