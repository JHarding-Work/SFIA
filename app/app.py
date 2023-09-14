import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

mysql_root_password = os.getenv('MYSQL_ROOT_PASSWORD')
mysql_database_uri = f'mysql+pymysql://root:{mysql_root_password}@mysql:3306/flask-db'

supplied_uri = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///db.sqlite")

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_database_uri if mysql_root_password else supplied_uri
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)