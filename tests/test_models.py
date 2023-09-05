from tests import TestBase
from app.models import *

from datetime import datetime as dt


class TestFilm(TestBase):
    def setUp(self) -> None:
        self.john = Actor(first_name="John", last_name="Actor")
        self.sarah = Actor(first_name="Sarah", last_name="Performer")

        self.oppenheimer = Film(title="Oppenheimer", actors=[self.john, self.sarah])
        self.lord_of_the_rings = Film(title="Lord of the Rings", actors=[self.sarah])

        self.showing1 = Showing(datetime=dt(2023, 9, 15, 11, 00), film=self.oppenheimer)
        self.showing2 = Showing(datetime=dt(2023, 9, 18, 14, 00), film=self.oppenheimer)

    def test_film_actors(self):
        self.assertEqual(self.oppenheimer.actors, [self.john, self.sarah])

    def test_actor_films(self):
        self.assertEqual(self.sarah.films, [self.oppenheimer, self.lord_of_the_rings])

    def test_film_showings(self):
        self.assertEqual(self.oppenheimer.showings, [self.showing1, self.showing2])
