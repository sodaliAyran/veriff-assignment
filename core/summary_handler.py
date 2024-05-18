from model.summary import Summary
from util.metrics import latency
from proxies import DB_PROXY, CACHE_PROXY


class SummaryHandler:
    db_proxy = DB_PROXY
    cache_proxy = CACHE_PROXY

    def __init__(self):
        return

    @latency
    def get_summary(self, session: str):
        session_images = self.db_proxy.get_session_images(session)
        remaining_images, encodings = self.cache_proxy.get_encoding(session_images)
        encodings.extend(self.db_proxy.get_encoding(remaining_images))
        return Summary(image_encodings=encodings)
