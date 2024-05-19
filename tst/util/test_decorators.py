from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from fastapi import Response, Header

from util.decorators import auth


@auth
async def test_endpoint(key: Optional[str] = Header(None)):
    return Response(status_code=200)


class TestAuthDecorator(IsolatedAsyncioTestCase):

    async def test_auth_missing_key(self):
        response = await test_endpoint()
        self.assertEqual(403, response.status_code)

    @patch("util.decorators.session_handler")
    async def test_auth_valid_key(self, mock_session_handler):
        mock_session_handler.authorize.return_value = True
        response = await test_endpoint(key="VALID")
        self.assertEqual(200, response.status_code)

    @patch("util.decorators.session_handler")
    async def test_auth_invalid_key(self, mock_session_handler):
        mock_session_handler.authorize.return_value = False
        response = await test_endpoint(key="INVALID")
        self.assertEqual(403, response.status_code)

