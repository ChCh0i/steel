# No Threshold
![js](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white) ![js](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![js](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

<img width="1468" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/08619760-81e0-4655-95dd-c3fd9a9f77ac">

## 개요
 - HackTheBox web chaining 문제였습니다.
 - multi threding 을 활용하여 문제에 접근중 haproxy.cfg acl 정책을 제대로 확인하지못하여 어려움이 있었습니다.

## Preview
<img width="1469" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/ba075da6-dd5c-4297-86af-9a38bc59dac5">

## Source
 - index.py
```
from flask import Blueprint, render_template

index_bp = Blueprint(
    "index",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


@index_bp.route("/", methods=["GET"])
def index():
    return render_template("public/index.html")
```

 - login.py
```
from flask import Blueprint, render_template, request, jsonify, redirect
from app.database import *
import random
import string
import uwsgi

login_bp = Blueprint("login", __name__, template_folder="templates")


def set_2fa_code(d):
    uwsgi.cache_del("2fa-code")
    uwsgi.cache_set(
        "2fa-code", "".join(random.choices(string.digits, k=d)), 300 # valid for 5 min
    ) 


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("public/login.html", error_message="Username or password is empty!"), 400
        try:
            user = query_db(
                f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'",
                one=True,
            )

            if user is None:
                return render_template("public/login.html", error_message="Invalid username or password"), 400

            set_2fa_code(4)

            return redirect("/auth/verify-2fa")
        finally:
            close_db()
    return render_template("public/login.html")
```

 - verify2fa.py
```
from flask import Blueprint, render_template, request, jsonify, session, redirect
import uwsgi

verify2fa_bp = Blueprint("verify2fa", __name__, template_folder="templates")

def requires_2fa(func):
    def wrapper(*args, **kwargs):
        if uwsgi.cache_exists("2fa-code"):
            return func(*args, **kwargs)
        else:
            return redirect("/auth/login")

    return wrapper


@verify2fa_bp.route("/verify-2fa", methods=["GET", "POST"])
@requires_2fa
def verify():
    if request.method == "POST":

        code = request.form.get("2fa-code")
        
        if not code:
            return render_template("private/verify2fa.html", error_message="2FA code is empty!"), 400

        stored_code = uwsgi.cache_get("2fa-code").decode("utf-8")

        if code == stored_code:
            uwsgi.cache_del("2fa-code")
            session["authenticated"] = True
            return redirect("/dashboard")

        else:
            return render_template("private/verify2fa.html", error_message="Invalid 2FA Code!"), 400
    return render_template("private/verify2fa.html")
```

 - dashboard.py
```
from flask import Blueprint, render_template, request, jsonify, session, redirect
from app.config import Config

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

def requires_authentication(func):
    def wrapper(*args, **kwargs):
        if session.get("authenticated"):
            return func(*args, **kwargs)
        else:
            return redirect("/auth/login")

    return wrapper


@dashboard_bp.route("/dashboard", methods=["GET"])
@requires_authentication
def dash():
    return render_template("private/dashboard.html", flag=Config.FLAG)
```

  - config.py
```
import os

class Config:
    DATABASE_URI = '/opt/www/app/nothreshold.db' 
    SECRET_KEY = os.urandom(69)
    FLAG = "HTB{f4k3_fl4g_f0r_t3st1ng}"
```

 - haproxy.cfg
```
global
    daemon
    maxconn 256

defaults
    mode http
    option forwardfor

    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend haproxy
    bind 0.0.0.0:1337
    default_backend backend

    # Parse the X-Forwarded-For header value if it exists. If it doesn't exist, add the client's IP address to the X-Forwarded-For header. 
    http-request add-header X-Forwarded-For %[src] if !{ req.hdr(X-Forwarded-For) -m found }
    
    # Apply rate limit on the /auth/verify-2fa route.
    acl is_auth_verify_2fa path_beg,url_dec /auth/verify-2fa

    # Checks for valid IPv4 address in X-Forwarded-For header and denies request if malformed IPv4 is found. (Application accepts IP addresses in the range from 0.0.0.0 to 255.255.255.255.)
    acl valid_ipv4 req.hdr(X-Forwarded-For) -m reg ^([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])$
    
    http-request deny deny_status 400 if is_auth_verify_2fa !valid_ipv4

    # Crate a stick-table to track the number of requests from a single IP address. (1min expire)
    stick-table type ip size 100k expire 60s store http_req_rate(60s)

    # Deny users that make more than 20 requests in a small timeframe.
    http-request track-sc0 hdr(X-Forwarded-For) if is_auth_verify_2fa
    http-request deny deny_status 429 if is_auth_verify_2fa { sc_http_req_rate(0) gt 20 }

    # External users should be blocked from accessing routes under maintenance.
    http-request deny if { path_beg /auth/login }

backend backend
    balance roundrobin
    server s1 0.0.0.0:8888 maxconn 32 check
```

## 시나리오
 - ```/auth/login``` 페이지를 소스하면 아래와같이 403 권한에러가 발생합니다.
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/3a0b01e1-d5a8-430c-b9bf-6cdf53ff5bf5">

 - ```//``` double slash를 활용하여 403 bypass ```http://94.237.54.50:55121//auth/login```
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/0dcc0a8e-5e07-4aba-b7da-9fbc27d8c446">

 - ```login.py``` 을 보았을때 ```post``` method 로 request 전송시 코드가 실행됩니다.
 - 이후 ```username``` & ```password``` 를 입력받아 body 에 실어 request를 보내게 되고
 - 해당 입력값을 query data와 비교하여 반환합니다. 이후 쿼리데이터가 맞을시 ```one``` 이라는 컬럼을 true로 보낸값을 ```verify-2fa``` 라는 페이지를 리다이렉트할때 같이 보내게됩니다.
 - 다음으로 entrypoint.sh의 데이터베이스 생성구문을 확인해보면 다음과 같다.
 - ```INSERT INTO users (username, password) VALUES ('admin', '$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)');```
 - 해당 내용으로 username 의 값은 ```admin``` 인것을 확인할수있다. 패스워드는 쿼리를 평문으로 받고있기때문에 sqli가 발생하는것을 알수있다.
 - ```username : admin'-- -``` & ```password : 1``` 이런식으로 값을주기되면 password가 주석처리되어 쿼리가 admin & true 로 들어가게된다.
```
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("public/login.html", error_message="Username or password is empty!"), 400
        try:
            user = query_db(
                f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'",
                one=True,
            )

            if user is None:
                return render_template("public/login.html", error_message="Invalid username or password"), 400

            set_2fa_code(4)

            return redirect("/auth/verify-2fa")
        finally:
            close_db()
    return render_template("public/login.html")
```

 - 두번째로 볼 함수는 ```login.py``` 내에 있는 ```set_2fa_code(4)```를 살펴보면 cache 데이터 설정값으로 2fa-code 라는 변수를 가지고 랜덤한 4글자 0~9자리로 세팅한다.
 - 이후 해당 캐시데이터는 5분간 유지된다.
 - 해당 데이터로 2단계 인증값을 입력받을때 검증을 한다.
```
def set_2fa_code(d):
    uwsgi.cache_del("2fa-code")
    uwsgi.cache_set(
        "2fa-code", "".join(random.choices(string.digits, k=d)), 300 # valid for 5 min
    ) 
``` 

  - ```verify2fa.py``` 코드를 확인해보았을때 login과 똑같이 method를 post로 request했을때 페이지가 리소스되는것을 확인할수있고 body의 내용으로 2fa-code를 받는다.
  - 위 내용의 캐시데이터 와 입력데이터를 검증하여 맞을경우 ```session.authenticated = True``` 로 설정하고 /dashboard로 리다이렉트 되는것을 확인할수있다.
```
@verify2fa_bp.route("/verify-2fa", methods=["GET", "POST"])
@requires_2fa
def verify():
    if request.method == "POST":

        code = request.form.get("2fa-code")
        
        if not code:
            return render_template("private/verify2fa.html", error_message="2FA code is empty!"), 400

        stored_code = uwsgi.cache_get("2fa-code").decode("utf-8")

        if code == stored_code:
            uwsgi.cache_del("2fa-code")
            session["authenticated"] = True
            return redirect("/dashboard")

        else:
            return render_template("private/verify2fa.html", error_message="Invalid 2FA Code!"), 400
    return render_template("private/verify2fa.html")
```
