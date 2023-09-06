from app import app, bcrypt
from app.models import *

from datetime import datetime as dt

john = Person(first_name="John", last_name="Actor")
sarah = Person(first_name="Sarah", last_name="Performer")
stephenson = Person(first_name="Stephen", last_name="Son")
louise = Person(first_name="Louise", last_name="Actor")


oppenheimer = Film(title="Oppenheimer", actors=[stephenson, sarah], image_src="oppenheimer.jpg")
blue = Film(title="Blue Beetle", actors=[stephenson], image_src="blue.jpg")
lord_of_the_rings = Film(title="Lord of the Rings", actors=[john, sarah], image_src="lord-of-the-rings.jpg")
toy = Film(title="Toy Story", actors=[john, louise], image_src="toy_story.jpg")


for d in range(13, 14):
    for n in 9, 13, 17:
        Showing(datetime=dt(2023, 9, d, n, 00), film=oppenheimer)

    for n in 11, 15:
        Showing(datetime=dt(2023, 9, d, n, 00), film=blue)


Showing(datetime=dt(2023, 9, 25, 11, 00), film=lord_of_the_rings)
Showing(datetime=dt(2023, 9, 25, 15, 00), film=toy)


customer = Customer(username="John Buyer", password="Password")


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all([oppenheimer, blue, lord_of_the_rings, toy, customer])
        db.session.commit()


if __name__ == "__main__":
    populate_db()
