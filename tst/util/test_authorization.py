from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from fastapi import Response, Request

from util.authorization import auth


@auth
async def test_endpoint(request: Request):
    return Response(status_code=200)


class TestAuthDecorator(IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_request = MagicMock()
        self.mock_request.headers = {}

    async def test_auth_missing_key(self):
        response = await test_endpoint(request=self.mock_request)
        self.assertEqual(response.status_code, 403)

    @patch("util.authorization.session_handler")
    async def test_auth_valid_key(self, mock_session_handler):
        mock_session_handler.authorize.return_value = True
        self.mock_request.headers = {"key": "valid_api_key"}
        response = await test_endpoint(request=self.mock_request)
        self.assertEqual(response.status_code, 200)

    @patch("util.authorization.session_handler")
    async def test_auth_invalid_key(self, mock_session_handler):
        mock_session_handler.authorize.return_value = False
        self.mock_request.headers = {"key": "invalid_api_key"}
        response = await test_endpoint(request=self.mock_request)
        self.assertEqual(response.status_code, 403)

