import os
from flask import Flask, jsonify, abort, request, render_template, redirect, session
from flask_cors import CORS
from models import setup_db, Book, Writer, Countries, db
import os.path
from auth import requires_auth, AuthError
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

BOOKS_PER_PAGE = 8

database_path = os.environ['DATABASE_URL']
Domain = os.environ['Domain']
Audience = os.environ['audience']
Client_id = os.environ['client_id']
returning = os.environ['redirect']


def create_auth0():
    AUTH0_AUTHORIZE_URL = 'https://' + Domain + '/authorize?audience=' + Audience + '&response_type=token&client_id=' + Client_id + '&redirect_uri=' + returning
    # print(AUTH0_AUTHORIZE_URL)
    return AUTH0_AUTHORIZE_URL


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
    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id='nnjGWA0Hjqopk5wfAZO9P1dduaOTDQTu',
        client_secret='YOUR_CLIENT_SECRET',
        api_base_url='https://banned-book-project.eu.auth0.com',
        access_token_url='https://banned-book-project.eu.auth0.com/oauth/token',
        authorize_url='https://banned-book-project.eu.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,PATCH,OPTIONS')

        return response

    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')

    @app.route('/')
    def get_books():

        books = Book.query.all()
        # query = db.session.query(Writer, Book).outerjoin(Writer, Book.id == Writer.book).all()
        # for book in books:
        AUTH0_AUTHORIZE_URL = create_auth0()

        return render_template('pages/home.html', books=books, isHomePage=True, AUTH0_AUTHORIZE_URL=AUTH0_AUTHORIZE_URL)

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
    @requires_auth('del:book')
    def delete_book(*args, **kwargs):
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

    @app.route('/addbook')
    def add_book_():

        return render_template('forms/add_book.html')

    @app.route('/addbook/submit', methods=['POST'])
    @requires_auth('post:book')
    def add_book_submit(*args, **kwargs):
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

    @app.route('/authors/edit/<int:writer_id>')
    def edit_writer(writer_id):
        authors = Writer.query.all()
        author = Writer.query.filter_by(id=writer_id).first()

        return render_template('forms/edit_authors.html', author=author)

    @app.route('/authors/edit/submit/<int:writer_id>', methods=['PATCH'])
    @requires_auth('patch:editauthor')
    def submit_writer_edit(*args, **kwargs):
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
