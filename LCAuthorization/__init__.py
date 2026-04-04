from fastapi import Request, APIRouter, WebSocket
from pydantic import BaseModel
from fastapi.responses import *

from protocol.LCAuthorization_pb2 import *

api = APIRouter(prefix='/LinChan3-Competition/api/v1/authorization')

class TaskType:
    PushNewestAuthorizationCode = 1

class UploadData(BaseModel):
    clientToken:str
    rawMessage:str

@api.post('/upload')
async def upload(data:UploadData) -> dict:
    return {}

def unpack_envelope(msg:bytes) -> Any:
    envelope = Envelope.FromString(msg)

    match envelope.type:
        case TaskType.PushNewestAuthorizationCode:  # PushNewestAuthorizationCodeResponse
            return TaskType.PushNewestAuthorizationCode, PushNewestAuthorizationCodeResponse.FromString(envelope.data)

@api.websocket('/ws/monitor/{client_token}')
async def monitor(ws:WebSocket, client_token:str) -> None:
    if client_token == 'e8a99456-d452-411e-af4c-525edaeaa68d':
        try:
            await ws.accept()

            while True:
                raw = await ws.receive_bytes()
                msg = unpack_envelope(raw) 

        except Exception:
            await ws.close()
    else:
        await ws.close()