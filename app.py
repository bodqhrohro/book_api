from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_pyfile('config.py')

engine = create_engine(app.config['DB_CONNECTION_STRING'])
Session = sessionmaker(bind=engine)
session = Session()


from . import views


if __name__ == '__main__':
    app.run()
