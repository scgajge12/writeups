# Inspect Me

## Solve
```
Inpect this code! http://2018shell.picoctf.com:28831
```

## Hint
```
How do you inspect a website's code on a browser?
Check all the website code.
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83478220-3eae8900-a4d0-11ea-9410-586ff2d4c8a4.png)

問題に移動すると`Website`が表示されます。

`About`の方を見てみると以下のようにあります。

![2](https://user-images.githubusercontent.com/47602064/83478342-92b96d80-a4d0-11ea-9384-90d2ca5b65a8.png)

すると`HTML`と`CSS`というのが書いてあるのでこのページのを見てみます。

<br>

HTMLを見てみると以下のように、flagの前半らしいのがありました。

![3](https://user-images.githubusercontent.com/47602064/67433826-cde2ec80-f623-11e9-9589-3f75f9d598a9.png)

```
flag: picoCTF{ur_4_real_1nspe
```

次にCSSを見てみるとflagの後半らしいのがありました。

![4](https://user-images.githubusercontent.com/47602064/67433868-e81cca80-f623-11e9-9fc8-caf245803bad.png)

```
flag: ct0r_g4dget_b4887011}
```

<br>

最後に前半と後半のを繋げるとflagが完成します。

<br><br>

## FLAG: picoCTF{ur_4_real_1nspect0r_g4dget_b4887011}
