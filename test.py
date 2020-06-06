import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Book


class BanedBooksTests(unittest.TestCase):
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

        self.editauthor = {
            "name": "updating Name"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

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

    def test_delete_book(self):
        # create a question to be deleted, stops it having to be changed all the time
        book = Book(title=self.addbook['title'], synopsis=self.addbook['synopsis'],
                    book_cover=self.addbook['book_cover'])
        book.insert()
        # store the new questions id
        book_delete = book.id
        response = self.client().delete('/book/delete/{}'.format(book_delete))
        data = json.loads(response.data)
        book = Book.query.filter(Book.id == book_delete).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], book_delete)

    def test_delete_book_is_none(self):
        response = self.client().delete('/book/delete/20000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_book_submit(self):
        response = self.client().post('/addbook', json=self.addbook)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_submit_writer_edit(self):
        response = self.client().patch('/authors/edit/1', json=self.editauthor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Author'])


if __name__ == '__main__':
    unittest.main()
