from model.summary import ImageEncoding


class DatabaseProxy:

    def __init__(self):
        self._session_table: dict[str, list[str]] = dict()
        self._image_encodings_table: dict[str, ImageEncoding] = dict()

    def insert_session(self, session: str):
        self._session_table[session] = []

    def update_session(self, session: str, image_hash: str):
        self._session_table[session].append(image_hash)

    def validate_session(self, session: str) -> bool:
        return session in self._session_table

    def reset_session(self, session: str):
        self._session_table[session] = []
        
    def get_session_images(self, session: str) -> list[str]:
        return self._session_table[session]

    def add_encoding(self, image_hash: str, encoding: ImageEncoding):
        self._image_encodings_table[image_hash] = encoding

    def get_encoding(self, images: list[str]) -> list[ImageEncoding]:
        return [self._image_encodings_table[image] for image in images]

    def contains_encoding(self, image_hash: str) -> bool:
        return image_hash in self._image_encodings_table


