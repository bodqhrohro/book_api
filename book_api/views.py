from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .app import app, session
from .models import Book, Author
from .exceptions import InvalidUsage, Conflict, NotFound
from .validation import authors_schema, author_schema, ValidatedAuthorSchema, \
    books_schema, book_schema, ValidatedBookSchema


def _read_json():
    try:
        return request.get_json()
    except:
        raise InvalidUsage('Can\'t read input JSON')


def _process_errors(errors):
    for field in errors:
        for error_type in errors[field]:
            for message in errors[field][error_type]:
                raise InvalidUsage('%s: %s: %s' % (field, error_type, message))


def _get_input_book():
    input = _read_json()

    if 'authors' in input:
        authors_dicts = []
        for id in input['authors']:
            author = session.query(Author).get(id)

            if author:
                authors_dicts.append({
                    'id': id,
                    'first_name': author.first_name,
                    'last_name': author.last_name,
                })
            else:
                raise InvalidUsage('Invalid author ID passed')
        input['authors'] = authors_dicts

    book, errors = ValidatedBookSchema().load(input)
    _process_errors(errors)

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

    # try:
    book = session.query(Book).get(id)
    if not book:
        raise NotFound('No such book')

    book.isbn = input.isbn
    book.title = input.title
    book.annotation = input.annotation
    # 'authors': book.authors, # not touching for now

    renewed_authors = []
    # add non-existing authors
    for id in input.authors:
        author = session.query(Author).get(id)

        if not author:
            raise InvalidUsage('Invalid author ID passed')
        else:
            same_authors = list(filter(
                lambda a: a.id == author.id,
                book.authors))

            if len(same_authors) == 0:
                book.authors.append(author)

    renewed_authors.append(author)
    # delete previously set but now absent authors
    for author in book.authors:
        if author not in renewed_authors:
            book.authors.delete(author)

    session.commit()
    # except IntegrityError:
    #     session.rollback()
    #     raise Conflict('Already exists')

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


def _get_input_author():
    input = _read_json()

    author, errors = ValidatedAuthorSchema().load(input)
    _process_errors(errors)

    return author


@app.route('/author/<id>', methods=['GET'])
def get_author(id):
    author = session.query(Author).get(id)
    if not author:
        raise NotFound('No such author')

    result = author_schema.dump(author)
    return jsonify(result.data)


@app.route('/author', methods=['GET'])
def get_authors():
    query = session.query(Author)

    result = authors_schema.dump(query.all())
    return jsonify(result.data)


@app.route('/author', methods=['POST'])
def post_author():
    author = _get_input_author()

    session.add(author)
    session.commit()

    result = author_schema.dump(author)
    return jsonify(result.data)


@app.route('/author/<id>', methods=['PUT'])
def update_author(id):
    input = _get_input_author()

    author = session.query(Author).get(id)
    if not author:
        raise NotFound('No such author')

    author.first_name = input.first_name
    author.last_name = input.last_name

    session.commit()

    result = author_schema.dump(author)
    return jsonify(result.data)


@app.route('/author/<id>', methods=['DELETE'])
def delete_author(id):
    author = session.query(Author).get(id)
    if not author:
        raise NotFound('No such author')

    session.delete(author)
    session.commit()
    return app.response_class(response=None, status=204)
