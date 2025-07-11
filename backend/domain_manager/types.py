from enum import Enum
from typing import List

class HostType(Enum):
    Default = 0
    WebSocket = 1

class Host:
    def __init__(self, type: HostType, path: str, host: str):
        self.type = type
        self.path = path
        self.host = host

class Domain:
    def __init__(self, domain: str, hosts: List[Host]):
        self.domain = domain
        self.hosts = hosts