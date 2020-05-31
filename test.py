import json
import unittest
from flask import  Flask

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, database_path


class BanedBooksTests(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.add_question = {
            "question": "Does the question get added to the database",
            "answer": "Yes",
            "category": 1,
            "difficulty": 5
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_books(self):
        response = self.client().get('/books')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == '__main__':
    unittest.main()
