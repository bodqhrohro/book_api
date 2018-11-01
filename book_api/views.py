from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from .app import app, session
from .models import Book
from .exceptions import InvalidUsage, Conflict
from .validation import validate_book


@app.route('/book/', methods=['GET'])
def get_books():
    return jsonify([book.to_json() for book in session.query(Book).all()])


@app.route('/book/', methods=['POST'])
def post_book():
    try:
        input = request.get_json()
    except:
        raise InvalidUsage('Can\'t read input JSON')

    input = validate_book(input)
    book = Book(
        isbn=input['isbn'],
        title=input['title'],
        annotation=input['annotation'],
        authors=input['authors'],
    )
    try:
        session.add(book)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise Conflict('Already exists')

    return jsonify(book.to_json())
