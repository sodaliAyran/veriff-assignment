from enum import Enum


class Paths(Enum):
    PING = "/ping"
    SESSION = "/session"
    SUMMARY = "/summary"
    ENCODE = "/encode"


class MediaType(Enum):
    JSON = "application/json"


MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

API_KEY_REQUEST_HEADER_KEY = "key"

IMAGE_ENCODER_URL = 'ENCODER_URL'

SESSION_IMAGE_LIMIT = 5
