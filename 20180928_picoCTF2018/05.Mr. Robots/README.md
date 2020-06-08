# Mr. Robots

## Solve
```
Do you see the same things I see? 
The glimpses of the flag hidden away? 
http://2018shell.picoctf.com:60945 (link)
```

## Hint
```
What part of the website could tell you where the creator doesn't want you to look?
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/67436327-13ee7f00-f629-11e9-9ca8-ee82269cb0c4.png)

問題のページに移動すると以上のように表示されました。

今回はヒントに`/robots.txt`とあるのでここでアクセスしてみます。

`http://2018shell.picoctf.com:60945/robots.txt`

![2](https://user-images.githubusercontent.com/47602064/67436365-2963a900-f629-11e9-843c-beecd2cb1b04.png)

するとそこでリンクが載って表示されました。

なのでそこにアクセスしてみます。

`http://2018shell.picoctf.com:60945/65c0c.html`

![3](https://user-images.githubusercontent.com/47602064/67436394-3c767900-f629-11e9-83bf-aaf42dba4f1e.png)

するとそのページにflagが表示されました。

<br>

Pythonでflagを表示させるには以下のようなプログラムで綺麗に得ることが出来ます。

```python
#!/usr/bin/python

import requests
import re

r = requests.get('http://2018shell1.picoctf.com:10157/robots.txt')
source = r.text
page = re.findall(r'Disallow: /(.+)', source)[0]
print 'Found: ' + page

r = requests.get('http://2018shell1.picoctf.com:10157/{}'.format(page))
source = r.text
print re.findall(r'(picoCTF\{.+\})', source)[0]
```

<br><br>

## FLAG: picoCTF{th3_w0rld_1s_4_danger0us_pl4c3_3lli0t_65c0c}
