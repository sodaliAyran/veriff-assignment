from model.summary import ImageEncoding
from util.lru_cache import LRUCache


class CacheProxy:
    def __init__(self):
        self._cache = LRUCache()

    def get_encoding(self, images: list[str]) -> (list[str], list[ImageEncoding]):
        encodings, remaining_images = [], []
        [(encodings.append(encoding)
          if (encoding := self._cache.get(image))
          else remaining_images.append(image))
         for image in images]
        return remaining_images, encodings

    def insert_encodings(self, encodings: dict[str, ImageEncoding]):
        for key, value in encodings.items():
            self._cache.put(key, value)
