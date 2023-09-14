from datetime import date, time

from flask import url_for, session
from datetime import date, time
from flask_bcrypt import generate_password_hash

from models import *
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
        
        john = Person(first_name="John", last_name="Actor")
        sarah = Person(first_name="Sarah", last_name="Performer")
        stephenson = Person(first_name="Stephen", last_name="Son")
        louise = Person(first_name="Louise", last_name="Actor")
        john_d = Person(first_name="John", last_name="Director")

        oppenheimer = Film(title="Oppenheimer", director=john_d, actors=[stephenson, sarah], image_src="oppenheimer.jpg", release_date=date(2023,9,6))
        blue = Film(title="Blue Beetle", director=sarah, actors=[stephenson], image_src="blue.jpg", release_date=date(2023,9,15))
        lord_of_the_rings = Film(title="Lord of the Rings", director=john_d, actors=[john, sarah], image_src="lord-of-the-rings.jpg", release_date=date(2024,9,6))
        toy = Film(title="Toy Story", actors=[john, louise], image_src="toy-story.png", release_date=date(2021,9,6))


        films = Film.query.all()
        for film in films:
            response = self.client.get(f'/film/{film.id}')
            self.assertEqual(response.status_code, 200)
    
    def payments_get(self):
        customer = Customer(username='Billy1010',password=generate_password_hash('password123!'))
        transaction = Transaction(customer_id = customer.id)

        response = self.client.get('/payments')
        self.assertEqual(response.status_code, 200)
    
    def pay_success_get(self):
        response = self.client.get(url_for('pay_success'))
        self.assertEqual(response.status_code, 200)
    


class TestPost(TestBase):
    def test_sign_up_post(self):
        # base test
        response = self.client.post(url_for('signup'), data=dict(username='Athena', password='pass123!'))
        obj1 = Customer.query.filter_by(username='Athena').first()
        self.assertEqual(obj1.username, 'Athena')
        
        # min length tests
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
        customer = Customer(username='Billy1010', password=generate_password_hash('password123!'))
        customer2 = Customer(username='Billy101010', password=generate_password_hash('password123!'))
        sarah = Person(first_name="Sarah", last_name="Performer")
        stephenson = Person(first_name="Stephen", last_name="Son")
        john_d = Person(first_name="John", last_name="Director")
        oppenheimer = Film(title="Oppenheimer", director=john_d, actors=[stephenson, sarah], image_src="oppenheimer.jpg", release_date=date(2023,9,6))

        for d in range(5, 14):
            for n in 11, 14:
                Showing(date=date(2023, 9, d), time=time(n, 0), film=oppenheimer, tickets=123)
        db.session.add_all([oppenheimer, customer])
        db.session.commit()

        with self.client.session_transaction(subdomain="sess") as session:
            session['loggedin'] = True
            session['id'] = customer.id
            session['username'] = customer.username

        #base test
        response = self.client.post(url_for('ticket_booking'),
                                    data=dict(movie=1,
                                            date=date(2023, 9, 13),
                                            time= time(11,0),
                                            no_of_adult=1,
                                            no_of_child=2,
                                            search=False,
                                            submit=True
                                            ),subdomain="sess")
        obj1 = Transaction.query.filter_by().count()
        self.assertEqual(obj1, 1)

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
                                            ),subdomain="sess")
        obj1 = Transaction.query.filter_by(customer_id=customer2.id).first()
        self.assertEqual(type(obj1), type(None))
    
    def test_payment_post(self):
        customer = Customer(id=1,username='Billy1010',password=generate_password_hash('password123!'))
        transaction = Transaction(customer_id = customer.id)
        db.session.add(customer)
        db.session.add(transaction)
        db.session.commit()

        data=dict(
        address_line='flat 124 wefijwe',
        city='qwefqwefqwef',
        postcode='AB12 3CD',
        card_name='asdfasdv',
        card_no='1234567890123451',
        card_exp='11/2024',
        cvv='123')

        with self.client.session_transaction(subdomain="sess") as session:
            session['loggedin'] = True
            session['id'] = customer.id
            session['username'] = customer.username
            session['trans'] = transaction.id
        #base test
        temp = data.copy()
        response = self.client.post('/payments',data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(address_line='flat 124 wefijwe').first()
        self.assertEqual(obj1.cvv,'123')

        #length tests
        temp = data.copy()
        temp['address_line'] = 'I Need to make this exactly 31c'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(address_line='I Need to make this exactly 31c').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['city'] = 'I Need to make this exactly 31c'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(city='I Need to make this exactly 31c').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['postcode'] = '9 charact'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(postcode='9 charact').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['card_name'] = 'This is exactly 20 ch'
        response = self.client.post('/payments', data=temp, subdomain="sess" )
        obj1 = Customer.query.filter_by(card_name='This is exactly 20 c').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['card_no'] = '012345678912345'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_no='012345678912345').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['card_no'] = '01234567891234567'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_no='01234567891234567').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['cvv'] = '01'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(cvv='01').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['cvv'] = '0123'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(cvv='0123').first()
        self.assertEqual(type(obj1), type(None))

        #Postcode Validation Tests
        temp = data.copy()
        temp['postcode'] = 'AB1 2CD'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by().first()
        self.assertEqual(obj1.postcode, 'AB1 2CD')

        temp = data.copy()
        temp['postcode'] = 'BN12 3CD'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by().first()
        self.assertEqual(obj1.postcode, 'BN12 3CD')

        temp = data.copy()
        temp['postcode'] = 'AB123CD'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by().first()
        self.assertEqual(obj1.postcode, 'AB123CD')
        
        temp = data.copy()
        temp['postcode'] = 'ABC23CD'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(postcode='ABC23CD').first()
        self.assertEqual(type(obj1), type(None))

        #Card Number Validation Tests

        temp = data.copy()
        temp['card_no'] = '012345678912345a'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_no='012345678912345a').first()
        self.assertEqual(type(obj1), type(None))     

        temp = data.copy()
        temp['card_no'] = '0!23456789123456'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_no='012345678912345a').first()
        self.assertEqual(type(obj1), type(None))     

        #Card Expiry Validation Tests

        temp = data.copy()
        temp['card_exp'] = '13/2025'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_exp='13/2025').first()
        self.assertEqual(type(obj1), type(None))     

        temp = data.copy()
        temp['card_exp'] = '01/2023'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_exp='01/20253').first()
        self.assertEqual(type(obj1), type(None))    

        temp = data.copy()
        temp['card_exp'] = '12/2022'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_exp='12/2022').first()
        self.assertEqual(type(obj1), type(None)) 

        temp = data.copy()
        temp['card_exp'] = '13 2025'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_exp='13 2025').first()
        self.assertEqual(type(obj1), type(None))     

        temp = data.copy()
        temp['card_exp'] = '3/2025'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_exp='3/2025').first()
        self.assertEqual(type(obj1), type(None))  

        temp = data.copy()
        temp['card_exp'] = '11/25'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(card_exp='11/25').first()
        self.assertEqual(type(obj1), type(None))  

        #cvv Validation Tests

        temp = data.copy()
        temp['cvv'] = '01a'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(cvv='01a').first()
        self.assertEqual(type(obj1), type(None))

        temp = data.copy()
        temp['cvv'] = '0!1'
        response = self.client.post('/payments', data=temp, subdomain="sess")
        obj1 = Customer.query.filter_by(cvv='0!1').first()
        self.assertEqual(type(obj1), type(None))


               


class TestHome(TestBase):
    def run_assertions(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'navbar', response.data)
        self.assertIn(b'<h1 class="font-impact">QA Cinemas</h1>', response.data)

    def test_get_base(self):
        self.run_assertions(self.client.get('/'))

    def test_get_home(self):
        self.run_assertions(self.client.get('/home'))


class TestFilm(TestBase):
    def setUpTestData(self) -> None:
        self.oppenheimer = Film(title="Oppenheimer")
        self.showing1 = Showing(date=date(2023, 9, 15), time=time(11, 00), film=self.oppenheimer)
        self.showing2 = Showing(date=date(2023, 9, 18), time=time(14, 15), film=self.oppenheimer)

        db.session.add(self.oppenheimer)
        db.session.commit()

    def test_post(self):
        response = self.client.post('/film/1', data=dict(date='2023-9-15'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Oppenheimer', response.data)
        self.assertIn(b'11:00', response.data)
        self.assertNotIn(b'14:15', response.data)

    @patch('routes.datetime')
    def test_get(self, datetime: Mock):
        datetime.now.return_value = Mock(date=lambda: date(2023, 9, 18))
        response = self.client.get('/film/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Oppenheimer', response.data)
        self.assertNotIn(b'11:00', response.data)
        self.assertIn(b'14:15', response.data)


class TestListings(TestBase):
    def setUpTestData(self) -> None:
        self.oppenheimer = Film(title="Oppenheimer", image_src="TestImage")

        db.session.add(self.oppenheimer)
        db.session.commit()

    def test_get(self):
        response = self.client.get('/listings')

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
