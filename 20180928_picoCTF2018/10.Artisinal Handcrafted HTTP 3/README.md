# Artisinal Handcrafted HTTP 3

## Solve
```txt
We found a hidden flag server hiding behind a proxy, 
but the proxy has some... _interesting_ ideas of what qualifies someone to make HTTP requests. 
Looks like you'll have to do this one by hand. 
Try connecting via nc 2018shell.picoctf.com 57775, and use the proxy to send HTTP requests to `flag.local`. 
We've also recovered a username and a password for you to use on the login page: `realbusinessuser`/`potoooooooo`.
```

## Hint
```txt
_Be the browser._ When you navigate to a page, how does your browser send HTTP requests? 
How does this change when you submit a form?
```

<br>

## Solution

picoCTFより、今は解けない状態になっているとのこと。

<br><br>

本当なら以下のように返ってくれるそうです。

この課題では、手動でHTTPリクエストを作成する必要があるそうです。

```http
$ nc 2018shell1.picoctf.com 27936                                                                                           
Real Business Corp., Internal Proxy
Version 2.0.7                                                                                                               
To proceed, please solve the following captcha:                                                                             
 _____            ___
|____ |          /   |  ______
    / / __  __  / /| | |______|
    \ \ \ \/ / / /_| |  ______
.___/ /  >  <  \___  | |______|
\____/  /_/\_\     |_/

> 12                                           
Validation succeeded.  Commence HTTP. 
```


```http
GET /index.html HTTP/1.1
Connection: close
```

```http
HTTP/1.1 400 Bad Request  
```

----------------------------------------

<br>

```http
GET / HTTP/1.1
Connection: close
```

```http
HTTP/1.1 400 Missing Host header                                                                                             
Date:                                                                                        
Connection: keep-alive                                                                                                       
Transfer-Encoding: chunked 
```

---------------------------------------

<br>

```http
GET / HTTP/1.1
Host: flag.local
Connection: close
```

```http
HTTP/1.1 200 OK
x-powered-by: Express
content-type: text/html; charset=utf-8
content-length: 321
etag: W/"141-LuTf9ny9p1l454tuA3Un+gDFLWo"
date: 
connection: close


<html>
  <head>
    <link rel="stylesheet" type="text/css" href="main.css" />
  </head>
  <body>
    <header>
      <h1>Real Business Internal Flag Server</h1>
      <a href="/login">Login</a>
    </header>
    <main>
      <p>You need to log in before you can see today's flag.</p>
    </main>
  </body>  
</html>  
```

---------------------

<br>

```http
GET /login HTTP/1.1
Host: flag.local
Connection: close
```

```http
HTTP/1.1 200 OK
x-powered-by: Express
content-type: text/html; charset=utf-8
content-length: 498
etag: W/"1f2-UE5AGAqbLVQn1qrfKFRIqanxl9I"
date: 
connection: close


<html>
  <head>
    <link rel="stylesheet" type="text/css" href="main.css" />
  </head>
  <body>
    <header>
      <h1>Real Business Internal Flag Server</h1>
      <a href="/login">Login</a>
    </header>
    <main>
      <h2>Log In</h2>
      
      <form method="POST" action="login">
        <input type="text" name="user" placeholder="Username" />      
        <input type="password" name="pass" placeholder="Password" />    
        <input type="submit" /> 
      </form>           
    </main>                       
  </body>                             
</html> 
```

---------------------------------

<br>

```http
POST /login HTTP/1.1
Host: flag.local
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Connection: close

user=realbusinessuser&pass=potoooooooo
```

```http
HTTP/1.1 302 Found
x-powered-by: Express
set-cookie: real_business_token=PHNjcmlwdD5hbGVydCgid2F0Iik8L3NjcmlwdD4%3D; Path=/
location: /
vary: Accept
content-type: text/plain; charset=utf-8
content-length: 23
date: Tue, 16 Oct 2018 20:55:26 GMT
connection: close

Found. Redirecting to /
```

------------------------------

<br>

```http
GET / HTTP/1.1
Host: flag.local
Cookie: real_business_token=PHNjcmlwdD5hbGVydCgid2F0Iik8L3NjcmlwdD4%3D;
Connection: close
```

```http
HTTP/1.1 200 OK
x-powered-by: Express
content-type: text/html; charset=utf-8
content-length: 438
etag: W/"1b6-bgxSS92CBVm1uJx+NK7DdppIBp8"
date: 
connection: close


<html>
  <head>
    <link rel="stylesheet" type="text/css" href="main.css" />
  </head>
  <body>
    <header>
      <h1>Real Business Internal Flag Server</h1>
      <div class="user">Real Business Employee</div>
      <a href="/logout">Logout</a>
    </header>
    <main>
      <p>Hello <b>Real Business Employee</b>!  Today's flag is: <code>picoCTF{0nLY_Us3_n0N_GmO_xF3r_pR0tOcol5_5f5f}</code></p>
    </main>
  </body>
</html>
```


<br><br>

## FLAG: picoCTF{0nLY_Us3_n0N_GmO_xF3r_pR0tOcol5_5f5f}
