import os
from flask import Flask, jsonify, abort, request, render_template, redirect, session
from flask_cors import CORS
from models import setup_db, Book, Writer, Countries, db
import os.path
from auth import requires_auth, AuthError

database_path = os.environ['DATABASE_URL']
Domain = os.environ['Domain']
Audience = os.environ['audience']
Client_id = os.environ['client_id']
returning = os.environ['redirect']


def create_auth0():
    AUTH0_AUTHORIZE_URL = 'https://' + Domain + '/authorize?audience=' + Audience + '&response_type=token&client_id=' + Client_id + '&redirect_uri=' + returning
    print(AUTH0_AUTHORIZE_URL)
    return AUTH0_AUTHORIZE_URL


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,PATCH,OPTIONS')

        return response

    @app.route('/')
    def landing_page():

        return "welcome to the banned books API  Landing page "

    @app.route('/books')
    def get_books():
        # retunrs all the books the countries they are banned
        books = Book.query.all()
        # AUTH0_AUTHORIZE_URL = create_auth0()
        books_dictionary = {}
        for books in books:
            books_dictionary[books.id] = books.title

        return jsonify({
            'success': True,
            'books': books_dictionary
        })

    @app.route('/authors')
    def get_authors():
        # returns all the writers and there books on this list
        authors = Writer.query.all()
        authors_dictionary = {}
        for author in authors:
            authors_dictionary[author.id] = author.name

        return jsonify({
            'success': True,
            'authors': authors_dictionary
        })

    @app.route('/countries')
    def get_countries():
        # retunrs all the countries and the books banned their
        countries = Countries.query.all()
        countries_dictionary = {}
        for country in countries:
            countries_dictionary[country.id] = country.name

        return jsonify({
            'success': True,
            'countries': countries_dictionary
        })

    @app.route('/authors/<int:author_id>')
    def get_individual_authors(author_id):
        # gets the individual author and all books associanted with them
        author = Writer.query.filter_by(id=author_id).first()
        author_name = author.name
        books = Book.query.filter_by(author_id=author_id).all()

        return jsonify({
            'success': True,
            'questions': author
        })

    @app.route('/book/<int:book_id>')
    def get_individual_book(book_id):
        # returrns book and author and countries it is banned in
        book = Book.query.filter_by(id=book_id).first()
        book = book.id
        print(book)

        return jsonify({
            'success': True,
            'questions': book
        })

    @app.route('/book/delete/<int:book_id>', methods=['DELETE'])
    @requires_auth('del:book')
    def delete_book(*args, **kwargs):
        # deletes a book
        id = kwargs['book_id']
        try:
            print('TRYING')
            delete_book = Book.query.filter(Book.id == id).one_or_none()

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

    @app.route('/addbook/', methods=['POST'])
    @requires_auth('post:book')
    def add_book_submit(*args, **kwargs):
        # adds a book
        body = request.get_json()
        new_book = body.get('title')
        print(new_book)
        new_synopsis = body.get('synopsis')
        print(new_synopsis)
        new_book_cover = body.get('book_cover')
        print(new_book_cover)
        try:

            book = Book(title=new_book, synopsis=new_synopsis, book_cover=new_book_cover)
            book.insert()
        finally:

            return jsonify({
                'success': True,
                'created': book.title
            })

    @app.route('/authors/edit/<int:writer_id>', methods=['PATCH'])
    @requires_auth('patch:editauthor')
    def submit_writer_edit(*args, **kwargs):
        # edddies an author
        writer_id = kwargs['writer_id']
        update = Writer.query.filter_by(id=writer_id).first()
        print(update.name, update.about, update.dob)
        body = request.get_json()
        print(body)

        if body.get('name'):
            update.name = body.get('name')
            print(update.name)
        if body.get('dob'):
            update.dob = body.get('dob')
            print(update.dob)
        if body.get('about'):
            update.about = body.get('about')
            print(update.about)

        try:
            update.insert()
        except:
            print('patch aborted')
            abort(422)
        return ({
            "success": True,
            "Author": update.name
        })

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

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
