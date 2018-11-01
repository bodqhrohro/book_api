from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .app import app, session
from .models import Book
from .exceptions import InvalidUsage, Conflict
from .validation import books_schema, book_schema, ValidatedBookSchema


@app.route('/book/', methods=['GET'])
def get_books():
    result = books_schema.dump(session.query(Book).all())
    return jsonify(result.data)


@app.route('/book/', methods=['POST'])
def post_book():
    try:
        input = request.get_json()
    except:
        raise InvalidUsage('Can\'t read input JSON')

    try:
        input = ValidatedBookSchema().load(input)
        book = Book(**input.data)
    except ValidationError as err:
        raise InvalidUsage(','.join(err.messages))

    try:
        session.add(book)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise Conflict('Already exists')

    return book_schema.jsonify(book)
