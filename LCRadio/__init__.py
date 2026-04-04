from fastapi import Request, APIRouter
from pydantic import BaseModel
from fastapi.responses import *

import bilibili_api as bili

from LCRadio.LCRadioPB_pb2 import *

api = APIRouter(prefix='/LinChan3-Competition/api/v1/radio')

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


class UploadTaskRequest(BaseModel):
    player:str
    ncm_factor:str


@api.post('/upload_task')
async def upload_task(rt:UploadTaskRequest) -> dict:
    
    return {}


class SimpleMinecraftDownloadBilibiliSubtitlesRequest(BaseModel):
    factor:str

@api.post('/simple/minecraft/download_bilibili_subtitles')
async def download_bilibili_subtitles(data:SimpleMinecraftDownloadBilibiliSubtitlesRequest) -> dict:
    video = bili.video.Video('BV1Q4411F7Qd')
    video.get_detail()
    _dms = await video.get_danmakus()
    dms:list[bili.Danmaku] = []
    for dm in _dms:
        if dm.text:
            dms.append(dm)
    dms.sort(key=lambda dm:dm.dm_time)

    mc_dms = []

    if len(dms):
        ltick = int(dms[-1].dm_time // 0.05)
        mc_dms = [[]] * (ltick + 1)
    
    for dm in dms:
        mc_dms[int(dm.dm_time // 0.05)].append(dm.text)
    
    return {
        'status': 'ok',
        'minecraft_danmakus': mc_dms
    }