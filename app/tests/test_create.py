from unittest.mock import patch, Mock

from create import populate_with_retries
from sqlalchemy.exc import OperationalError
from tests import TestBase


class TestPopulateWithRetries(TestBase):
    @patch('create.populate_db')
    def test_no_error(self, populate_db: Mock):
        populate_with_retries(5)
        populate_db.assert_called_once()

    @patch('create.populate_db')
    def test_with_error(self, populate_db: Mock):
        populate_db.side_effect = [OperationalError(None, [], BaseException()), None]
        populate_with_retries(1)

