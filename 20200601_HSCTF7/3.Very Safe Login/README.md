# Very Safe Login

```
web new beginner

Bet you can't log in.
https://very-safe-login.web.hsctf.com/very-safe-login
Author: Madeleine
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83932501-e7fdc380-a7dd-11ea-8d25-cf5db546d8f0.png)

問題のページに移動するとloginページが表示されました。

ページのソースを見てみると`script`タグにloginの処理が見える状態で載っていました。

```javascript
var login = document.login;

        function submit() {
            const username = login.username.value;
            const password = login.password.value;
            
            if(username === "jiminy_cricket" && password === "mushu500") {
                showFlag();
                return false;
            }
            return false;
        }
```

`username`と`password`がそのままあるのでこれを入力してみます。


![2](https://user-images.githubusercontent.com/47602064/83932570-52aeff00-a7de-11ea-8bfc-d9d30786cea8.png)

するとloginが出来て、flagが表示されました。

<br><br>

## FLAG: flag{cl13nt_51de_5uck5_135313531}
