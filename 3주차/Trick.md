# Trick
- 포맷 바이트를 지키지않아 canary를 우회하여 원하는 주소에 값을 넣을수있음

## Source Code Analysis
![image](https://github.com/user-attachments/assets/ef07d75d-ba77-4194-a4d7-e7e1c8bbfe01)
- sub_8AD()라는 함수에 쉘을 실행시키는 명령어 존재

![image](https://github.com/user-attachments/assets/4406fdd0-d3ba-4d65-8ae1-1ddde514b4d3)
- 반복문에 사용되는 매개값은 공격자가 컨트롤 가능하다.
- s라는 변수는 ```_DWORD```로 선언되어 있는 반면 scanf할때 포맷타입이 ```%hd```이다.
- ```DWORD```는 4byte 인데 ```%hd```는 2byte이므로 사용자가 값을 넣을때마다 2바이트만 입력받고 나머지는 넘어가게된다.

## 동적 분석
![image](https://github.com/user-attachments/assets/370b6245-a45f-4205-8e99-339485babcc0)
- memset으로 64바이트만큼 ```0x03```으로 덮어줘 공격자가 디버깅할때 좀더 편하게 하려는 의도가 있는것닽다.
- hi : 5 (반복문 매개)
- gogo : 1111을 두번주어 확인

![image](https://github.com/user-attachments/assets/b4c2faaf-9040-4118-a90f-568790384587)
- gogo에 넣었던 값 1111이 16진수로 변환되어 0x457로 들어간것을 확인이 가능하다.

![image](https://github.com/user-attachments/assets/6fceb6c0-4aa5-46d1-af99-8569d278f7a5)
- 이후 0x03이 64byte만큼 세팅 되어있는것을 확인할수있고, 배열의 마지막은 null인것을 알수있다.
- 이후 canary가 존재하고 아키텍쳐 64bit 기준 rbp-8 포인트에 canary가 위치하는것을 우리는 알고있다.
- 그러면 0x7ff.....e270이라는 값이 rbp인것을 알수있다.
- rbp+8 포인트에는 ret주소가 존재한다.
- 하지만 실행할때마다 변하는 canary 값을 우회하는건 현실적으로 무리가 있다.

![image](https://github.com/user-attachments/assets/0aa30c16-f45f-4634-a9a9-9bbdcfa68e6c)
- 우연히 찾게된 블로그가 힌트가 되었다.
- scanf로 입력받을때 포맷타입이 ```float```형 이면 ```.```을 이용하여 입력되는 메모리 주소를 건너뛸수 있다는 내용이었다.
- 여기서 힌트를 얻어 정수형에서 입력받는 모든 부호들을 다 넣어보았다.
- 그러다 찾은게 ```-``` 였다.

![image](https://github.com/user-attachments/assets/17d994b1-63ab-4320-aa1d-f456767f7663)
- ```hi:5```
- ```gogo:-```
- ```gogo:1111```
- 위 와 같이 입력값을 주고 분석한다.
- ```-```를 입력하였을때 원래 입력받는 포인트 주소를 ```eof```없이 건너뛰는것을 확인할수 있다.
- 이러한 트릭으로 canary를 bypass하고 ret address에 값을 덮어씌울수있다.

![image](https://github.com/user-attachments/assets/0c8ff485-a936-4730-91e9-7b7daa04bb4e)
- 마지막으로 구해야할것은 함수 주소이다.
- strip으로 실행주소가 계속 바뀌기 때문이다.
- 먼저 해당 함수의 주소는 시작주소+8ad이다.
- binary의 시작주소는 0x555555400000 이다.
- bin + 0x8ad를 해주면 0x5555554008ad 이것이 쉘 함수 주소이다.

![image](https://github.com/user-attachments/assets/6fa09d93-ce69-4fd0-a124-85a0ef60ebc3)
- 해당 주소를 확인해보면 다음과같이 stack frame pointer를 생성하는것을 볼수있다.

## PoC
- exploit 코드는 따로 필요가없다.
- gogo 에서부터 사용자의 입력값을 하나로 4byte만큼의 거리를 이동하기때문에 ```-```를 이용하여 canary와 rbp주소를 넘긴후 ret주소의 마지막 2byte를 0x8ad로 덮으면 된다.
- ret까지의 거리는 88byte이고 입력값 하나로 움직이는 거리는 4byte라고 하였으니 ```88/4=22```
- 즉 입력값을 ```-```로 22번 입력하고 ```0x8ad```를 int형으로 바꾼 2221을 입력하면 exploit 이 된다.

- ![image](https://github.com/user-attachments/assets/b023ce32-f8ad-4fa8-b1bb-975be2c08e7a)



