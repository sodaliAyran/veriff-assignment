from proxies.cache_proxy import CacheProxy
from proxies.database_proxy import DatabaseProxy
from proxies.data_hasher_sha256_impl import DataHasher
from proxies.image_encoder_veriff_impl import VeriffImageEncoderImpl

DB_PROXY = DatabaseProxy()
CACHE_PROXY = CacheProxy()
DATA_HASHER = DataHasher()
IMAGE_ENCODER = VeriffImageEncoderImpl()
