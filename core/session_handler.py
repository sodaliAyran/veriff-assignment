import uuid

from util.metrics import latency
from proxies import db_proxy


class SessionHandler:
    db_proxy = db_proxy

    def __init__(self):
        return

    @latency
    def create(self) -> uuid.uuid4():
        key = uuid.uuid4()
        self.db_proxy.insert_session(key)
        return key

    @latency
    def authorize(self, session: str) -> bool:
        return self.db_proxy.validate_session(session)

    @latency
    def reset(self, session: str):
        self.db_proxy.reset_session(session)
