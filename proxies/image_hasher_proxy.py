from abc import abstractmethod

from fastapi import UploadFile


class ImageHasher:

    @abstractmethod
    def hash(self, image: UploadFile) -> str:
        pass