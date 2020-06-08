# Buttons 

## Solve
```
There is a website running at http://2018shell.picoctf.com:7949 (link). 
Try to see if you can push their buttons.
```

## Hint
```
What's different about the two buttons?
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83597087-586bd100-a5a1-11ea-9e4e-4c7b47c4afa8.png)

まず問題にあるリンクに移動するとボタン1がある。

ボタンを押すと次のページに移動する。

```txt
You did it! Try the next button: Button2
```

すると次はボタン2があるのでそれを押すと変な動画のページに移動しました。

```txt
Button2: ACCESS DENIED
FORM DISABLED. THIS INCIDENT HAS BEEN LOGGED AND REPORTED TO /dev/null
```

次に以下のページのソースコードを見てみます。

`http://2018shell.picoctf.com:7949/button1.php`

```html
<!doctype html>
<html>
<head>
    <title>Buttons!</title>
    <link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</head>
<body>
<div>
    You did it! Try the next button: <a href="button2.php">Button2</a>
</div>
</body>
</html>
```

すると`Buttons!`のアクセス先が`button2.php`になっていないことがわかります。

実際は以下のリンクに移動して動画のサイトが表示されます。

`http://2018shell.picoctf.com:7949/boo.html`

なので`button2.php`にアクセスしてみます。

一つ前のページで`button1.php`にアクセスする時はPOSTで送られていたのでこれも同じように送ります。

`http://2018shell.picoctf.com:7949/`

```html
<form action="button1.php" method="POST">
 <input type="submit" value="PUSH ME! I am your only hope!"/>
</form>
```

<br>

```http
$ http POST http://2018shell.picoctf.com:7949/button2.php
HTTP/1.1 200 OK
Content-type: text/html; charset=UTF-8

Well done, your flag is: picoCTF{button_button_whose_got_the_button_3e5652dd}
```

するとアクセスできてflagが表示されました。

<br><br>

## FLAG: picoCTF{button_button_whose_got_the_button_3e5652dd}
