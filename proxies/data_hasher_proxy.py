from abc import abstractmethod


class DataHasher:

    @abstractmethod
    def hash(self, data) -> str:
        pass
