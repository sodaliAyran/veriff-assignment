from collections.abc import Buffer
from hashlib import sha256


class ImageHasher:

    def hash(self, data: Buffer) -> str:
        hasher = sha256()
        hasher.update(data)
        return hasher.hexdigest()
