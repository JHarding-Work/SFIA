import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)