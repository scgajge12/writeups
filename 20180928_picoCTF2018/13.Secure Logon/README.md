# Secure Logon

## Solve
```
Uh oh, the login page is more secure... 
I think. http://2018shell.picoctf.com:46026 (link). 
[Source](https://2018shell.picoctf.com/static/be78851c72116a5a1aea0e3ec52bdec9/server_noflag.py).
```

## Hint
```
There are versions of AES that really aren't secure.
```
<br>

## Solution

暗号系　CBCビットフリッピング攻撃に関するもの(CBCモードでのAESへの攻撃)

<br>

![1](https://user-images.githubusercontent.com/47602064/83819965-49eafa00-a706-11ea-8371-74604235f457.png)

問題のページに移動するとloginページが表示されました。

まずは適当に入力してみます。

すると以下のようになりました。

![2](https://user-images.githubusercontent.com/47602064/83825096-4b6eef00-a713-11ea-9767-ba54295a27d3.png)

flagは表示されないで`Cookie`の内容が表示されました。

ここに`admin:0`とあるのでadminでloginするのが関係していそうと考えられます。

試しに`amdin`と入力してみると以下のコメントが表示されて、出来ませんでした。

```txt
I'm sorry the admin password is super secure. You're not getting in that way.
```

なので`Cookie`の内容を直接書き換えなければいけないと考えられます。

<br>

次にソースコードを見てみます。

```python
from flask import Flask, render_template, request, url_for, redirect, make_response, flash
import json
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES

app = Flask(__name__)
app.secret_key = 'seed removed'
flag_value = 'flag removed'

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form['user'] == 'admin':
        message = "I'm sorry the admin password is super secure. You're not getting in that way."
        category = 'danger'
        flash(message, category)
        return render_template('index.html')
    resp = make_response(redirect("/flag"))

    cookie = {}
    cookie['password'] = request.form['password']
    cookie['username'] = request.form['user']
    cookie['admin'] = 0
    print(cookie)
    cookie_data = json.dumps(cookie, sort_keys=True)
    encrypted = AESCipher(app.secret_key).encrypt(cookie_data)
    print(encrypted)
    resp.set_cookie('cookie', encrypted)
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('cookie', '', expires=0)
    return resp

@app.route('/flag', methods=['GET'])
def flag():
  try:
      encrypted = request.cookies['cookie']
  except KeyError:
      flash("Error: Please log-in again.")
      return redirect(url_for('main'))
  data = AESCipher(app.secret_key).decrypt(encrypted)
  data = json.loads(data)

  try:
     check = data['admin']
  except KeyError:
     check = 0
  if check == 1:
      return render_template('flag.html', value=flag_value)
  flash("Success: You logged in! Not sure you'll be able to see the flag though.", "success")
  return render_template('not-flag.html', cookie=data)

class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')

if __name__ == "__main__":
    app.run()
```

<br>

このソースコードより以下を注目してみます。

```python
@app.route('/flag', methods=['GET'])
def flag():
  try:
      encrypted = request.cookies['cookie']
  except KeyError:
      flash("Error: Please log-in again.")
      return redirect(url_for('main'))
  data = AESCipher(app.secret_key).decrypt(encrypted)
  data = json.loads(data)

  try:
     check = data['admin']
  except KeyError:
     check = 0
  if check == 1:
      return render_template('flag.html', value=flag_value)

```

以上より、`/flag`へ`GET`で呼んだ時に`admin`が`1`ならflagが表示してくれそうです。

`cookie`の値はjson形式になって,`AESCipher`で暗号化されていることもわかります。

<br>

`json`は`password`,`username`,`admin`の順に値が入っています。

暗号は以下のように`AES`されています。

```python
class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')
```

全体のソースコードより、`username`などを入力されて、json形式で暗号化されて、`cookie`に入れられている流れになっています、

なのでjsonの`admin`の値が`1`になるようにして暗号化、`cookie`にセットして`/flag` に`GET`でアクセスすれば良さそうです。

<br>

実際にpythonで変換させてみます。

変換には`XOR`で変換させます。

```python
import base64

cookie = 'cBF0Sy9OsxO6AYVi6pyNdlLEq2W00/dsqkHeaInulF1oSwXhfUjO0zFu2nhoCy4NDEG1i+zTMBxvPIWdcBfNow=='

print(cookie)

decode = base64.b64decode(cookie)
flipped = bytes([decode[10] ^ ord('0') ^ ord('1')])

flipped_arr = []
for i in range(len(decode)):
    if i != 10:
        flipped_arr.append(bytes([decode[i]]))
    else:
        flipped_arr.append(flipped)

final = b''.join(flipped_arr)
print(base64.b64encode(final))
```

```
$ python3 s.py 
cBF0Sy9OsxO6AYVi6pyNdlLEq2W00/dsqkHeaInulF1oSwXhfUjO0zFu2nhoCy4NDEG1i+zTMBxvPIWdcBfNow==
b'cBF0Sy9OsxO6AYRi6pyNdlLEq2W00/dsqkHeaInulF1oSwXhfUjO0zFu2nhoCy4NDEG1i+zTMBxvPIWdcBfNow=='
```

これで新しいcookieが生成されました。

以下を`/flag`にアクセスするcookieにセットをすればよいです。

```txt
cBF0Sy9OsxO6AYRi6pyNdlLEq2W00/dsqkHeaInulF1oSwXhfUjO0zFu2nhoCy4NDEG1i+zTMBxvPIWdcBfNow==
```

```http
GET /flag HTTP/1.1
Host: 2018shell.picoctf.com:46026

Cookie: _ga=GA1.2.1326079095.1591175644; cookie=cBF0Sy9OsxO6AYRi6pyNdlLEq2W00/dsqkHeaInulF1oSwXhfUjO0zFu2nhoCy4NDEG1i+zTMBxvPIWdcBfNow==

```

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1418

<!DOCTYPE html>

        <div class="jumbotron">
            <p class="lead"></p>
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{fl1p_4ll_th3_bit3_a6396679}</code></p>
        </div>
```


![3](https://user-images.githubusercontent.com/47602064/83846684-f4364200-a745-11ea-91d9-a52d761586ba.png)

<br><br>

## FLAG: picoCTF{fl1p_4ll_th3_bit3_a6396679}
