
from config import SESSION_IMAGE_LIMIT
from proxies import DB_PROXY, DATA_HASHER, IMAGE_ENCODER
from proxies.image_encoder_proxy import ImageEncoder
from util.exceptions import LimitReachedException
from util.metrics import latency


class EncoderHandler:
    db_proxy = DB_PROXY
    image_encoder_proxy: ImageEncoder = IMAGE_ENCODER
    data_hasher = DATA_HASHER

    @latency
    def encode(self, session: str, data: bytes):
        image_hash = self.data_hasher.hash(data)
        session_hash = self.data_hasher.hash(session)

        if self.db_proxy.get_session_limit(session_hash) >= SESSION_IMAGE_LIMIT:
            raise LimitReachedException(session_hash)

        if not self.db_proxy.contains_encoding(image_hash):  # I should check cache here but I won't
            encoding = self.image_encoder_proxy.encode(data)
            self.db_proxy.add_encoding(image_hash, encoding)
        self.db_proxy.update_session(session_hash, image_hash)
