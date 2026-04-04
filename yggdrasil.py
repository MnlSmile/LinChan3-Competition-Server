from fastapi import Request, APIRouter
from fastapi.responses import *
from pydantic import BaseModel

import json
import rsa
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend



# 提供的 RSA 私钥（PEM 格式）
PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQDxq9ixn4smfiXe
/iaGH3bddt2rakI249uLBMKvUVaL99UHkpdOHSgE2J3X6Hu9NeT5mYdRNFXd6SmP
0diAra9bVYdlRXyxR+P+r/jMtqyWeoZBmqZ4Uhwic30BvXh4GTDXRHZgLV90jDZR
puXcjj7r1BpBdP0dPT5J9f+rOEzSZ0gNgsXS9Woyph0YY0IiXwqbFRwAcFsCe8t/
tAP4lHWNhVdhUvByzjhRAE28A022QuZ3XYbk3Lda0R2x/MJbdeW5aKUimYNaj6mN
UdXaWcHwagOfcVW+J2CZRl8ynDsSUTYaDiPs53ezg0pnyrwtTLrdckVjgiv3THRw
5p7au62jAgMBAAECggEBANwSwaH+x5imB5apmitJO9UxCWuvt9yEYsiV7TP5vfZ4
GWZr950KsAa5vAOBki0bhwhE5xTrs8YBLffqAF4tzCJAIKv4OzS1YsnrNYY2U7Q0
n03epvmqzDQTNyL+h1XWmsNtdN7gcqyPgmeYtHnEj0fyPnadMmIOA0sW2VvySQLP
hXpkFhu4nyFFlEs29Pj7L2sroRQHcKZMWfqgrrrhCwohJlojL7oWY4/1xbP/UjRT
yq9c4G2zIzy7WI6gCOFC2LBo9AJR19eKI/lKwSQGfX2iw03Wk1RJTXjPL8U0SHjC
AIlbC+w0Y/JDDJtSBrGKBvX31ht4qARn8IIxmgjtqwECgYEA//uVd4PPinUVFh1B
nsVJ48eI6gVrFFenU/RAoKm7lpZZkZw7Ift+daF5tbMwDq3plvKQLFj3YBF5eUSF
sRNJaCLpxB7yuyQsLAF6b2aMgN5QVJ/p7R/T/SUNd/yZCkbRgKuT2vqidVOYV72R
i8bE5gL2SJttTRYSUDjPQIjzX8cCgYEA8bAEBWwMOjl/Oj8HjpFy3i+JZbsn2MvJ
WOeUJ3q0VT2JLfl8yqJi/NvkHbBnmoEd4QGuZre8o0NyLjMFld/wZO9MnvD1UqxK
hwC6dgmGjlVb+o9oyyDhLRZ7/Tkm9U2U4FjPBhEnJ0VCHcX09aK36BIU/I+9R8Nf
QC2DRnVwO0UCgYEAkGbx2CvJJggKTyFN5SzSE+Z5u9o2n5Ea2WdOFdPp+Hb0LAn/
6Zmfqufearucfoto3DgVUI8XbWAuMFSRPmTs4gvf5zy2HQ+4w1JKKRGmbQP8OODE
63kq8wC16lvaUUvF31nq3HrKrnjr1YMg2cLVTBObrzXOoM+0oQCLGZKoB/0CgYEA
vJkS+jwvanwVqRkoR3t+vJ0xxZ3/YTDdJTBJL2mUMXQ8iRDH7cQ8JH9fCj/vCOU6
sKvEMUmtvWVTQ3PzJtpCWDFYhCsZ9PKXkbPizVtvkcBQbzzblK9KqAmEpbykhwWM
aGlE28Ik4IMuLdec6NWaV1FM6S0tkkOGH6mkaCYad1UCgYEApOf2C+LrqvP0Zbqm
JINFeFwVGadydyhZvrLgyhTjaPuBMaGVJHEDUfMQUpnwAIeznWQtuxXzgjHFY1Uy
pAvu1I7ZkAAjlPqF3LmShs4srpMUdzFHvOjMll2v+2TaFcSeoDeQRqiQAId/5831
fltqt3aLu6J3tLWny88RGnBHGrc=
-----END PRIVATE KEY-----"""

def sign_sha1_with_rsa(original_str: str) -> str:
    """
    对输入的字符串原文进行 SHA1WithRSA 签名，返回 Base64 编码的签名结果。

    :param original_str: 待签名的原始字符串
    :return: Base64 编码的签名
    """
    # 加载 PEM 格式的私钥
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY_PEM.encode('utf-8'),
        password=None,
        backend=default_backend()
    )

    # 将字符串转换为字节
    message_bytes = original_str.encode('utf-8')

    # 使用 SHA1 和 PKCS#1 v1.5 填充进行签名
    signature = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA1()
    )

    # 对签名结果进行 Base64 编码并返回
    return base64.b64encode(signature).decode('utf-8')

api = APIRouter(prefix='/LinChan3-Competition/api/v1/yggdrasil')
texture_api = APIRouter(prefix='/linchan3-competition/api/v1/yggdrasil')

@api.get('/')
async def meta() -> dict:
    resp = {
        "meta": {
            "implementationName": "LinChan3-Competition Auth Server",
            "implementationVersion": "0.0.1",
            "serverName": "LinChan3-Competition Auth Server",
            "links": {
                "homepage": "https://www.mnlsmile.cn",
                "register": "https://www.mnlsmile.cn/register"
            },
            "feature.non_email_login": True
        },
        "skinDomains": [
            "mnlsmile.cn",
            ".mnlsmile.cn",
            "littleskin.cn",
            ".littleskin.cn"
        ],
        "signaturePublickey": """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8avYsZ+LJn4l3v4mhh92
3Xbdq2pCNuPbiwTCr1FWi/fVB5KXTh0oBNid1+h7vTXk+ZmHUTRV3ekpj9HYgK2v
W1WHZUV8sUfj/q/4zLaslnqGQZqmeFIcInN9Ab14eBkw10R2YC1fdIw2Uabl3I4+
69QaQXT9HT0+SfX/qzhM0mdIDYLF0vVqMqYdGGNCIl8KmxUcAHBbAnvLf7QD+JR1
jYVXYVLwcs44UQBNvANNtkLmd12G5Ny3WtEdsfzCW3XluWilIpmDWo+pjVHV2lnB
8GoDn3FVvidgmUZfMpw7ElE2Gg4j7Od3s4NKZ8q8LUy63XJFY4Ir90x0cOae2rut
owIDAQAB
-----END PUBLIC KEY-----"""
    }
    return resp

class YggdrasilLoginRequestData(BaseModel):
    username:str
    password:str
    clientToken:str = '301ab721-623f-4640-bf39-984600bafb88'
    requestUser:bool = False
    agent:dict

@api.post('/authserver/authenticate')
async def login(data:YggdrasilLoginRequestData) -> dict:
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
            "id": "3073c4fda015447084fd5169d6c9f98e",
            "properties": [
                {
                    "name": "preferredLanguage",
                    "value": "zh_CN",
                }
            ]
        }
    }

class YggdrasilRefreshRequestData(BaseModel):
    accessToken:str
    clientToken:str
    requestUser:bool
    selectedProfile:dict

@api.post('/authserver/refresh')
async def refresh(data:YggdrasilRefreshRequestData) -> dict:
    return {
        "accessToken":"f4190ec9b1b84fcfb4beed2bc7f19df7",
        "clientToken":"e8f79924b0b74df0bfa611aee824024a",
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

class YggdrasilValidateRequestData(BaseModel):
    accessToken:str
    clientToken:str

@api.post('/authserver/validate')
async def validate(data:YggdrasilValidateRequestData) -> Response:
    return Response(status_code=204)

class YggdrasilInvalidateRequestData(BaseModel):
    accessToken:str
    clientToken:str

@api.post('/authserver/invalidate')
async def validate(data:YggdrasilInvalidateRequestData) -> Response:
    return Response(status_code=204)

class YggdrasilSignoutRequestData(BaseModel):
    username:str
    password:str

@api.post('/authserver/signout')
async def validate(data:YggdrasilSignoutRequestData) -> Response:
    return Response(status_code=204)

@api.get('/e051c27e803ba15de78a1d1e83491411dffb6d7fd2886da0a6c34a2161f7ca99')
async def _default_skin2() -> FileResponse:
    return FileResponse('F:/const_images/三月七(来自littleskin).png')

@texture_api.get('/e051c27e803ba15de78a1d1e83491411dffb6d7fd2886da0a6c34a2161f7ca99')
async def _default_skin() -> FileResponse:
    return FileResponse('F:/const_images/三月七(来自littleskin).png')

@api.get('/4ec65514dafd438a8d3a89be3ca5a9bf64d5adf2a7cb466f91e0a0265f06e210')
async def _default_cape2() -> FileResponse:
    return FileResponse('F:/const_images/超精致（细节）白毛龙娘最终无瑕疵版【自改+自改鞘翅】.png')

@api.get('/sessionserver/session/minecraft/profile/{uuid}')
async def profile(uuid:str, unsigned:bool=False) -> dict:
    texture = {
        "timestamp": 1774711508000,
        "profileId": "f43ef5ea1fc449928d37eaa0a5a7f3da",
        "profileName": "MnlSmile",
        "textures": {
            "SKIN": {
                "url": "http://localhost.mnlsmile.cn:5799/LinChan3-Competition/api/v1/yggdrasil/e051c27e803ba15de78a1d1e83491411dffb6d7fd2886da0a6c34a2161f7ca99"
            },
            "CAPE": {
                "url": "http://localhost.mnlsmile.cn:5799/LinChan3-Competition/api/v1/yggdrasil/4ec65514dafd438a8d3a89be3ca5a9bf64d5adf2a7cb466f91e0a0265f06e210"
                #"url": "https://littleskin.cn/raw/154734"
            }
        }
    }
    _jr = json.dumps(texture)
    _jb64 = base64.b64encode(_jr.encode('utf-8')).decode('utf-8')
    return {
        "id": "f43ef5ea1fc449928d37eaa0a5a7f3da",
        "name": "MnlSmile",
        "properties": [
            {
                "name": "textures",
                "value": _jb64,
                "signature": sign_sha1_with_rsa(_jb64)
		    }
        ]
    }