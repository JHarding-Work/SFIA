from app import app, bcrypt
from app.models import *

from flask import redirect, url_for, render_template, request

if __name__ == "__main__":
    app.run(debug=True)