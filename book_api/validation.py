import string
import re

from .app import ma
from marshmallow import fields, ValidationError


class BookSchema(ma.Schema):
    class Meta:
            fields = ['id', 'isbn', 'title', 'annotation', 'authors']

book_schema = BookSchema()
books_schema = BookSchema(many=True)


def validate_isbn(isbn):
    if not re.match(r'\d{13}', isbn):
        raise ValidationError('ISBN should contain exactly 13 digits')


class ValidatedBookSchema(BookSchema):
    isbn = fields.String(validate=validate_isbn)
    title = fields.String()
    annotation = fields.String()
    authors = fields.List(fields.String)
