from flask_sqlalchemy import SQLAlchemy
from flask_api import FlaskAPI

app = FlaskAPI(__name__)
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return {'Hello': 'World!'}


if __name__ == '__main__':
    app.run()
