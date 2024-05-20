from enum import Enum


class Paths(Enum):
    PING = "/ping"
    SESSION = "/session"
    SUMMARY = "/summary"
    ENCODE = "/encode"


class MediaType(Enum):
    JSON = "application/json"




