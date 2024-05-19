import unittest
from unittest.mock import patch

from core import SummaryHandler
from model.summary import ImageEncoding, FaceEncoding, Summary


class TestSummaryHandler(unittest.TestCase):
    def setUp(self):
        self.summary_handler = SummaryHandler()
        self.mock_session = 'session'
        self.mock_session_hash = "session_hash"
        self.session_images = ['image1', 'image2', 'image3']
        self.image_encoding_1 = ImageEncoding(faces=[FaceEncoding(encoding=[1])])
        self.image_encoding_2 = ImageEncoding(faces=[FaceEncoding(encoding=[2])])
        self.image_encoding_3 = ImageEncoding(faces=[FaceEncoding(encoding=[3])])

    @patch('core.SummaryHandler.db_proxy')
    @patch('core.SummaryHandler.cache_proxy')
    @patch('core.SummaryHandler.data_hasher')
    def test_get_summary(self, mock_data_hasher, mock_cache_proxy, mock_db_proxy):
        image3 = 'image3'
        db_encoding = {image3: self.image_encoding_3}

        mock_data_hasher.hash.return_value(self.mock_session_hash)
        mock_db_proxy.get_session_images.return_value = self.session_images
        mock_cache_proxy.get_encoding.return_value = ([image3], [self.image_encoding_1,
                                                                   self.image_encoding_2])
        mock_db_proxy.get_encoding.return_value = db_encoding

        result = self.summary_handler.get_summary(self.mock_session)
        mock_cache_proxy.insert_encodings.assert_called_once_with(db_encoding)
        expected = Summary(image_encodings=[self.image_encoding_1, self.image_encoding_2, self.image_encoding_3])
        self.assertEqual(expected, result)
