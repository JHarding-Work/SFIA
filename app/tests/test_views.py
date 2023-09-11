from datetime import date, time

from flask import url_for

from app import db, bcrypt
from models import Customer, Film, Showing
from tests import TestBase

from unittest.mock import patch, Mock


class TestGet(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_get(self):
        response = self.client.get(url_for('signup'))
        self.assertEqual(response.status_code, 200)

    def test_opening_times_get(self):
        response = self.client.get(url_for('opening_times'))
        self.assertEqual(response.status_code, 200)

    def test_listings_get(self):
        response = self.client.get(url_for('listings'))
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


class TestPost(TestBase):
    def test_sign_up_post(self):
        # min length test
        response = self.client.post(url_for('signup'), data=dict(username='Athena', password='pass123!'))
        obj1 = Customer.query.filter_by(username='Athena').first()
        self.assertEqual(obj1.username, 'Athena')

        response = self.client.post(url_for('signup'), data=dict(username='Athen', password='pass123!'))
        obj1 = Customer.query.filter_by(username='Athen').first()
        self.assertEqual(type(obj1), type(None))

        response = self.client.post(url_for('signup'), data=dict(username='Athena01', password='p3!'))
        obj1 = Customer.query.filter_by(username='Athena01').first()
        self.assertEqual(type(obj1), type(None))

        # max length test
        response = self.client.post(url_for('signup'),
                                    data=dict(username='Thiswillbetwentychar', password='password123!'))
        obj1 = Customer.query.filter_by(username='Thiswillbetwentychar').first()
        self.assertEqual(obj1.username, 'Thiswillbetwentychar')

        response = self.client.post(url_for('signup'),
                                    data=dict(username='Thiswillbetwentyfourchar', password='password123!'))
        obj1 = Customer.query.filter_by(username='Thiswillbetwentyfourchar').first()
        self.assertEqual(type(obj1), type(None))

        # number test
        response = self.client.post(url_for('signup'), data=dict(username='Athenanum', password='pass!'))
        obj1 = Customer.query.filter_by(username='Athenanum').first()
        self.assertEqual(type(obj1), type(None))

        # special char test
        response = self.client.post(url_for('signup'), data=dict(username='Athenachar', password='pass001'))
        obj1 = Customer.query.filter_by(username='Athenachar').first()
        self.assertEqual(type(obj1), type(None))

        # same username test
        response = self.client.post(url_for('signup'), data=dict(username='Athena', password='pass001!'))
        obj1 = Customer.query.filter_by(username='Athena').count()
        self.assertEqual(obj1, 1)


class TestHome(TestBase):
    def run_assertions(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'navbar', response.data)
        self.assertIn(b'<h1 class="font-impact">QA Cinemas</h1>', response.data)

    def test_get_base(self):
        self.run_assertions(self.client.get('/'))

    def test_get_home(self):
        self.run_assertions(self.client.get('/home'))


class TestListings(TestBase):
    def setUpTestData(self) -> None:
        self.oppenheimer = Film(title="Oppenheimer")
        self.showing1 = Showing(date=date(2023, 9, 15), time=time(11, 00), film=self.oppenheimer)
        self.showing2 = Showing(date=date(2023, 9, 18), time=time(14, 15), film=self.oppenheimer)

        db.session.add(self.oppenheimer)
        db.session.commit()

    def test_post(self):
        response = self.client.post('/listings', data=dict(date='2023-9-15'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Oppenheimer', response.data)
        self.assertIn(b'11:00', response.data)
        self.assertNotIn(b'14:15', response.data)

    @patch('routes.datetime')
    def test_get(self, datetime: Mock):
        datetime.now.return_value = Mock(date=lambda: date(2023, 9, 18))
        response = self.client.get('/listings')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Oppenheimer', response.data)
        self.assertNotIn(b'11:00', response.data)
        self.assertIn(b'14:15', response.data)


class TestFilm(TestBase):
    def setUpTestData(self) -> None:
        self.oppenheimer = Film(title="Oppenheimer", image_src="TestImage")

        db.session.add(self.oppenheimer)
        db.session.commit()

    def test_get(self):
        response = self.client.get('/film/1')

        self.assertEqual(response.status_code, 200)
        self.assertIn('src="/static/TestImage"', str(response.data))


class TestLogin(TestBase):
    def setUpTestData(self):
        self.customer = Customer(username="John Buyer", password=bcrypt.generate_password_hash("Password"))
        db.session.add(self.customer)
        db.session.commit()

    def test_login(self):
        response = self.client.post('/login', data=dict(username="John Buyer", password="Password"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged In', response.data)

    def test_bad_username(self):
        response = self.client.post('/login', data=dict(username="John B", password="Password"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Failed to Log In', response.data)

    def test_bad_password(self):
        response = self.client.post('/login', data=dict(username="John Buyer", password="password"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Failed to Log In', response.data)
