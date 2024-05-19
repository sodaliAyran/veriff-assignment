import uuid

from util.metrics import latency
from proxies import DB_PROXY, DATA_HASHER


class SessionHandler:
    db_proxy = DB_PROXY
    data_hasher = DATA_HASHER

    def __init__(self):
        return

    @latency
    def create(self) -> uuid.uuid4():
        key = uuid.uuid4()
        session_hash = self.data_hasher.hash(key)
        self.db_proxy.insert_session(session_hash)
        return key

    @latency
    def authorize(self, session: str) -> bool:
        session_hash = self.data_hasher.hash(session)
        return self.db_proxy.validate_session(session_hash)

    @latency
    def reset(self, session: str):
        session_hash = self.data_hasher.hash(session)
        self.db_proxy.reset_session(session_hash)
