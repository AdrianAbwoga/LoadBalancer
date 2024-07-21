import hashlib
import random
from typing import Set

def get_random_number(length: int) -> int:
    return int(''.join(random.choices('0123456789', k=length)))

class ConsistentHashing:
    def __init__(self, num_slots=512, num_virtual_servers=100):
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.consistent_hash = [None] * self.num_slots
        self.map = {}
        self.server_positions = {}

    def _hash(self, key):
        # Modified hash function
        return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % self.num_slots

    def hash_request(self, request_id: str) -> int:
        return self._hash(request_id)

    def hash_server(self, server_id: int, j: int) -> int:
        # Modified hash function
        return (server_id * 3 + j * 7 + 19) % self.num_slots

    def get_server_id(self, server: str) -> int:
        return self.map.get(server)

    def build(self, server_list: Set[str]):
        for server in server_list:
            self.add_server(server)

    def add_server(self, server: str):
        server_id = get_random_number(6)
        self.map[server] = server_id
        self.server_positions[server] = []
        for j in range(self.num_virtual_servers):
            pos = self.hash_server(server_id, j)
            while self.consistent_hash[pos] is not None:
                pos = (pos + 1) % self.num_slots
            self.consistent_hash[pos] = server
            self.server_positions[server].append(pos)

    def remove_server(self, server: str):
        server_id = self.get_server_id(server)
        if server_id is None:
            return
        for pos in self.server_positions[server]:
            self.consistent_hash[pos] = None
        del self.map[server]
        del self.server_positions[server]

    def get_replicas(self):
        return list(self.map.keys())

    def get_server_url(self, path: str):
        req_pos = self.hash_request(path)
        for i in range(self.num_slots):
            if self.consistent_hash[req_pos] is not None:
                return self.consistent_hash[req_pos]
            req_pos = (req_pos + 1) % self.num_slots
        return None
