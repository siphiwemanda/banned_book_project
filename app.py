##Imports
import os
from flask import Flask, jsonify, abort, request, render_template, redirect, session
from flask_cors import CORS
from models import setup_db, Book, Writer, Countries, db, Banned_book
import os.path
from auth import requires_auth, AuthError
from dotenv import load_dotenv

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    load_dotenv(verbose=True)
    Domain = os.getenv('Domain')
    print('Domain is ' + Domain)


    database_path = os.getenv('DATABASE_URL')
    #Domain = os.getenv('Domain')
    #print('Domain is ' + Domain)
    Audience = os.getenv('audience')
    Client_id = os.getenv('client_id')
    returning = os.getenv('redirect')
    print(returning)
    DATAMANGER_ROLE = os.getenv('DATAMANGER_ROLE')

    ##Create login link
    def create_auth0():
        AUTH0_AUTHORIZE_URL = 'https://' + Domain + '/authorize?audience=' + Audience + '&response_type=token&client_id=' + Client_id + '&redirect_uri=' + returning
        print(AUTH0_AUTHORIZE_URL)
        print(returning)
        return AUTH0_AUTHORIZE_URL

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,PATCH,OPTIONS')

        return response

    @app.route('/')
    def landing_page():
        AUTH0_AUTHORIZE_URL = create_auth0()
        return render_template('layouts/main.html', AUTH0_AUTHORIZE_URL=AUTH0_AUTHORIZE_URL)


    @app.route('/book')
    def get_books():
        # returns all the books in the database
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
        # returns all the writers in the database
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
        # returns all the countries in the database
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
        try:
            # gets the individual author and all books in the database associated with them
            author = Writer.query.filter_by(id=author_id).first()
            writer_name = author.name
            books = Book.query.filter_by(author_id=author_id).all()
            books_dictionary = {}
            for book in books:
                books_dictionary[book.id] = book.title

            return jsonify({
                'success': True,
                'author': writer_name,
                'Books': books_dictionary
            })
        except:
            abort(422)

    @app.route('/book/<int:book_id>')
    def get_individual_book(book_id):
        try:
            # returns book and author and the counties they are banned in
            book = Book.query.filter_by(id=book_id).first()
            print(book)
            book_title = book.title

            bookwriter = book.author_id
            print(bookwriter)

            writer = Writer.query.filter_by(id=bookwriter).first()
            writer_name = writer.name
            print(writer)
            print(writer_name)
            print(book_title)

            banned_details = Banned_book.query.filter(Banned_book.book_id == book_id).all()
            print(banned_details)
            details_list = []
            for details in banned_details:
                start_date = details.start_date
                end_date = details.end_date
                reason_given = details.reason_given
                sublist = [start_date, end_date, reason_given]

                countries = details.country_id
                print(countries)
                country_name = Countries.query.filter_by(id=countries).all()
                print(country_name)
                # name =country_name.name
                for name in country_name:
                    name = name.name
                    print(name)
                    sublist.insert(0, name)
                details_list.append(sublist)
            print(details_list)
            return jsonify({
                'success': True,
                'Book title': book_title,
                'author': writer_name,
                'banned details': details_list
            })
        except:
            abort(422)

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

    @app.route('/addbook', methods=['POST'])
    @requires_auth('post:book')
    def add_book_submit(*args, **kwargs):
        # adds a book
        body = request.get_json()
        new_book = body.get('title')
        print('book is ' + new_book)
        new_synopsis = body.get('synopsis')
        print(new_synopsis)
        new_book_cover = body.get('book_cover')
        print(new_book_cover)

        if new_book=='' and new_synopsis=='':
            abort(422)
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
        # edits an author
        writer_id = kwargs['writer_id']
        update = Writer.query.filter_by(id=writer_id).first()
        print(update.name, update.about, update.dob)
        body = request.get_json()
        #print('body is ' + body)

        if body.get('name') == '' or body.get('dob') == '' or body.get('about') == '':
            print('failing')
            abort(422)

        if body.get('name'):
            update.name = body.get('name')
            print('name ' + update.name)
        if body.get('dob'):
            update.dob = body.get('dob')
            print('dob ' + update.dob)
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


    ##Error handlers
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
