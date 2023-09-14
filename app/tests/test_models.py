from app import app
from tests import TestBase
from models import *

from datetime import date, time


class TestFilm(TestBase):
    def setUp(self) -> None:
        self.john = Person(first_name="John", last_name="Actor")
        self.sarah = Person(first_name="Sarah", last_name="Performer")

        self.oppenheimer = Film(title="Oppenheimer", actors=[self.john, self.sarah])
        self.lord_of_the_rings = Film(title="Lord of the Rings", actors=[self.sarah])

        self.showing1 = Showing(date=date(2023, 9, 15), time=time(11, 00), film=self.oppenheimer)
        self.showing2 = Showing(date=date(2023, 9, 18), time=time(14, 00), film=self.oppenheimer)

    def test_film_actors(self):
        self.assertEqual(self.oppenheimer.actors, [self.john, self.sarah])

    def test_actor_films(self):
        self.assertEqual(self.sarah.starred_in, [self.oppenheimer, self.lord_of_the_rings])

    def test_film_showings(self):
        self.assertEqual(self.oppenheimer.showings, [self.showing1, self.showing2])

    def test_actor_list(self):
        self.assertEqual(self.oppenheimer.actor_list, ["John Actor", "Sarah Performer"])


class TestShowing(TestBase):
    def setUp(self) -> None:
        self.oppenheimer = Film(title="Oppenheimer")
        self.showing1 = Showing(date=date(2023, 9, 15), time=time(11, 00), film=self.oppenheimer)
        self.showing2 = Showing(date=date(2023, 9, 18), time=time(14, 15), film=self.oppenheimer)

    def test_formatted_time(self):
        self.assertEqual(self.showing1.formatted_time, "11:00")
        self.assertEqual(self.showing2.formatted_time, "14:15")


class TestPerson(TestBase):
    def setUp(self) -> None:
        self.sarah = Person(first_name="Sarah", last_name="Performer")

    def test_fullname(self):
        self.assertEqual("Sarah Performer", self.sarah.fullname)


class TestCustomer(TestBase):
    def setUpTestData(self):
        self.customer = Customer(username="John Buyer", password=bcrypt.generate_password_hash("Password"))

    def test_check_password_match(self):
        self.assertTrue(self.customer.check_password("Password"))

    def test_check_password_non_match(self):
        self.assertFalse(self.customer.check_password("password"))
