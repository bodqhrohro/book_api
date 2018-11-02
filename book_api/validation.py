import string
import re

from marshmallow import fields, ValidationError
from marshmallow_sqlalchemy import ModelSchema

from .app import session
from .models import Book


class BookSchema(ModelSchema):
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'annotation', 'authors']
        sqla_session = session

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
