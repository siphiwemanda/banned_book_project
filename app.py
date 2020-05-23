import os
from flask import Flask, jsonify, abort, request, render_template, redirect
from flask_cors import CORS
from models import setup_db, Book, Writer, Countries

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

        books = Book.query.all()

        # for book in books:

        return render_template('pages/home.html', books=books, isHomePage=True)

    @app.route('/authors')
    def get_authors():
        authors = Writer.query.all()

        return render_template('pages/author.html', authors=authors)

    @app.route('/countries')
    def get_countries():
        countries = Countries.query.all()

        return render_template('pages/countries.html', countries=countries)

    @app.route('/authors/<int:author_id>')
    def get_individual_authors(author_id):
        author = Writer.query.filter_by(id=author_id).first()
        author_name = author.name
        books = Book.query.filter_by(author_id=author_id).all()

        return render_template('pages/author_profile.html', author_name=author_name, books=books)

    @app.route('/book/<int:book_id>')
    def get_individual_book(book_id):
        book = Book.query.filter_by(id=book_id).first()
        book = book.title
        print(book)

        return render_template('pages/individual_book.html', book=book)

    @app.route('/book/delete/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            print('TRYING')
            delete_book = Book.query.filter(Book.id == book_id).one_or_none()

            if delete_book is None:
                print('IS NONE')
                abort(404)
            print(delete_book.id)
            delete_book.delete()

            return jsonify({
                'success': True,
                'deleted': delete_book.id,
            })
        except:
            print(422)
            abort(422)

    @app.route('/Addbook', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_book = body.get('title')
        new_blurb = body.get('blurb')
        try:

            book = Book(title=new_book, synopsis=new_blurb)
            book.insert()
        finally:

            return jsonify({
                'success': True,
                'created': book.title
            })

    @app.route('/authors/edit/<int:writer_id>')
    def edit_writer(writer_id):

        return render_template('forms/edit_authors.html')

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"

        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
