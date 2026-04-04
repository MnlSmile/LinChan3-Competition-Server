from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import *
from pydantic import BaseModel

from tinydb import Query
from tinybridge import AIOBridge
import httpx
import uuid

import os

api = APIRouter(prefix='/LinChan3/api/v1/auth')

ahttp = httpx.AsyncClient()


class URConnect:
    appid = 4016
    appkey = os.getenv('UR_CONNECT_APPKEY')
    redirect_url = 'http://auth.mnlsmile.cn/ur_callback'

    class Act:
        login = 'login'
        callback = 'callback'


def hex_uuid() -> str:
    return uuid.uuid4().hex
def bin_uuid() -> bytes:
    return uuid.uuid4().bytes
def str_uuid() -> str:
    return str(uuid.uuid4())


@api.get('/ur_login_callback')
async def ur_login_callback(type:str, code:str) -> FileResponse:
    resp = await ahttp.get(
        'https://uniqueker.top/connect.php',
        params={
            "act": URConnect.Act.callback,
            "appid": URConnect.appid,
            "appkey": URConnect.appkey,
            "type": 'qq',
            "code": code
        }
    )
    data:dict = resp.json()
    retcode:int = data.get('code')
    suid:str = data.get('social_uid')
    fimg:str = data.get('faceimg')
    name:str = data.get('nickname')

    match retcode:
        case 0:
            async with AIOBridge('linchan3.users.json') as db:
                user = Query()
                result = await db.search(user.qq_with_ur_connect == suid)
                if result.is_ok() and len(result) == 0:
                    result_ = await db.insert({
                        "uuid": str_uuid(),
                        "mc_major_profile_uuid": hex_uuid(),
                        "qq_with_ur_connect": suid
                    })
            return HTMLResponse(f"<p>Welcome, {name}</p>")
        case 2:
            return HTMLResponse(f"<p>User canceled</p>")
        case _:
            return HTMLResponse(f"<p>Login failed due to unknown reason</p>")