import os

import requests
from pydantic import ValidationError
from requests import Response

from util.constants import IMAGE_ENCODER_URL
from model.summary import ImageEncoding, FaceEncoding
from proxies.image_encoder_proxy import ImageEncoder
from util.exceptions import (DependencyTimeoutException,
                             DependencyUnknownException,
                             DependencyResponseValidationException,
                             DependencyEmptyResponseException,
                             DependencyBadRequestException)


class VeriffImageEncoderImpl(ImageEncoder):
    DEFAULT_ENCODER_URL = "http://localhost:8000/v1/selfie"
    TIMEOUT = 2  # seconds
    __name__ = "VeriffImageEncoder"

    def __init__(self):
        self.url = os.environ.get(IMAGE_ENCODER_URL, self.DEFAULT_ENCODER_URL)

    def encode(self, data: bytes) -> ImageEncoding:
        try:
            response = requests.post(self.url,
                                     files={"file": data},
                                     timeout=self.TIMEOUT)
        except requests.Timeout:
            raise DependencyTimeoutException(self.encode, self.__name__)
        return self._handle_response(response)

    def _handle_response(self, response: Response) -> ImageEncoding:
        match response.status_code:
            case 200:
                if response.json():
                    try:
                        image_encoding = ImageEncoding(faces=[FaceEncoding(encoding=encoding)
                                                              for encoding in response.json()])
                        return image_encoding
                    except ValidationError as e:
                        raise DependencyResponseValidationException(self.encode, self.__name__, e)
                else:
                    raise DependencyEmptyResponseException(self.encode, self.__name__)
            case 400 | 422:
                raise DependencyBadRequestException(self.__name__, response.json())
            case _:
                raise DependencyUnknownException(self.__name__, response)
