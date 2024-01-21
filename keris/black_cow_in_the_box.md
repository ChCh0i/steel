# black cow in the box
![js](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)

# 개요
 - 스틸리언교육에서 풀어본 keris 제9회 blackbox 문제입니다.
 - lfi 인건 알고있었지만 조금 특이하게 풀이를 하는경향이 있어 문제해결에 어려움이 있었던것같습니다.
 - Source코드는 제공되지 않았습니다.

# Preview
![image](https://github.com/ChCh0i/steel/assets/108965611/6a37b99d-c2f3-4f07-be76-b4cdd7841398)
![image](https://github.com/ChCh0i/steel/assets/108965611/2932dd52-7843-4fc6-9faf-62566610735c)

# 시나리오
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
