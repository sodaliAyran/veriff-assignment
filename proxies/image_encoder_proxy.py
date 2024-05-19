from abc import abstractmethod

from model.summary import ImageEncoding


class ImageEncoder:

    @abstractmethod
    def encode(self, data: bytes) -> ImageEncoding:
        pass
