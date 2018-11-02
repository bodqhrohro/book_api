from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .app import app, session
from .models import Book
from .exceptions import InvalidUsage, Conflict
from .validation import books_schema, book_schema, ValidatedBookSchema


def _get_input_book():
    try:
        input = request.get_json()
    except:
        raise InvalidUsage('Can\'t read input JSON')

    book, errors = ValidatedBookSchema().load(input)
    for field in errors:
        for message in errors[field]:
            raise InvalidUsage('%s: %s' % (field, message))

    return book


@app.route('/book', methods=['GET'])
def get_books():
    result = books_schema.dump(session.query(Book).all())
    return jsonify(result.data)


@app.route('/book', methods=['POST'])
def post_book():
    book = _get_input_book()

    try:
        session.add(book)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise Conflict('Already exists')

    result = book_schema.dump(book)
    return jsonify(result.data)


@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = _get_input_book()

    try:
        session.query(Book).filter_by(id=id).update({
            'isbn': book.isbn,
            'title': book.title,
            'annotation': book.annotation,
            # 'authors': book.authors, # not touching for now
        })
        session.commit()
    except IntegrityError:
        session.rollback()
        raise Conflict('Already exists')

    updated_book = session.query(Book).get(id)
    result = book_schema.dump(updated_book)
    return jsonify(result.data)
