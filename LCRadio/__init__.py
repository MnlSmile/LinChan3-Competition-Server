from fastapi import Request, APIRouter
from pydantic import BaseModel
from fastapi.responses import *

from LCRadio.LCRadioPB_pb2 import *

api = APIRouter(prefix='/LinChan3-Competition/api/v1/music')

class TaskType:
    URLPlay = 1
    URLBrowse = 2
    URLCache = 3
    NCMPlay = 4
    NCMPluginPlay = 5
    NCMCache = 6
    DouyinPlay = 7
    DouyinBrowse = 8
    DouyinCache = 9
    BilibiliPlay = 10
    BilibiliBrowse = 11
    BilibiliCache = 12


class RequestTask(BaseModel):
    player:str
    ncm_factor:str


@api.post('/upload_task')
async def upload_task(rt:RequestTask) -> dict:
    
    return {}