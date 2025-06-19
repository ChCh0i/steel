# Prying Eyes
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)

![image](https://github.com/user-attachments/assets/b4435797-0e6a-4df7-89f8-5f0c4f65381a)

## Source Code Analysis
```
FROM node:18-bullseye-slim

# Install packages and build ImageMagick
RUN apt update && \
    apt install -y wget pkg-config build-essential unzip \
                   libpng-dev libjpeg-dev libavif-dev libheif-dev \
                   supervisor && \
    wget https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.0-33.zip -O /tmp/ImageMagick-7.1.0-33.zip && \
    cd /tmp && \
    unzip ImageMagick-7.1.0-33.zip && \
    cd ImageMagick-7.1.0-33 && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    ldconfig /usr/local/lib && \
    rm -rf /var/lib/apt/lists/* /tmp/ImageMagick-7.1.0-33*

# Setup supervisor configuration
COPY ./config/supervisord.conf /etc/supervisor/supervisord.conf

# Use non-root user for Node.js application
USER node

# Create application directory
RUN mkdir /home/node/app

# Set working directory
WORKDIR /home/node/app

# Copy challenge files
COPY --chown=node:node ./challenge/ .

# Install Node.js dependencies
RUN npm install

# Expose application port
EXPOSE 8000

# Switch back to root to run supervisor
USER root

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
```
- ```Dockerfile```의 내용은 위와 같다.
- ```ImageMagick``` 오픈소스 소프트웨어를 사용하는것을 확인

```
const express = require("express");
const nunjucks = require("nunjucks");
const cookieSession = require("cookie-session");
const { randomBytes } = require("node:crypto");

const Database = require("./database");
const { render } = require("./utils");
const FlashMiddleware = require("./middleware/FlashMiddleware");
const AuthRoutes = require("./routes/auth");
const ForumRoutes = require("./routes/forum");

const app = express();
const db = new Database("./database.db");

// Set up the templating engine
const env = nunjucks.configure("views", {
  autoescape: true,
  express: app,
});

env.addFilter("date", (timestamp) => {
  const date = new Date(timestamp);
  return `${date.toLocaleDateString()} at ${date.toLocaleTimeString()}`;
});

// Session configuration
app.use(
  cookieSession({
    name: "session",
    secret: randomBytes(69),
    maxAge: 24 * 60 * 60 * 1000, // 1 day
  })
);

// Static file serving
app.use("/static", express.static("public"));
app.use(
  "/uploads",
  express.static("uploads", {
    setHeaders: (res) => {
      res.setHeader("Content-Type", "image/avif");
    },
  })
);

// Middleware
app.use(express.urlencoded({ extended: false }));
app.use(FlashMiddleware);

// Routes
app.get("/", (req, res) => {
  res.redirect("/forum");
});

app.use("/auth", AuthRoutes(db));
app.use("/forum", ForumRoutes(db));

// 404 handler
app.use("*", (req, res) => {
  res.status(404);
  render(req, res, "error.html", {
    errorMessage: "We can't seem to find that page!",
    errorCode: "404",
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500);
  render(req, res, "error.html", {
    errorMessage: "Something went wrong!",
    errorCode: "500",
  });
});

// Start server
(async () => {
  await db.connect();
  await db.migrate();

  app.listen(1337, "0.0.0.0", () => {
    console.log("Listening on port 1337");
  });
})();
```
- 해당 코드는 라우팅되는 메인 ```app.js``` 파일 이다.
- ```/```경로로 접근할 경우 ```/forum```으로 리다이렉트 시키고, ```/auth```에 접근할 경우 ```AuthRoutes(db)```를 호출 한다.

```
const express = require("express");
const { RedirectIfAuthed } = require("../middleware/AuthMiddleware");
const ValidationMiddleware = require("../middleware/ValidationMiddleware");
const { render } = require("../utils");

const router = express.Router();
let db;

// GET /auth/login
router.get("/login", RedirectIfAuthed, (req, res) => {
  render(req, res, "login.html");
});

// POST /auth/login
router.post(
  "/login",
  RedirectIfAuthed,
  ValidationMiddleware("login", "/auth/login"),
  async (req, res) => {
    const user = await db.loginUser(req.body.username, req.body.password);

    if (!user) {
      req.flashError("Please specify a valid username and password.");
      return res.redirect("/auth/login");
    }

    req.session = {
      flashes: {
        success: [],
        error: [],
      },
      userId: user.id,
    };

    req.flashSuccess("You are now logged in.");
    return res.redirect("/forum");
  }
);

// GET /auth/register
router.get("/register", RedirectIfAuthed, (req, res) => {
  render(req, res, "register.html");
});

// POST /auth/register
router.post(
  "/register",
  RedirectIfAuthed,
  ValidationMiddleware("register", "/auth/register"),
  async (req, res) => {
    const user = await db.getUserByUsername(req.body.username);

    if (user) {
      req.flashError("That username already exists.");
      return res.redirect("/auth/register");
    }

    await db.registerUser(req.body.username, req.body.password);

    req.flashSuccess("You are now registered.");
    return res.redirect("/auth/login");
  }
);

// GET /auth/logout
router.get("/logout", (req, res) => {
  req.session.userId = null;
  req.flashSuccess("You have been logged out.");
  return res.redirect("/forum");
});

module.exports = (database) => {
  db = database;
  return router;
};
```
- ```./routes/auth.js```파일 이다.
- ```<URL>/auth/login```과 같이 접속할 경우 미들웨어 ```RedirectIfAuthed```로 이동하게 된다.

```
router.get("/post/:parentId", AuthRequired, async (req, res) => {
  const { parentId } = req.params;
  const parent = await db.getPost(parentId);

  // 존재하지 않거나 부모 글이 아닌 경우
  if (!parent || parent.parentId) {
    req.flashError("That post doesn't seem to exist.");
    return res.redirect("/forum");
  }

  const thread = await db.getThread(parentId);
  render(req, res, "post.html", { parent, posts: thread });
});
```
- ```./routes/forum.js```의 내용이다.

```
// 인증 필요 미들웨어
const AuthRequired = (req, res, next) => {
  if (!req.session.userId) {
    req.flashError("You must be logged in to view this.");
    return res.redirect("/auth/login");
  }
  next();
};

// GET /forum/new
router.get("/new", AuthRequired, async (req, res) => {
  render(req, res, "new.html");
});
```
- ```/forum/new```의 라우터와 미들웨어 관련 코드이다.
- 세션에 ```userId```가 존재하지 않을 경우 리다이렉트 시키는것을 볼 수 있다.

```
{
  "type": "object",
  "properties": {
    "username": {
      "type": "string",
      "minLength": 4,
      "maxLength": 32
    },
    "password": {
      "type": "string",
      "minLength": 6,
      "maxLength": 32
    }
  },
  "required": ["username", "password"],
  "errorMessage": {
    "properties": {
      "username": "Username should be between 4 and 32 characters.",
      "password": "Password should be between 6 and 32 characters."
    }
  }
}
```
- ```/auth/login```에 POST 요청을 할경우 위와 같이 선언된 json 스키마 룰을 따라야한다.

```
router.get("/new", AuthRequired, async function (req, res) {
    render(req, res, "new.html");
});
```
- 로그인후 글 작성시 ```new.html```을 렌더링 한다.

```
<form method="post" action="/forum/post" enctype="multipart/form-data">
    ...
    <input
        class="form-control"
        id="image-upload"
        name="image"
        type="file"
        accept=".png, .jpg, .jpeg"
    />
    ...
</form>
```
- 렌더링 된 내용은 위와 같다.
- 사용자가 이미지 파일을 업로드 할 수 있는 필드를 생성하고, ```png,jpg,jpeg``` 확장자를 가진 파일만 업로드가 가능하다.
- 이후 ```/forum/post```로 요청을 보낸다.

```
proceed() {
    return new Promise((resolve, reject) => {
        const source = this.options.get('srcData');

        if (source && (source instanceof Buffer)) {
            try {
                const origin = this.createOccurrence(this.options.get('srcFormat'));
                const result = this.createOccurrence(this.options.get('format'));
                const cmd = this.composeCommand(origin, result);
                const cp = spawn('convert', cmd);
                const store = [];

                cp.stdout.on('data', (data) => store.push(Buffer.from(data)));
                cp.stdout.on('end', () => resolve(Buffer.concat(store)));
                cp.stderr.on('data', (data) => reject(data.toString()));

                cp.stdin.end(source);
            } catch (e) {
                reject(e);
            }
        } else {
            reject(new Error('imagemagick-convert: the field `srcData` is required and should have `Buffer` type'));
        }
    });
}
```
- 다음으로는 ```convert()```의 소스코드 중 일부를 확인
- ```cp = spawn('convert',cmd)``` ```convert```는 실행하려는 프로그램 명, ```cmd```는 해당 프로그램 설정 옵션 이다.
- 

```
[ 
   "-density 600",
   "-background none",
   "-gravity Center",
   "-quality 75",
   "-rotate 0",
   "-",
   "AVIF:-",
]
```
- ```cmd```의 형태는 위와 같다.

```
{
  rotate: 0,
  flip: false,
}
```
- 공격코드를 넣지않고 일반적인 사진을 올렸을때 ```...convertParams```의 값은 위와 같다.
- ```-route 0```이 해당 객체의 값을 그대로 사용한 것이라는 것을 알 수 있다. 따라서 사용자의 입력으로 ```convert```프로그램의 인자를 조작하는 것이 가능하다.
- 인자만 조작할 수 있는 이유는 ```child_process```모듈의 ```spawn()```이 파이썬으로 치면 ```Popen(shell=True)```이기 때문

## PoC
- ImageMagick Arbitrary File Disclosure (CVE-2022-44268)
- 해당 취약점의 poc코드를 사용하여 익스플로잇 진행
- ```Dockerfile```에서 ```flag.txt```의 경로가 ```/home/node/app/flag.txt``` 라는것을 알 수 있다.

```
 ./poc.py generate -o poc.png -r /home/node/app/flag.txt
```
- ```flag.txt```를 읽는 poc.png 생성
![image](https://github.com/user-attachments/assets/50b3ed17-d5f7-4584-ab70-5ace8ef66382)
```red -write ./uploads/output.png```
- 사용자가 접근할수 있는 경로에 읽은 플래그를 저장한다.

![image](https://github.com/user-attachments/assets/16c55e4b-21a9-4b32-a4c3-7d441f2f5862)
- 플래그가 성공적으로 저장된것을 알 수 있다.

![image](https://github.com/user-attachments/assets/e20c2784-a2c5-4d23-93e6-2c3e8929c32c)
- flag획득

