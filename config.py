import os

from flask import app

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@localhost:5432/banned_books'
SQLALCHEMY_TRACK_MODIFICATIONS = False

