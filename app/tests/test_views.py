from flask import url_for

from tests import TestBase


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
        response = self.client.get('/film/1')
        self.assertEqual(response.status_code, 200)
