import os

# Variables here can be acquired from env variables if necessary, but I decided to not do it for all.

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

API_KEY_REQUEST_HEADER_KEY = "key"

SESSION_IMAGE_LIMIT = 5


# To be honest this three should be bundled together in file called image_encoder_proxy_config
IMAGE_ENCODER_URL_ENV_VARIABLE = 'ENCODER_URL'
IMAGE_ENCODER_URL = os.environ.get(IMAGE_ENCODER_URL_ENV_VARIABLE, "http://face-encoding-app:8000/v1/selfie")
IMAGE_ENCODER_TIMEOUT = 2  # seconds
