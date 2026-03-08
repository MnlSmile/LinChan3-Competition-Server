from fastapi import Request, APIRouter
from fastapi.responses import *
from pydantic import BaseModel

api = APIRouter(prefix='/LinChan3-Competition/api/v1/authserver')

class YggdrasilLogin(BaseModel):
    username:str
    password:str
    clientToken:str = '301ab721-623f-4640-bf39-984600bafb88'
    requestUser:bool = False
    agent:dict

@api.post('/authenticate')
async def login(data:YggdrasilLogin) -> dict:
    return {
        "accessToken": "c051b41d-4e24-47ea-83df-6da124cba00b",
        "clientToken": "a94942d9-84b4-4c13-9cf9-7df47ac2b80f",
        "availableProfiles": [
            {
                "id": "f43ef5ea1fc449928d37eaa0a5a7f3da",
                "name": "MnlSmile",
                "properties": []
            }
        ],
        "selectedProfile": {
            "id": "f43ef5ea1fc449928d37eaa0a5a7f3da",
            "name": "MnlSmile",
            "properties": []
        },
        "user": {
            "id": "3073c4fd-a015-4470-84fd-5169d6c9f98e",
            "properties": [
                {
                    "name": "preferredLanguage",
                    "value": "zh_CN",
                }
            ]
        }
    }

@api.get('/sessionserver/session/minecraft/profile/{uuid}')
async def profile(uuid:str) -> dict:
    return {
        "id": "f43ef5ea1fc449928d37eaa0a5a7f3da",
        "name": "MnlSmile",
        "properties": []
    }