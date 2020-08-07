# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse
import os


__all__ = ['douyin']

headers = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}


def douyin(url, out_path='./'):
    session = requests.Session()

    # 登录分享页面
    response = session.get(url, verify=False)
    uid = urlparse(response.url).path.split('/')[3]

    # 获取视频地址
    video_info = session.get('https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'.format(uid),
                             verify=False).json()

    # 获取下载链接
    download_items = [
        {
            'url_list': [url.replace('playwm', 'play') for url in item['video']['play_addr']['url_list']],
            'name': item['desc'],
        } for item in video_info['item_list']
    ]

    # 下载
    for item in download_items:
        for index, url in enumerate(item['url_list']):
            video_response = session.get(url=url, headers=headers, stream=True)
            if len(item['url_list']) == 1:
                filename = '{}.mp4'.format(item['name'])
            else:
                filename = '{}-{}.mp4'.format(item['name'], index)
            with open(os.path.join(out_path, filename), 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
