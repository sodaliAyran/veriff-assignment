import unittest
from unittest.mock import patch

from core import SessionHandler


class TestSessionHandler(unittest.TestCase):
    def setUp(self):
        self.session_handler = SessionHandler()
        self.MOCK_SESSION_ID = "mock_key"

    @patch('core.SessionHandler.db_proxy')
    def test_create(self, mock_db_proxy):
        mock_db_proxy.insert_session.return_value = None

        with patch('uuid.uuid4', return_value=self.MOCK_SESSION_ID):
            result = self.session_handler.create()
            mock_db_proxy.insert_session.assert_called_once_with(self.MOCK_SESSION_ID)
            self.assertEqual(result, self.MOCK_SESSION_ID)

    @patch('core.SessionHandler.db_proxy')
    def test_authorize(self, mock_db_proxy):
        mock_db_proxy.validate_session.return_value = True
        session_handler = SessionHandler()
        result = session_handler.authorize(self.MOCK_SESSION_ID)
        self.assertTrue(result)
        mock_db_proxy.validate_session.assert_called_once_with(self.MOCK_SESSION_ID)

    @patch('core.SessionHandler.db_proxy')
    def test_reset(self, mock_db_proxy):
        session_handler = SessionHandler()
        session_handler.reset(self.MOCK_SESSION_ID)
        mock_db_proxy.reset_session.assert_called_once_with(self.MOCK_SESSION_ID)