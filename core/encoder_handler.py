import logging

from proxies import DB_PROXY, DATA_HASHER, IMAGE_ENCODER
from proxies.image_encoder_proxy import ImageEncoder
from util.constants import SESSION_IMAGE_LIMIT
from util.metrics import latency


class EncoderHandler:
    db_proxy = DB_PROXY
    image_encoder_proxy: ImageEncoder = IMAGE_ENCODER
    data_hasher = DATA_HASHER

    @latency
    async def encode(self, session: str, data: bytes):
        image_hash = self.data_hasher.hash(data)
        session_hash = self.data_hasher.hash(session)

        if self.db_proxy.get_session_limit(session_hash) >= SESSION_IMAGE_LIMIT:
            logging.error(f"User: '{session_hash}' reached its image upload limit.")
            raise ValueError

        if not self.db_proxy.contains_encoding(image_hash):  # I should check cache here but I won't
            encoding = self.image_encoder_proxy.encode(data)
            self.db_proxy.add_encoding(image_hash, encoding)
        self.db_proxy.update_session(session_hash, image_hash)
