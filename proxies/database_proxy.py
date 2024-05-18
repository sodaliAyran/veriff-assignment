
class DatabaseProxy:

    def __init__(self):
        self._session_table: set[str] = set()
        self._image_encodings_table: dict[str, list[str]] = {}
        self._session_images_table: dict[str, list[str]] = dict()

    def insert_session(self, session_key: str):
        self._session_table.add(session_key)

    def validate_session(self, session_key: str) -> bool:
        return session_key in self._session_table

    def reset_session(self, session_key: str):
        self._session_images_table[session_key] = []


