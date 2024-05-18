import uuid

from util.metrics import latency
from proxies import db_proxy


class SessionHandler:

    def __init__(self):
        return

    @latency
    def create(self) -> uuid.uuid4():
        key = uuid.uuid4()
        db_proxy.insert_session(key)
        return key

    @latency
    def authorize(self, session: str) -> bool:
        return db_proxy.validate_session(session)

    @latency
    def reset(self, session: str):
        db_proxy.reset_session(session)



