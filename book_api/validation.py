import string
import re

from .exceptions import InvalidUsage
from .app import ma
from marshmallow import fields


class BookSchema(ma.Schema):
    class Meta:
            fields = ['id', 'isbn', 'title', 'annotation', 'authors']

book_schema = BookSchema()
books_schema = BookSchema(many=True)


class ValidatedBookSchema(BookSchema):
    isbn = fields.String(validate=lambda s: re.match(r'\d{13}', s))
    title = fields.String()
    annotation = fields.String()
    authors = fields.List(fields.String)
