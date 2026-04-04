from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import *
from pydantic import BaseModel

import httpx
import aiomysql
import pypika
import uuid

import os

api = APIRouter(prefix='/LinChan3/api/v1/auth')

ahttp = httpx.AsyncClient()


class URConnect:
    appid = 4016
    appkey = os.getenv('UR_CONNECT_APPKEY')


class MySQLConnectionPool:
    def __init__(self) -> None:
        self.pool = None
    async def initialize(self):
        self.pool = await aiomysql.create_pool(
            host='smp.mnlsmile.cn',
            port=3306,
            user='MnlSmile',
            password=os.getenv('MYSQL_PASSWORD'),
            db='linchan3-competition',
            minsize=1,
            maxsize=10,
            autocommit=False
        )
    async def acquire(self):
        if self.pool is None:
            await self.initialize()
        return await self.pool.acquire()
    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

pool = MySQLConnectionPool()


def hex_uuid() -> str:
    return uuid.uuid4().hex
def bin_uuid() -> bytes:
    return uuid.uuid4().bytes


@api.get('/ur_login_callback')
async def ur_login_callback(type:str, code:str) -> FileResponse:
    retry_count = 0
    while retry_count < 10:
        try:
            resp = await ahttp.get(f"https://uniqueker.top/connect.php?act=callback&appid={URConnect.appid}&appkey={URConnect.appkey}&type={type}&code={code}")
        except Exception:
            retry_count += 1
            continue
        else:
            break
    data:dict = resp.json()
    uid = data.get('social_uid')
    retcode = data.get('code')
    nickname = data.get('nickname')

    if not retcode and uid:
        db = await pool.acquire()
        async with db.cursor() as cur:
            lc = pypika.Table('linchan3')
            retry_count = 0
            query = pypika.MySQLQuery.from_(lc).select(
                lc.id
            ).where(
                lc.qq_uid_ur_connect == uid
            )
            while retry_count < 10:
                try:
                    await cur.execute(str(query))
                    result = await cur.fetchall()
                except Exception:
                    retry_count += 1
                    continue
                else:
                    if not len(result):
                        while retry_count < 10:
                            query = pypika.MySQLQuery.into(lc).columns(
                                'uuid', 'mc_major_profile_uuid', 'qq_uid_ur_connect'
                            ).insert(
                                bin_uuid(), bin_uuid(), uid
                            )
                            try:
                                await cur.execute(str(query))
                            except Exception:
                                retry_count += 1
                                continue
                            else:
                                return HTMLResponse(
                                    f"""<p>LinChan3 login succeeded: {nickname}</p>"""
                                )
                    else:
                        return HTMLResponse(
                            f"""<p>LinChan3 login succeeded: {nickname}</p>"""
                        )