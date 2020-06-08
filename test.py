import json
import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Book
from dotenv import load_dotenv


class BanedBooksTests(unittest.TestCase):
    load_dotenv(verbose=True)
    DATAMANGER_ROLE = os.getenv('DATAMANGER_ROLE')
    EDITOR_ROLE = os.getenv('EDITOR_ROLE')

    Domain = os.getenv('Domain')

    AUTH0_DOMAIN = os.getenv('Domain')
    ALGORITHMS = os.getenv('ALGORITHMS')
    API_AUDIENCE = os.getenv('audience')

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:pass@localhost:5432/banned_books_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.addbook = {
            "title": "test book",
            "synopsis": "test book synopsis",
            "book_cover": "https://images.unsplash.com/photo-1567940800780-fc97bdfda133?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        }

        self.addbook_incorect = {
            "title": "",
            "synopsis": "",
            "book_cover": ""
        }

        self.editauthor = {
            "name": "updating Name"
        }

        self.editauthor_wrong = {
            "name": ""
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def create_auth_headers(self, token):
        # return auth headers using token
        return {
            "Authorization": "Bearer {}".format(
                token
            )}

    def test_landing_page(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_books(self):
        response = self.client().get('/book')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_books_400_error(self):
        response = self.client().get('/books')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_authors(self):
        response = self.client().get('/authors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_authors_404_error(self):
        response = self.client().get('/authorss')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_countries(self):
        response = self.client().get('/countries')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_countries_404_errors(self):
        response = self.client().get('/countriesss')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_individual_authors(self):
        response = self.client().get('/authors/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_individual_authors_out_of_range(self):
        response = self.client().get('/authors/7000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_individual_book(self):
        response = self.client().get('/book/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_individual_book_out_of_range(self):
        response = self.client().get('/book/7000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        print(data)

    def test_role_editor_fail(self):
        headers = self.create_auth_headers(token=self.EDITOR_ROLE)
        response = self.client().post('/book', json=self.addbook, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
