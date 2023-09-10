import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from time import sleep

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@mysql:3306/flask-db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from routes import *
from create import populate_db


if __name__ == "__main__":
    sleep(30)
    populate_db()
    app.run(host="0.0.0.0", port=5000, debug=True)