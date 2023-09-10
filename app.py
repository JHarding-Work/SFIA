from app import app
from create import populate_db

if __name__ == "__main__":
    populate_db()
    app.run(host="0.0.0.0", port=5000, debug=True)