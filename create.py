from app import app, bcrypt
from app.models import *

from datetime import date, time

john = Person(first_name="John", last_name="Actor")
sarah = Person(first_name="Sarah", last_name="Performer")
stephenson = Person(first_name="Stephen", last_name="Son")
louise = Person(first_name="Louise", last_name="Actor")
john_d = Person(first_name="John", last_name="Director")


oppenheimer = Film(title="Oppenheimer", director=john_d, actors=[stephenson, sarah], image_src="oppenheimer.jpg")
blue = Film(title="Blue Beetle", director=sarah, actors=[stephenson], image_src="blue.jpg")
lord_of_the_rings = Film(title="Lord of the Rings", director=john_d, actors=[john, sarah], image_src="lord-of-the-rings.jpg")
toy = Film(title="Toy Story", actors=[john, louise], image_src="toy_story.jpg")


for d in range(5, 14):
    for n in 11, 14:
        Showing(date=date(2023, 9, d), time=time(n, 0), film=oppenheimer)


for d in range(13, 24):
    for n in 9, 13, 17:
        Showing(date=date(2023, 9, d), time=time(n, 0), film=oppenheimer)

    for n in 11, 15:
        Showing(date=date(2023, 9, d), time=time(n, 0), film=blue)


Showing(date=date(2023, 9, 25), time=time(11, 0), film=lord_of_the_rings)
Showing(date=date(2023, 9, 25), time=time(15, 0), film=toy)


customer = Customer(username="John Buyer", password="Password")


def populate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all([oppenheimer, blue, lord_of_the_rings, toy, customer])
        db.session.commit()


if __name__ == "__main__":
    populate_db()