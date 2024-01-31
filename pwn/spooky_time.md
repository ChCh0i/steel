# Spooky_time
![js](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)

![image](https://github.com/ChCh0i/steel/assets/108965611/89a6a33e-4acb-41c0-b143-972cd2a3ff23)

## 개요
 - aslr이 활성화되어있는 format string bug 문제입니다.
 - 큰 어려움은 없지만 libc base offset 과 binary base offset 을 구하는데 debug과정이 필요합니다.

## Tree
```
whoami@choijunwon:~/Spooky Time$ tree
.
└── challenge
    ├── flag.txt
    ├── flag.txt:Zone.Identifier
    ├── glibc
    │   ├── ld-linux-x86-64.so.2
    │   ├── ld-linux-x86-64.so.2:Zone.Identifier
    │   ├── libc.so.6
    │   └── libc.so.6:Zone.Identifier
    ├── spooky_time
    └── spooky_time:Zone.Identifier
```
## Protect
![image](https://github.com/ChCh0i/steel/assets/108965611/ea487dbd-3df5-4592-8ce5-145b68e43a46)
![image](https://github.com/ChCh0i/steel/assets/108965611/6c6fb721-4357-4147-90c3-4063007258f5)
![image](https://github.com/ChCh0i/steel/assets/108965611/1b688c32-9b86-48de-a80f-3fe2b83e4cd7)

```arch``` : ```64bit-little```

```aslr``` : ```enable```

```Relro``` : ```disable```

```stack``` : ```enable```

```nx``` : ```enable```

```pie``` : ```enable```

 - aslr 이 활성화되있어 바이너리 실행 주소가 유동적으로 실행될때마다 랜덤으로 매핑되며
 - Relro가 비활성화되있어 global offset table overwrite가 가능하다.

## Source

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char format[12]; // [rsp+4h] [rbp-14Ch] BYREF
  char v6[312]; // [rsp+10h] [rbp-140h] BYREF
  unsigned __int64 v7; // [rsp+148h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  setup(argc, argv, envp);
  banner();
  puts("It's your chance to scare those little kids, say something scary!\n");
  __isoc99_scanf("%11s", format);
  puts("\nSeriously?? I bet you can do better than ");
  printf(format);
  puts("\nAnyway, here comes another bunch of kids, let's try one more time..");
  puts("\n");
  __isoc99_scanf("%299s", v6);
  puts("\nOk, you are not good with that, do you think that was scary??\n");
  printf(v6);
  puts("Better luck next time!\n");
  return v7 - __readfsqword(0x28u);
}
```

 - 코드를 살펴보면 다음과 같다.
```
__isoc99_scanf("%11s", format);
  puts("\nSeriously?? I bet you can do better than ");
  printf(format);
```
 - 처음 입력을때 11s 만큼 받고 format이라는 변수에 저장후 format형식이 지정되지않은 printf를 사용해 출력한다.
 - 이때 format타입을 지정하지않아 format string bug가 발생한다.

 - 두 번째 부분이다.
```
__isoc99_scanf("%299s", v6);
  puts("\nOk, you are not good with that, do you think that was scary??\n");
  printf(v6);
```
 - 위와 마찬가지지만 입력받을때 좀 더 크게 입력을받으며 마찬가지로 fsb가 발생한다.
 - 큰 입력값으로 인하여 좀더 광범위한 포인트 탐색 가능

## 시나리오 구성
 - 시나리오 구성은 다음과 같습니다.
 - 첫번째 입력값에 %p,%x,%xl.. 등을 이용하여 libc와 binary 의 실행주소를 찾습니다.
 - 이후 aslr을 off한 상태에서 offset을 구한후 다시 aslr을 활성화하여 실제로 그 주소가 offset을 찾을만한 인자인지 검증합니다.
 - 다음으로 puts_got 주소를 bin_base 에 더하고 libc 파일에서 찾은 onegadget을 libc_base + 해줍니다.
 - 두번째 입력값에 pwntools fmtstring payload 를 활용하여 8바이트만큼 puts_got 주소에 onegadget 주소를 덮어 씌웁니다.
 - exploit

## Debug
 - 일단 aslr을 off합니다.    ![image](https://github.com/ChCh0i/steel/assets/108965611/49efbb2f-c193-4ec4-8039-e80f6fa4dccc)
 - 이후 break point를 main에 설정하고 start & vmmap을 확인해보면 aslr이 off상태일때의 binary & libc 의 start point와 end point를 확인할수 있습니다.

![image](https://github.com/ChCh0i/steel/assets/108965611/394fcfba-5416-4dfa-9314-919b3a9e7d9c)

 - aslr이 disable일때의 주소는 알고있지만 enable 상태일때의 주소는 유동적으로 변한다고 말했습니다.
 - 그렇다면 저흰 fsb를 이용하여 libc 와 binary 주소를 참조하고있는 주소를 활용하여 offset을 구한후 exploit에 활용할수 있습니다.
 - gdb) continue

![image](https://github.com/ChCh0i/steel/assets/108965611/8b23f6ad-fdd7-4e94-ab1b-52e72cc38113)

