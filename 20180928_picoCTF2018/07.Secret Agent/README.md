# Secret Agent

## Solve
```
Here's a little website that hasn't fully been finished. 
But I heard google gets all your info anyway. 
http://2018shell.picoctf.com:11421 (link)
```

## Hint
```
How can your browser pretend to be something else?
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83594471-40dd1a00-a59a-11ea-861d-8ac761f02c18.png)

問題のページに移動するとflagのボタンが表示されます。

押してみると以下が表示されました。

![2](https://user-images.githubusercontent.com/47602064/83594554-7c77e400-a59a-11ea-933a-071a50d366a9.png)

```txt
You're not google! Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
```

あなたはgoogleでないと表示されました。

なのでUA(User Agent)を変更して送ってみます。

<br>

今回はgoogleでアクセスすればいいそうなので`Googlebot`で設定させます。

UAをPythonで送る場合は`headers`で送ればできます。

```http
$ http GET http://2018shell1.picoctf.com:53383/flag "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

HTTP/1.1 200 OK

<!DOCTYPE html>

         <!-- <strong>Title</strong> --> Googlebot!
           </div>
     
        <div class="jumbotron">
            <p class="lead"></p>
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{s3cr3t_ag3nt_m4n_134ecd62}</code></p>
            <!-- <p><a class="btn btn-lg btn-success" href="admin" role="button">Click here for the flag!</a> -->
            <!-- </p> -->
        </div>

```

これで`google`でアクセスできてflagが表示されました。

<br>

デバッグや`Burp`でrequestを編集して送信すると以下のように表示されます。

![2](https://user-images.githubusercontent.com/47602064/68101259-10ec6c00-ff10-11e9-8476-80f39108db0a.png)

<br>

Pythonで実行すると以下のプログラムで綺麗にflagを得ることが出来ます。

```python
#!/usr/bin/python

import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

r = requests.get('http://2018shell1.picoctf.com:53383/flag', headers=headers)
source = r.text

print re.findall(r'(picoCTF\{.+\})', source)[0]
```

<br><br>

## FLAG: picoCTF{s3cr3t_ag3nt_m4n_ed3fe08d}
