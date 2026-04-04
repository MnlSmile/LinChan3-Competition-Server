import bilibili_api as bili
import asyncio as aio
import asyncqt as aqt
import time
import json
import sys

from stdqt import *

def danmaku_sort_comparison(dm:bili.Danmaku) -> float:
    return dm.dm_time

app = QApplication(sys.argv)

window = QWidget()
window.setGeometry((1920 - 1280) // 2, (1080 - 720) // 2, 1280, 720)
window.setWindowTitle('LinChan3-Radio')

video = bili.video.Video('BV1ut411P7Sz')

web = QWebEngineView(window)
web.setGeometry(100, 100, 960, 540)
web.load(QUrl(
    """https://player.bilibili.com/player.html?bvid=BV1ut411P7Sz&p=1&high_quality=1&danmaku=0&autoplay=false"""
))
web.load(QUrl(
    """https://www.bilibili.com/video/BV1ut411P7Sz/?spm_id_from=333.788.recommend_more_video.0&trackid=web_related_0.router-related-2481894-ksftd.1774155524481.989&vd_source=137f1235ddb32630db7ec27a195a0343"""
))

window.show()

app.exec()