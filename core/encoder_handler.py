from proxies import DB_PROXY, DATA_HASHER
from proxies.image_encoder_proxy import ImageEncoder
from util.metrics import latency


class EncoderHandler:
    db_proxy = DB_PROXY
    image_encoder_proxy: ImageEncoder = any
    data_hasher = DATA_HASHER

    @latency
    async def encode(self, session: str, data: bytes):
        image_hash = self.data_hasher.hash(data)
        session_hash = self.data_hasher.hash(session)

        if not self.db_proxy.contains_encoding(image_hash):  # I should check cache here but I won't
            encoding = self.image_encoder_proxy.encode(data)
            self.db_proxy.add_encoding(image_hash, encoding)
        self.db_proxy.update_session(session_hash, image_hash)
