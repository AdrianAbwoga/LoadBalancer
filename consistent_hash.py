import hashlib
import bisect

class ConsistentHash:
    def __init__(self, replicas=3, max_slots=512):
        self.replicas = replicas
        self.max_slots = max_slots
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.max_slots

    def add_node(self, node):
        for i in range(self.replicas):
            replica_key = f'{node}:{i}'
            hashed_key = self._hash(replica_key)
            self.ring[hashed_key] = node
            bisect.insort(self.sorted_keys, hashed_key)

    def remove_node(self, node):
        for i in range(self.replicas):
            replica_key = f'{node}:{i}'
            hashed_key = self._hash(replica_key)
            self.ring.pop(hashed_key)
            self.sorted_keys.remove(hashed_key)

    def get_node(self, key):
        if not self.ring:
            return None
        hashed_key = self._hash(key)
        index = bisect.bisect(self.sorted_keys, hashed_key)
        if index == len(self.sorted_keys):
            index = 0
        return self.ring[self.sorted_keys[index]]
