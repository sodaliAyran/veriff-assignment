from proxies.cache_proxy import CacheProxy
from proxies.database_proxy import DatabaseProxy
from proxies.image_hasher_sha256_impl import ImageHasher

DB_PROXY = DatabaseProxy()
CACHE_PROXY = CacheProxy()
IMAGE_HASHER = ImageHasher()
