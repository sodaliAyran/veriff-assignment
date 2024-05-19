from model.summary import ImageEncoding


class DatabaseProxy:

    def __init__(self):
        self._session_table: dict[str, list[str]] = dict()
        self._image_encodings_table: dict[str, ImageEncoding] = dict()

    def insert_session(self, session_hash: str):
        self._session_table[session_hash] = []

    def update_session(self, session_hash: str, image_hash: str):
        self._session_table[session_hash].append(image_hash)

    def get_session_limit(self, session_hash: str) -> int:
        return len(self._session_table[session_hash])

    def validate_session(self, session_hash: str) -> bool:
        return session_hash in self._session_table

    def reset_session(self, session_hash: str):
        self._session_table[session_hash] = []
        
    def get_session_images(self, session_hash: str) -> list[str]:
        return self._session_table[session_hash]

    def add_encoding(self, image_hash: str, encoding: ImageEncoding):
        self._image_encodings_table[image_hash] = encoding

    def get_encoding(self, images: list[str]) -> dict[str, ImageEncoding]:
        return {image: self._image_encodings_table[image] for image in images}

    def contains_encoding(self, image_hash: str) -> bool:
        return image_hash in self._image_encodings_table


