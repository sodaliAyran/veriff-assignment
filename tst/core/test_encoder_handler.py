from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from core import EncoderHandler
from model.summary import ImageEncoding, FaceEncoding


class TestEncoderHandler(IsolatedAsyncioTestCase):
    def setUp(self):
        self.encoder_handler = EncoderHandler()
        self.MOCK_SESSION_ID = "mock_key"
        self.MOCK_SESSION_ID_HASH = "mock_key_hash"
        self.MOCK_IMAGE_HASH = "mock_hash"
        self.MOCK_IMAGE_DATA = bytes()
        self.MOCK_IMAGE_ENCODING = ImageEncoding(faces=[FaceEncoding(encoding=[0])])

    @patch('core.EncoderHandler.db_proxy')
    @patch('core.EncoderHandler.data_hasher')
    async def test_encode_over_image_limit_raises_exception(self, mock_data_hasher, mock_db_proxy):
        mock_data_hasher.hash = lambda hash_item: self.MOCK_IMAGE_HASH \
            if hash_item == self.MOCK_IMAGE_DATA else self.MOCK_SESSION_ID_HASH
        mock_db_proxy.get_session_limit.return_value = 5
        with self.assertRaises(ValueError):
            await self.encoder_handler.encode(self.MOCK_SESSION_ID, self.MOCK_IMAGE_DATA)

    @patch('core.EncoderHandler.db_proxy')
    @patch('core.EncoderHandler.image_encoder_proxy')
    @patch('core.EncoderHandler.data_hasher')
    async def test_encode_with_cached_image(self, mock_data_hasher,
                                            mock_image_encoder_proxy,
                                            mock_db_proxy):
        mock_data_hasher.hash = lambda hash_item: self.MOCK_IMAGE_HASH \
            if hash_item == self.MOCK_IMAGE_DATA else self.MOCK_SESSION_ID_HASH
        mock_db_proxy.get_session_limit.return_value = 0
        mock_db_proxy.contains_encoding.return_value = True

        await self.encoder_handler.encode(self.MOCK_SESSION_ID, self.MOCK_IMAGE_DATA)

        mock_image_encoder_proxy.encode.assert_not_called()
        mock_db_proxy.add_encoding.assert_not_called()

        mock_db_proxy.update_session.assert_called_once_with(self.MOCK_SESSION_ID_HASH, self.MOCK_IMAGE_HASH)

    @patch('core.EncoderHandler.db_proxy')
    @patch('core.EncoderHandler.image_encoder_proxy')
    @patch('core.EncoderHandler.data_hasher')
    async def test_encode_with_not_cached_image(self, mock_data_hasher,
                                                mock_image_encoder_proxy,
                                                mock_db_proxy):
        mock_data_hasher.hash = lambda hash_item: self.MOCK_IMAGE_HASH \
            if hash_item == self.MOCK_IMAGE_DATA else self.MOCK_SESSION_ID_HASH
        mock_db_proxy.get_session_limit.return_value = 0
        mock_db_proxy.contains_encoding.return_value = False
        mock_image_encoder_proxy.encode.return_value = self.MOCK_IMAGE_ENCODING

        await self.encoder_handler.encode(self.MOCK_SESSION_ID, self.MOCK_IMAGE_DATA)

        mock_image_encoder_proxy.encode.assert_called_once_with(self.MOCK_IMAGE_DATA)
        mock_db_proxy.add_encoding.assert_called_once_with(self.MOCK_IMAGE_HASH, self.MOCK_IMAGE_ENCODING)

        mock_db_proxy.update_session.assert_called_once_with(self.MOCK_SESSION_ID_HASH, self.MOCK_IMAGE_HASH)
