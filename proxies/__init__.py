from proxies.cache_proxy import CacheProxy
from proxies.database_proxy import DatabaseProxy
from proxies.data_hasher_sha256_impl import DataHasher

DB_PROXY = DatabaseProxy()
CACHE_PROXY = CacheProxy()
DATA_HASHER = DataHasher()
