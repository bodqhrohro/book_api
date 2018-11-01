import string
import re

from .exceptions import InvalidUsage


def validate_book(book, complete=False):
    for key in ['isbn', 'title', 'annotation', 'authors']:
        if not key in book.keys():
            if complete:
                raise InvalidUsage('"%s" key is missing' % key)
            else:
                book[key] = None

    if 'isbn' in book.keys():
        book['isbn'] = book['isbn'].replace('-', '')
        if not re.match(r'\d{13}', book['isbn']):
            raise InvalidUsage('ISBN should contain exactly 13 digits')

    if 'authors' in book.keys():
        if not isinstance(book['authors'], list):
            raise InvalidUsage('"authors" should be an array')
    return book