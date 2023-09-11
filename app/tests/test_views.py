from flask import url_for
from datetime import date, time
from flask_bcrypt import generate_password_hash

from models import *
from tests import TestBase


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
        sarah = Person(first_name="Sarah", last_name="Performer")
        stephenson = Person(first_name="Stephen", last_name="Son")
        john_d = Person(first_name="John", last_name="Director")
        oppenheimer = Film(title="Oppenheimer", director=john_d, actors=[stephenson, sarah], image_src="oppenheimer.jpg", release_date=date(2023,9,6))
        
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
        response = self.client.post(url_for('signup'), data=dict(username='Thiswillbetwentychar', password='password123!'))
        obj1 = Customer.query.filter_by(username='Thiswillbetwentychar').first()
        self.assertEqual(obj1.username, 'Thiswillbetwentychar')

        response = self.client.post(url_for('signup'), data=dict(username='Thiswillbetwentyfourchar', password='password123!'))
        obj1 = Customer.query.filter_by(username='Thiswillbetwentyfourchar').first()
        self.assertEqual(type(obj1), type(None))

        # number test
        response = self.client.post(url_for('signup'), data=dict(username='Athenanum', password='password!'))
        obj1 = Customer.query.filter_by(username='Athenanum').first()
        self.assertEqual(type(obj1), type(None))

        # special char test
        response = self.client.post(url_for('signup'), data=dict(username='Athenachar', password='password001'))
        obj1 = Customer.query.filter_by(username='Athenachar').first()
        self.assertEqual(type(obj1), type(None))

        # same username test
        response = self.client.post(url_for('signup'), data=dict(username='Athena', password='pass001!'))
        obj1 = Customer.query.filter_by(username='Athena').count()
        self.assertEqual(obj1, 1)

    def test_ticket_booking_post(self):
        
        customer=Customer(username='Billy1010',password=generate_password_hash('password123!'))
        customer2=Customer(username='Billy101010',password=generate_password_hash('password123!'))
        sarah = Person(first_name="Sarah", last_name="Performer")
        stephenson = Person(first_name="Stephen", last_name="Son")
        john_d = Person(first_name="John", last_name="Director")
        oppenheimer = Film(title="Oppenheimer", director=john_d, actors=[stephenson, sarah], image_src="oppenheimer.jpg", release_date=date(2023,9,6))
        
        for d in range(5, 14):
            for n in 11, 14:
                Showing(date=date(2023, 9, d), time=time(n, 0), film=oppenheimer, tickets=123)
        db.session.add_all([oppenheimer, customer])
        db.session.commit()

        #base test
        response = self.client.post(url_for('ticket_booking'), 
                                    data=dict(movie=1, 
                                            date=date(2023, 9, 13),
                                            time= time(11,0),
                                            username='Billy1010',
                                            password='password123!',
                                            no_of_adult=1,
                                            no_of_child=2,
                                            search=False,
                                            submit=True
                                            ))
        obj1 = Transaction.query.filter_by().count()
        self.assertEqual(obj1, 1)

        #incorrect username
        response = self.client.post(url_for('ticket_booking'), 
                                        data=dict(movie=1, 
                                            date=date(2023, 9, 13),
                                            time= time(11,0),
                                            username='Billy111111',
                                            password='password123!',
                                            no_of_adult=1,
                                            no_of_child=2,
                                            search=False,
                                            submit=True
                                            ))
        obj1 = Transaction.query.filter_by(customer_id=customer2.id).first()
        self.assertEqual(type(obj1), type(None))
        
        #incorrect password
        response = self.client.post(url_for('ticket_booking'), 
                                        data=dict(movie=1, 
                                            date=date(2023, 9, 13),
                                            time= time(11,0),
                                            username='Billy101010',
                                            password='password12!',
                                            no_of_adult=1,
                                            no_of_child=2,
                                            search=False,
                                            submit=True
                                            ))
        obj1 = Transaction.query.filter_by(customer_id=customer2.id).first()
        self.assertEqual(type(obj1), type(None))

        #booking too many tickets
        response = self.client.post(url_for('ticket_booking'), 
                                        data=dict(movie=1, 
                                            date=date(2023, 9, 13),
                                            time= time(11,0),
                                            username='Billy101010',
                                            password='password123!',
                                            no_of_adult=100,
                                            no_of_child=100,
                                            search=False,
                                            submit=True
                                            ))
        obj1 = Transaction.query.filter_by(customer_id=customer2.id).first()
        self.assertEqual(type(obj1), type(None))
