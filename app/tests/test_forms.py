from datetime import time

from forms import BookingForm
from tests import TestBase


class TestBooking(TestBase):
    def setUp(self) -> None:
        self.form = BookingForm()

    def test_dt_time(self):
        self.form.time.data = '9:15'
        self.assertEqual(self.form.dt_time, time(9, 15))
