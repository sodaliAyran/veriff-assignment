from hashlib import sha256

from proxies.data_hasher_proxy import DataHasher


class DataHasherSha256Impl(DataHasher):

    def hash(self, data) -> str:
        hasher = sha256()
        hasher.update(data)
        return hasher.hexdigest()
