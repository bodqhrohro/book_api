from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .app import app, session
from .models import Book
from .exceptions import InvalidUsage, Conflict, NotFound
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


@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = session.query(Book).get(id)
    if not book:
        raise NotFound('No such book')

    result = book_schema.dump(book)
    return jsonify(result.data)


@app.route('/book', methods=['GET'])
def get_books():
    try:
        input = request.get_json() or {}
    except:
        input = {}

    query = session.query(Book)

    if 'isbn' in input:
        query = query.filter(Book.isbn == input['isbn'])
    if 'title' in input:
        query = query.filter(Book.title.ilike('%%%s%%' % input['title']))
    if 'annotation' in input:
        query = query.filter(Book.annotation.ilike('%%%s%%' % input['annotation']))

    result = books_schema.dump(query.all())
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
    input = _get_input_book()

    try:
        book = session.query(Book).get(id)
        if not book:
            raise NotFound('No such book')

        book.isbn = input.isbn
        book.title = input.title
        book.annotation = input.annotation
        # 'authors': book.authors, # not touching for now

        session.commit()
    except IntegrityError:
        session.rollback()
        raise Conflict('Already exists')

    result = book_schema.dump(book)
    return jsonify(result.data)


@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = session.query(Book).get(id)
    if not book:
        raise NotFound('No such book')

    session.delete(book)
    session.commit()
    return app.response_class(response=None, status=204)
