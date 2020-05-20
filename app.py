import os
from flask import Flask, jsonify, abort, request, render_template
from flask_cors import CORS
from models import setup_db, Books, Authors

BOOKS_PER_PAGE = 8


def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_PAGE
    end = start + BOOKS_PER_PAGE

    books = [book.format() for book in selection]
    current_book = books[start:end]

    return current_book


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

        return render_template('pages/home.html', books=books)

    @app.route('/authors')
    def get_authors():
        authors = Authors.query.all()

        return render_template('pages/authors.html', authors=authors)

    @app.route('/authors/<int:author_id>')
    def get_individual_authors(author_id):
        author = Authors.query.filter_by(id=author_id).first()
        author_name = author.author_name
        books = Books.query.filter_by(author_id=author_id).all()

        return render_template('pages/author_profile.html', author_name=author_name, books=books)

    @app.route('/book/<int:book_id>')
    def get_individual_book(book_id):
        book = Authors.query.filter_by(id=book_id).first()
        book = book.id

        return render_template('pages/individual_book.html', book=book)

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
