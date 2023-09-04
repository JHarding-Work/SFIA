from app import app, bcrypt
from models import *


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == "__main__":
    populate_db()
