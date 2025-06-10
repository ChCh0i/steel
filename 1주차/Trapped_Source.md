# Trapped Source
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

![image](https://github.com/user-attachments/assets/4ba03adf-76fc-4593-ba5b-a8d47ec5207d)
- 처음 접속시 번호4개를 입력할 수 있는 창이 나온다.
- ```Enter```를 누르면 INVALID! 문자열 출력

## Source Code Analysis
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title></title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
  </head>
  <body>
    <script>
      window.CONFIG = window.CONFIG || {
        buildNumber: "v20190816",
        debug: false,
        modelName: "Valencia",
        correctPin: "4139",
      }
    </script>
    <div class="lockbox">
      <div class="lockStatus">LOCKED</div>
      <div class="lockMid">
        <span id="btn9" class="button" onclick="unlock(9)">9</span>
        <span id="btn8" class="button" onclick="unlock(8)">8</span>
        <span id="btn7" class="button" onclick="unlock(7)">7</span>
        <span id="btn6" class="button" onclick="unlock(6)">6</span>
        <span id="btn5" class="button" onclick="unlock(5)">5</span>
        <span id="btn4" class="button" onclick="unlock(4)">4</span>
        <span id="btn3" class="button" onclick="unlock(3)">3</span>
        <span id="btn2" class="button" onclick="unlock(2)">2</span>
        <span id="btn1" class="button" onclick="unlock(1)">1</span>
        <div class="clear" onclick="reset()">Clear</div>
        <div class="scoreCount" onclick="checkPin()">Enter</div>
      </div>
    </div>
    <!-- partial -->
    <script src='/static/js/jquery.js'></script>
    <script src="/static/js/script.js"></script>
  </body>
</html>
```
- 정적으로 페이징되는 소스를 보면 ```windows.CONFIG```값을 설정하는것을 확인가능
- 또한 ```<script src="/static/js/script.js"></script>``` 로 특정 스크립트 경로 확인가능

```
currentPin = []

const checkPin = () => {
  pin = currentPin.join('')
  
  if (CONFIG.correctPin == pin) {
    fetch('/flag', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'pin': CONFIG.correctPin
      })
    })
      .then((data) => data.json())
      .then((res) => {
        $('.lockStatus').css('font-size', '8px')
        $('.lockStatus').text(res.message)
      })
    return
  }
  
  $('.lockStatus').text('INVALID!')
  setTimeout(() => {
    reset()
  }, 3000)
}

const unlock = (pin) => {
  currentPin.push(pin)
  if (currentPin.length > 4) return
  $('.lockStatus').text(currentPin.join(' '))
}

const reset = () => {
  currentPin.length = 0
  $('.lockStatus').css('font-size', 'x-large')
  $('.lockStatus').text('LOCKED')
}
```
- 해당 소스 확인시 앞서 클라이언트에서 설정했던 ```CONFIG.correctPin```과 사용자의 입력값을 비교 하는것을 확인

## Flag 획득
![image](https://github.com/user-attachments/assets/553131e1-a4e8-4bf7-aa68-4c098eef68f0)
- ```CONFIG.correctPin```값인 4139를 입력하면 플래그 획득
```HTB{vi3w_cli13nt_s0urc3_S3cr3ts!```
