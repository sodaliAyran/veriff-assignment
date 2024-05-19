import unittest

from model.summary import ImageEncoding
from proxies import VeriffImageEncoderImpl
from util.exceptions import DependencyEmptyResponseException, DependencyBadRequestException, DependencyUnknownException, \
    DependencyTimeoutException


class VeriffImageEncoderTest(unittest.TestCase):

    def setUp(self):
        self.client = VeriffImageEncoderImpl()
        self.resource_path = '../resources'
        self.no_faces = "no_face.jpg"
        self.two_faces = "2_face.jpg"
        self.six_faces = "6_face.jpg"
        self.hq_image = "4k_image.jpg"
        self.txt_file = "invalid.txt"

    def _send_file(self, filename: str):
        with open(f"{self.resource_path}/{filename}", "rb") as f:
            file = f.read()
            response = self.client.encode(file)
        return response

    def test_noFaceImage_raisesResponseValidationException(self):
        with self.assertRaises(DependencyEmptyResponseException):
            self._send_file(self.no_faces)

    def test_validImage_returnsEncodings(self):
        response = self._send_file(self.two_faces)
        self.assertTrue(isinstance(response, ImageEncoding))
        self.assertEqual(2, len(response.faces))

    def test_invalidImage_raisesBadRequestException(self):
        with self.assertRaises(DependencyBadRequestException):
            self._send_file(self.six_faces)

    def test_invalidFile_raisesUnknownException(self):
        with self.assertRaises(DependencyUnknownException):
            self._send_file(self.txt_file)

    def test_hqFile_raisesTimeoutException(self):
        with self.assertRaises(DependencyTimeoutException):
            self._send_file(self.hq_image)
