from model.summary import ImageEncoding


class DatabaseProxy:

    def __init__(self):
        self._session_table: dict[str, list[str]] = dict()
        self._image_encodings_table: dict[str, ImageEncoding] = dict()

    def insert_session(self, session: str):
        self._session_table[session] = []

    def validate_session(self, session: str) -> bool:
        return session in self._session_table

    def reset_session(self, session: str):
        self._session_table[session] = []
        
    def get_session_images(self, session: str) -> list[str]:
        return self._session_table[session]

    def get_encoding(self, images: list[str]) -> list[ImageEncoding]:
        return [self._image_encodings_table[image] for image in images]


