# emdee_five_for_life

## 개요
 - hackthebox md5 time limit 문제
 - Source Code 미제공

## Preview
<img width="1468" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/abd1be55-732c-4aa2-aa37-bdeb0cb50f8b">

## 시나리오
 - text form에 입력시 too slow 출력후 위 제공되는 hash화할 text random으로 변경
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/92b90b3e-bd4f-40a8-a01e-272cbfb2ae02">
 - 아래와같이 request와 response를 확인해볼경우 cookie값을 request에 안넣고 요청시 respone으로 session값을 랜덤으로 받아오는것을 확인가능
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/50e70bba-2bb8-4f01-8e5d-c510b2644b81">
 - payload 구성 beautifulsoup를 활용하여 처음 페이지를 소스할때 response를 받아와 출력되는 text와 sessionid 를 가져오고 post요청으로 body/hash 라는 변수에 hash화된 text입력
 - 이후 headers에 sessionid값을 넣어주고 post요청을 보낼시 flag를 출력하게된다.

## payload
```
import requests
import hashlib
from bs4 import BeautifulSoup


url = 'http://188.166.175.58:32707/'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
print(res.text)

pro = soup.find('h3').text
print(pro)

md5_hash = hashlib.md5(pro.encode()).hexdigest()
print(md5_hash)

session = res.headers['Set-Cookie']

data = {
    'hash': md5_hash
}

header = {'Cookie': session}

response = requests.post(url, data=data, headers=header)

if response.status_code == 200:
    print('ok')
    print('내용',response.text)

else:
    print('요청실패')
    print('error', response.text)
```

 - response
```
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>rzhW6IgdwboDZbVJ3xTd</h3><p align='center'>HTB{N1c3_ScrIpt1nG_B0i!}</p><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```
