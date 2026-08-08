from collections import defaultdict


class APIKeyCache:

    def __init__(self):
        self.store:dict[int, tuple[str, str]] = defaultdict()

    def add(self, key_id:int, token:str):
        self.store[key_id] = token

    def pop(self, key_id:int) -> tuple[str, str]:
        if key_id in self.store:
            return self.store.pop(key_id)

API_KEY_CACHE = APIKeyCache()