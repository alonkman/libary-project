import json
import requests
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app) 

db = SQLAlchemy(app)




# Books model
class Books(db.Model):
    id = db.Column('ID', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year_published = db.Column(db.String(100))
    book_type = db.Column(db.Integer)

    def __init__(self, name, author, year_published, book_type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year_published': self.year_published,
            'book_type': self.book_type
        }


# Function to display books
@app.route('/show-books', methods=['GET'])
def show_books():
    books_list = [book.to_dict() for book in Books.query.all()]
    return jsonify(books_list)


# Function to add a book
@app.route('/add-book', methods=['POST'])
def add_book():
    data = request.get_json()
    name = data.get('name')
    author = data.get('author')
    year_published = data.get('year_published')
    book_type = data.get('book_type')

    new_book = Books(name, author, year_published, book_type)
    db.session.add(new_book)
    db.session.commit()
    return "A new record was created."


# Function to delete a book
@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Books.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return 'Book deleted.'
    else:
        return 'Book not found.'