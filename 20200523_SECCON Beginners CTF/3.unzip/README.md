# unzip

```
point:188 Easy

Unzip Your .zip Archive Like a Pro.
 https://unzip.quals.beginners.seccon.jp/

Hint:index.php (sha1: 968357c7a82367eb1ad6c3a4e9a52a30eada2a7d)
Hint:(updated at 5/23 17:30) docker-compose.yml
```

<br>

## Solution

![1](https://user-images.githubusercontent.com/47602064/82997016-c9ab0180-a040-11ea-998b-deae5f3e25f6.png)

問題に移動するとファイルをアップロードできるサイトになっています。

タイトルから考えるようにzipファイルが関係していそうです。

試しに適当なファイルを入れたzipファイルをアップロードして送ると展開して中身が表示できるサイトとわかりました。

展開されたファイル名をクリックすると中身が見れました。

その状態でURL上を見るとディレクトリが含まれて表示されています。

`/?filename={filename}`

この時にディレクトリが関係しているので`path traversal`が関係していると考えられます。

<br>

ヒントでphpソースコードとymlテキストがあるのでそちらも見てみます。

まず`docker-compose.yml`を見てみると以下に注目します。

```yml
 php-fpm:
    build: ./docker/php-fpm
    env_file: .env
    working_dir: /var/www/web
    environment:
      TZ: "Asia/Tokyo"
    volumes:
      - ./public:/var/www/web
      - ./uploads:/uploads
      - ./flag.txt:/flag.txt
    restart: always
```

これよりflagは`flag.txt`に入ってそうなことがわかります。

試しに直接url上で`../../../../flag.txt`と指定してみます。

`https://unzip.quals.beginners.seccon.jp/?filename=../../../../flag.txt`

でもflagは表示されませんでした。(アクセスできなかった)

`no such file`

<br>

次に試したのは新しく`flag.txt`をアップロードしてみました。

すると既に同じファイル名があると判定されて無理でした。

`index.php`を見てみると以下で処理がされていました。

```php
// add files to $_SESSION["files"]
for ($i = 0; $i < $zip->numFiles; $i++) {
    $s = $zip->statIndex($i);
    if (!in_array($s["name"], $_SESSION["files"], TRUE)) {
        $_SESSION["files"][] = $s["name"];
    }
}
```

ファイル名の重複判定をした後に`$_SESSION["files"]`にファイル名が入れられていることがわかります。

なので悪意のあるファイル名にしてアップロードがされたら、ディレクトリを渡ってflag.txtにアクセスできるようにします。


<br>

次に`index.php`でfileがアップロードされた後、どのように処理されているかを探すと以下を注目します。

```php
// return file if filename parameter is passed
if (isset($_GET["filename"]) && is_string(($_GET["filename"]))) {
    if (in_array($_GET["filename"], $_SESSION["files"], TRUE)) {
        $filepath = $user_dir . "/" . $_GET["filename"];
        header("Content-Type: text/plain");
        echo file_get_contents($filepath);
```

これより`filename`がそのまま`filepath`に格納されていることがわかります。

なのでアップロードするファイル名にflagへのディレクトリが入ればアクセスできそうです。

ですが、ファイル名に`../`などを付けることは普通できません。

なのでzipに圧縮するときに工夫をしてみます。

それには実際の自分の環境に同じようなディレクトリを作ってそれで作ってみます。

```
$touch flag.txt
$mkdir -p dr/dr/dr/dr/
$cd dr/dr/dr/dr/
$zip flag.zip ../../../../flag.txt
```

<br>

これでファイル名に`../`を含めることが出来ました。

そして生成したzipファイルをアップロードしてみます。

すると以下のように画面に表示されます。

![2](https://user-images.githubusercontent.com/47602064/82999796-80f54780-a044-11ea-8c62-b32584e83187.png)

これで中身の`../../../../flag.txt`を表示させてみると以下のようにflagが表示されました。

`https://unzip.quals.beginners.seccon.jp/?filename=..%2F..%2F..%2F..%2Fflag.txt`

![3](https://user-images.githubusercontent.com/47602064/82998336-92d5eb00-a042-11ea-81ed-e1e391fd07ac.png)

<br><br>

## FLAG: ctf4b{y0u_c4nn07_7ru57_4ny_1npu75_1nclud1n6_z1p_f1l3n4m35}
