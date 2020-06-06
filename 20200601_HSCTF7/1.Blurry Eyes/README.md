# Blurry Eyes
```
web beginner

I can't see :(
https://blurry-eyes.web.hsctf.com
Author: meow
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83932185-db786b80-a7db-11ea-8de9-7e18a328e9d3.png)

問題に移動するとCTFについての文章が書いてあります。

下の方にある文章を見ます。

```txt
Anyways, the flag that you need for this cha
```

この文章の右側がぼやけています。

なのでページのソースを見てみます。

```html
 <h4>Anyways, the flag that you need for this cha<span class="blur">llenge is: <span
          class="poefKuKjNPojzLDf"></span></span></h4>
```

htmlのspanタグはタグで挟んだ文字を変更させます。

なのでこの部分を消してみます。

![3](https://user-images.githubusercontent.com/47602064/83932354-d8ca4600-a7dc-11ea-8b95-13bd018cb1d5.png)

するとぼやけが取れてflagが表示されました。


<br><br>

## FLAG: flag{glasses_are_useful}
