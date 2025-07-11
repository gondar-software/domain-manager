from pydantic import BaseModel
from enum import Enum

class HostType(Enum):
    Default = 0
    WebSocket = 1

class Host(BaseModel):
    type: HostType
    path: str
    host: str

class Domain(BaseModel):
    domain: str
    hosts: list[Host]