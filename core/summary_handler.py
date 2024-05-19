from model.summary import Summary
from util.metrics import latency
from proxies import DB_PROXY, CACHE_PROXY, DATA_HASHER


class SummaryHandler:
    db_proxy = DB_PROXY
    cache_proxy = CACHE_PROXY
    data_hasher = DATA_HASHER

    def __init__(self):
        return

    @latency
    def get_summary(self, session: str):
        session_hash = self.data_hasher.hash(session)
        session_images = self.db_proxy.get_session_images(session_hash)
        remaining_images, encodings = self.cache_proxy.get_encoding(session_images)
        remaining_encodings = self.db_proxy.get_encoding(remaining_images)
        self.cache_proxy.insert_encodings(remaining_encodings)
        encodings.extend(remaining_encodings.values())
        return Summary(image_encodings=encodings)
