from flask import jsonify

from .app import app, session
from .models import Book


@app.route('/book/')
def book():
    return jsonify(session.query(Book).all())
