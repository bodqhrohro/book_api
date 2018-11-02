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

    input, errors = ValidatedBookSchema().load(input)
    for field in errors:
        for message in errors[field]:
            raise InvalidUsage('%s: %s' % (field, message))
    book = Book(**input)

    try:
        session.add(book)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise Conflict('Already exists')

    return book_schema.jsonify(book)
