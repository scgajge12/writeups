# Client Side is Still Bad

## Solve
```
I forgot my password again, but this time there doesn't seem to be a reset, can you help me? 
http://2018shell.picoctf.com:8930 (link)
```

## Hint
```
Client Side really is a bad way to do it.
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/67434296-dd166a00-f624-11e9-93db-2f90786ad7e9.png)

問題のページに移動すろとloginページが表示されます。

試しにHTMLを見てみるとflagらしいのがありました。

![2](https://user-images.githubusercontent.com/47602064/67434344-fae3cf00-f624-11e9-936a-18b7d26a3bc2.png)

```javascript
if (checkpass.substring(split*7, split*8) == '}') {
      if (checkpass.substring(split*6, split*7) == 'ebbd') {
        if (checkpass.substring(split*5, split*6) == 'd_d0') {
         if (checkpass.substring(split*4, split*5) == 's_ba') {
          if (checkpass.substring(split*3, split*4) == 'nt_i') {
            if (checkpass.substring(split*2, split*3) == 'clie') {
              if (checkpass.substring(split, split*2) == 'CTF{') {
                if (checkpass.substring(0,split) == 'pico') {
                  alert("You got the flag!")
                  }
                }
              }
      
            }
          }
        }
      }
    }
```

if文の条件が丸見え状態でflagを入力すろとloginができるようです。

`picoCTF{client_is_bad_d0ebbd}`

なのでflagらしいのをloginページの入力欄に入力してみます。

![3](https://user-images.githubusercontent.com/47602064/67434386-14851680-f625-11e9-8db3-3a1a29fc2aab.png)

するとこれでflagが正しいことがわかりました。

<br><br>

## FLAG: picoCTF{client_is_bad_d0ebbd}
