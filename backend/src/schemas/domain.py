from pydantic import BaseModel
from enum import Enum

class HostType(Enum):
    Default = "default"
    WebSocket = "websocket"

class Host(BaseModel):
    type: HostType
    path: str
    host: str

class Domain(BaseModel):
    domain: str
    hosts: list[Host]