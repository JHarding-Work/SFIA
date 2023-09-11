from unittest.mock import patch, Mock

from create import populate_with_retries
from sqlalchemy.exc import OperationalError
from tests import TestBase


class TestPopulateWithRetries(TestBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sqlalchemy_operational_error = OperationalError(None, [], BaseException())

    @patch('create.populate_db')
    def test_no_error(self, populate_db: Mock):
        populate_with_retries(5)
        populate_db.assert_called_once()

    @patch('create.populate_db')
    def test_with_one_error(self, populate_db: Mock):
        populate_db.side_effect = [self.sqlalchemy_operational_error, None]
        populate_with_retries(1)

    @patch('create.populate_db')
    def test_with_errors_exceeding_retries(self, populate_db: Mock):
        populate_db.side_effect = self.sqlalchemy_operational_error

        with self.assertRaises(OperationalError):
            populate_with_retries(1)