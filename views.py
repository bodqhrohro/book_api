from .app import app
from flask import jsonify
# from .models import Book


@app.route('/book/')
def book():
    # return Book.query.all()
    return jsonify({'test': 'tist'})