from app import app
from tests import TestBase
from models import *

from datetime import date, time


class TestFilm(TestBase):
    def create_app(self):
        # Pass in testing configurations for the app.
        # Here we use sqlite without a persistent database for our tests.
        app.config.update(
              SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
              SECRET_KEY='TEST_SECRET_KEY',
              DEBUG=True,
              WTF_CSRF_ENABLED=False
        )
        return app

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



class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)  
    
    def test_login_get(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)  
        
    def test_signup_get(self):
        response = self.client.get(url_for('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)  
          
    def test_opening_times_get(self):
        response = self.client.get(url_for('opening_times'))
        self.assertEqual(response.status_code, 200)  

    def test_listings_get(self):
        response = self.client.get(url_for('listings'))
        self.assertEqual(response.status_code, 200)  

    def test_login_get(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)  
    
    def test_about_us_get(self):
        response = self.client.get(url_for('about_us'))
        self.assertEqual(response.status_code, 200) 

    def test_contacts_get(self):
        response = self.client.get(url_for('contacts'))
        self.assertEqual(response.status_code, 200) 

    def test_new_releases_get(self):
        response = self.client.get(url_for('new_releases'))
        self.assertEqual(response.status_code, 200)  

    def test_ticket_booking_get(self):
        response = self.client.get(url_for('ticket_booking'))
        self.assertEqual(response.status_code, 200)  
    
    def test_single_film_get(self):
        films = Film.query.all()
        for film in films:
            response = self.client.get(f'/film/{film.id}')
            self.assertEqual(response.status_code, 200)


class TestCrud(TestBase):

    def test_sign_up_post(self):
        #min length test
        response = self.client.post(url_for('signup'), data = dict(username='Athena',password='pass123!'))
        obj1 = Customer.query.filter_by(username='Athena').first()
        self.assertEqual(obj1.username, 'Athena')

        response = self.client.post(url_for('signup'), data = dict(username='Athen',password='pass123!'))
        obj1 = Customer.query.filter_by(username='Athen').first()
        self.assertEqual(type(obj1), type(None))

        response = self.client.post(url_for('signup'), data = dict(username='Athena01',password='p3!'))
        obj1 = Customer.query.filter_by(username='Athena01').first()
        self.assertEqual(type(obj1), type(None))

        #max length test
        response = self.client.post(url_for('signup'), data = dict(username='Thiswillbetwentychar',password='password123!'))
        obj1 = Customer.query.filter_by(username='Thiswillbetwentychar').first()
        self.assertEqual(obj1.username, 'Thiswillbetwentychar')

        response = self.client.post(url_for('signup'), data = dict(username='Thiswillbetwentyfourchar',password='password123!'))
        obj1 = Customer.query.filter_by(username='Thiswillbetwentyfourchar').first()
        self.assertEqual(type(obj1), type(None))

        #number test
        response = self.client.post(url_for('signup'), data = dict(username='Athenanum',password='pass!'))
        obj1 = Customer.query.filter_by(username='Athenanum').first()
        self.assertEqual(type(obj1), type(None))

        #special char test
        response = self.client.post(url_for('signup'), data = dict(username='Athenachar',password='pass001'))
        obj1 = Customer.query.filter_by(username='Athenachar').first()
        self.assertEqual(type(obj1), type(None))

        #same username test
        response = self.client.post(url_for('signup'), data = dict(username='Athena',password='pass001!'))
        obj1 = Customer.query.filter_by(username='Athena').count()
        self.assertEqual(obj1, 1)



          

          
                  