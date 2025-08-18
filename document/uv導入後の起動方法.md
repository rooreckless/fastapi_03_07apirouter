# pipの代わりにuvを使うようになったこと、pytest、githubActionsによるCIについて

## このドキュメントの内容

pipの代わりにuvを使うようになり、pipをパッケージ管理として使わなくなったので、requirements.txtを削除しました。
この変更はプロジェクトの実行方法などに影響が大きいので、実行方法、テストの起動方法などをまとめています。

## uvを使うことで、docker-composeの元でfastapiを起動させる方法の変更点

パッケージ管理は、`fastapi/pyproject.toml`を使用して管理するようになります。

1. `pyproject.toml`を更新して使うパッケージが増えた場合は、このプロジェクトの`fastapi`ディレクトリへ移動してから、`uv lock`コマンドを実行し、`uv.lock`ファイルを更新してください。

```shell
# --- uv.lockを更新する時の様子 ---
~/fastapi_03_07apirouter$ ls
docker-compose.yml  fastapi  postgres
# ↑pyproject.tomlがない...
~/fastapi_03_07apirouter$ cd fastapi/
~/fastapi_03_07apirouter/fastapi$ ls
Dockerfile  alembic.ini  app  pyproject.toml  pyrightconfig.json  requirements.txt  uv.lock
# ↑pyproject.tomlがあるディレクトリに来ている
~/fastapi_03_07apirouter/fastapi$ uv lock
Using CPython 3.12.3 interpreter at: /usr/bin/python3
Resolved 48 packages in 17ms
# ↑これで、uv.lockファイルが更新される
```

2. `docker compose build --no-cache fastapi`コマンドを実行して、fastapiのイメージファイルを作成する

このコマンドは、「キャッシュを一切使わず“完全に作り直す”ことで、イメージ内の依存関係やベースイメージを強制的に最新状態にする」ことです。


3. `docker compose up -d`で起動する

## fastapiが起動した後に、pytestによるtestの実行や、ruff、pyrightによるチェックの実行方法。

fastapi起動後に、テストやruffチェックがしたい場合は以下のコマンドを実行する(`--profile test`を使う必要があるのはdocker-compose.ymlでprofilesを指定してるから。)

4 pytest,ruff,basedpyright(pyrightの代替)の実行について

### テストの実行

- テスト実行 : `docker compose --profile test run --rm pytest-fastapi pytest tests --cache-clear`
  - これはtestケースファイルの配置を`fastapi/tests`においているからできること。
  - コマンドは`docker compose --profile test run --rm pytest-fastapi`と、`pytest`で別れている。つまり、`docker-compose.yml`では`profile`が、`pytest-fastapi`サービスに指定されていて、それが、`test`であり、「このコンテナで、`pytest`コマンドを実行し、実行後はコンテナが自動終了」の意味。`pytest`コマンドの意味は、文字通り「pytestによるテストを行う」のだが、その際のテストケースファイルディレクトリは、「引数で`tests`ディレクトリを指定」の意味である。

### テスト時にカバレッジ計測するには

- カバレッジレポートもついたテストをしたいなら、`docker compose --profile test run --rm pytest-fastapi pytest tests --cache-clear --cov=app --cov-branch --cov-report=term-missing:skip-covered`
    - コマンドの構造は先ほどの`docker compose --profile test run --rm pytest-fastapi pytest tests`の内容に追加して、`--cov=app --cov-branch --cov-report=term-missing:skip-covered`がついている状態。
    - 意味は今までの内容に追加して、「カバレッジ計測と、その計測の仕方、カバレッジレポートの作成とその形式」を意味している。
      - つまり「`tests`ディレクトリの内容でテストする」の後に、「`--cov=app`で、カバレッジ計測してもらいたいが、その際の対象のソースコードは`app`ディレクトリ内のもの」+「`--cov-branch`でブランチカバレッジも計測したい」+「`--cov-report`でカバレッジレポートの設定については、`term-missing`でテストでカバーできていない対象のソースコードの行番号の記載。ただし`:skip-covered`で、100%カバーできているなら、対象のソースコードをレポートから外す(フルカバーできているなら記載する意味がないから)」
#### カバレッジレポートをxmlやhtmlで出力したい
- もし、xml,html形式でカバレッジレポートを出してほしいなら、追加で`--cov-report`を使っていい。例えば以下だと、「コンソール出力としては`term-missing:skip-covered`」、「xmlでのレポート出力先指定」、「htmlでのレポート出力先指定」を指定した形になる。

```shell
# docker compose部分は長いので省略
# pytestの -qオプションは 「Quiet」。これがあると、テストを順次実行時に1つ1つがpassしてもfailでも逐一結果がでない。最終結果やカバレッジレポートだけがでてくる = GithubActionsでのログ出力向き。
pytest tests -q \
--cov=app --cov-branch \
--cov-report=term-missing:skip-covered \
--cov-report=xml:/ci_artifacts/coverage.xml \
--cov-report=html:/ci_artifacts/htmlcov
```
つまり、上記だと、`ci_artifacts`ディレクトリには、`coverage.xml`ファイルと`htmlcov`ディレクトリができることになる。「html形式のレポートは`htmlcov`ディレクトリ内に大量のファイルと共に出来上がる」ので、そのうちの`index.html`をブラウザで開けばレポートになる。

- カバレッジレポートの記載内容は、コンソールやhtmlの場合でも[pytestのすぐに使えるカバレッジ計測](https://qiita.com/kg1/items/e2fc65e4189faf50bfe6)と、[pythonのカバレッジをpytest-covで調べる](https://qiita.com/mink0212/items/34b9def61d58ab781714)。特に`stmts`とか、`cover`の意味、「ステートメントカバレッジ(c0)とブランチカバレッジ(c1)の違い」は見ておくべきかと。

### ruffによるコードの解析

- ruffによるコードの静的解析 : `docker compose --profile test run --rm ruff-fastapi ruff check /fastapi/app`
  - ruffとはの説明は[Pythonの Ruff (linter) でコード整形もできるようになりました](https://qiita.com/ciscorn/items/bf78b7ad8e0e332f891b)
  - 解析と同時に修正したい場合は`--fix`をつける(でも安全なものだけやってくれるから気休め程度) : `docker compose --profile test run --rm ruff-fastapi ruff check /fastapi/app --fix`
- ruffによるコード整形(blackなどのフォーマッタの機能) : `docker compose --profile test run --rm ruff-fastapi ruff format /fastapi/app`

### pyrightによるコードの解析
- pyright(型チェック。vscodeならpylance拡張機能) : `docker compose --profile test run --rm ruff-fastapi basedpyright app`
  - これは`ruff-fastapi`のコンテナに`basedpyright`による型チェックをさせるということ。(別に、`basedPyright`専用のサービスを作らなくても実行できるため。)
  - もし、以下のように`typecheck`サービスをdocker-compose.ymlに記述したなら、
    ```YAML
    typecheck:
    profiles: ["test"]  # 任意
    build:
        context: .
        dockerfile: ./fastapi/Dockerfile/local/Dockerfile
        args: { INCLUDE_DEV: "true" }
    container_name: typecheck-pyright-fastapi
    working_dir: /fastapi
    volumes:
        - ./fastapi/app:/fastapi/app
        - ./fastapi/tests:/fastapi/tests #<- テストケースも型チェックしたい場合のみ
        - ./fastapi/pyrightconfig.json:/fastapi/pyrightconfig.json # <- basedpyrightの設定ファイルの読み込みのため
    ```

  - ただし上記のコマンドだけだと、「warning=警告」の分もでてきて面倒。`fastapi/pyrightconfig.json`で、黙らせたい`warning`を記述して、`None`にしておこう。

- 一応、ruffサービスのコンテナは、`command: ["/fastapi/.venv/bin/ruff", "check", "/fastapi/app", "--watch"]`を使っている場合、`docker compose --profile test up`としておけば、ruffチェックだけは監視してくれます。(でも使わないかな? vscodeのruff拡張とpylance拡張で十分そうだし...。)

## 今回のプロジェクト用によく使うテスト、ruff、pyright用コマンド

```shell
## pytest (カバレッジ計測、ブランチカバレッジつき、未カバー行番号取得、フルカバーを省略)
docker compose --profile test run --rm pytest-fastapi pytest tests \
  --cov=app --cov-branch \
  --cov-report=term-missing:skip-covered
### 上に+でxml,htmlレポート出力+ いちいちテストケースのpass,failを出力せず最後にまとめて出力
docker compose --profile test run --rm pytest-fastapi pytest tests -q \
  --cov=app --cov-branch \
  --cov-report=term-missing:skip-covered \
  --cov-report=xml:/ci_artifacts/coverage.xml \
  --cov-report=html:/ci_artifacts/htmlcov


## ruffによるコードチェック

docker compose --profile test run --rm ruff-fastapi ruff check /fastapi/app

## ruff 自動修正つき

docker compose --profile test run --rm ruff-fastapi ruff check /fastapi/app --fix
#　or
docker compose --profile test run --rm ruff-fastapi ruff format /fastapi/app


## pyrightによる型チェック
docker compose --profile test run --rm ruff-fastapi basedpyright app
```

## 何度もテストしたり、ruffチェックするために

ローカル開発では、ソースコードを編集するたびにテストを実施したり、ruffチェックやbasedpyrightのチェックをしたいはずです。

つまり、上記の`docker compose --profile test run --rm`は「最初の1回目は成功」するのですが、2回目を実行すると失敗するケースがあります。

これに対応するため、テスト開始やruff、basedpyrightの実行手順を分割します。

```shell
# 0-1 必要な時はuv lockをしてください
cd fastapi
uv lock
# 0-2 ビルド
cd ../
docker compose build --no-cache fastapi

# 1 通常のfastapiとpostgresの起動
docker compose up -d
# 2 profile = devのサービスをバックグラウンドで起動
#(devのprofileにはfastapi, postgres, ruff-fastapi, pytest-fastapiが所属している)
docker compose --profile test up -d

# 3 テストをしたい場合、
docker compose exec pytest-fastapi pytest tests

# 3-2 テスト + cov + cov-branch + レポート(コンソール,xml,html)+ q
docker compose exec pytest-fastapi pytest tests -q \
  --cov=app --cov-branch \
  --cov-report=term-missing:skip-covered \
  --cov-report=xml:/ci_artifacts/coverage.xml \
  --cov-report=html:/ci_artifacts/htmlcov
# ↑ただし、生成されるカバレッジレポートはroot権限でないと編集、削除できない
# その場合は、sudo chmod -R 777 ci_artifactsを実行すること


## 4 ruffによるコードチェック

docker compose exec ruff-fastapi ruff check /fastapi/app
# もちろんfastapi/tests内もruffチェックできる
docker compose exec ruff-fastapi ruff check /fastapi/tests

## 4-2ruff 自動修正つき

docker compose exec ruff-fastapi ruff check /fastapi/app --fix
#　or
docker compose exec ruff-fastapi ruff format /fastapi/app


## 5 basedpyrightによる型チェック
docker compose exec ruff-fastapi basedpyright /fastapi/app
# もちろんfastapi/tests内もbasedpyrightによる型チェックできる
docker compose exec ruff-fastapi basedpyright /fastapi/tests
# 6 終了
docker compose down
docker compose --profile test down
```


## 【余談】ruffとpyright(=basedpyright)の違い

ruffとpyright(=basedpyright)の違いは、

1. ruff の静的解析（コード品質・スタイル）
- 主目的: コード品質や可読性のチェック
- 見ているもの:
  - PEP8 準拠（インデント・空白・改行位置）
  - 命名規則（関数・変数・クラス名）
  - 未使用変数や import
  - セキュリティ的に危ない書き方（例: eval）
  - 一部のバグの可能性（例えば == None の代わりに is None）

- 型情報の扱い:
  - 基本的に型推論は浅い（型定義ミスを本格的に検出しない）

例:

```python
import os  # ← 未使用 → ruff が警告
def add(a, b): return a+b  # ← 改行やスペースがPEP8違反 → ruff が警告
```

2. pyright / basedpyright の静的解析（型チェック）
- 主目的: 型アノテーションに基づく型整合性の検証
- 見ているもの:
  - 関数引数・戻り値の型不一致
  - None を許可していない変数に None を代入
  - 非同期関数の await 忘れ
  - 存在しない属性やメソッドの呼び出し

- 型情報の扱い:
  - PEP 484 / PEP 561 の型ヒントをガチで解析
  - 型定義ファイル（.pyi）やサードパーティの型情報も参照

例:

```python
def greet(name: str) -> None:
    print(name.upper())

greet(123)  # ← pyright が型エラー
```


両者の違いを一言で
- ruff → 「書き方が綺麗か？ 無駄がないか？」
- pyright → 「型的に正しいか？ 間違いが起きないか？」

重複しているようで違う部分

確かに両方「静的解析」という広いカテゴリに入りますが、

- ruff は 構文とスタイル・品質中心
- pyright は 型とロジックの整合性中心

という棲み分けになっています。


# テスト作成

基本的にはソースコードは`fastapi/app`ディレクトリ内にあるので、これに対するテストケースは`fastapi/tests`に配置することになる。そして、単体テストとしては、ソースコードファイルと、単体テストケースファイルは1対1で対応するものとする。

例えば、
- ソースファイルの`fastapi/app/domain/category/value_objects.py`に対するテストケースファイルは、`fastapi/tests/domain/category/test_value_objects.py`が対応する。
  - このテストケースファイルで、対応するソースファイルに対し単独で、c0,c1カバレッジ100%であり、正常系、異常系、エッジケースの確認ができるようにする。
  - 上記ソースファイルと同じ階層には`category.py`があるが、これが対応するテストケースファイルは、`fastapi/tests/domain/category/test_category.py`とする。`test_value_objects.py`に混ぜ込んだりはしない。
- 値オブジェクト、エンティティ、ユースケース、エンドポイント、スキーマなどのソースファイルに対するテストの考え方は以下。
  - 値オブジェクト：入力値の妥当性確認に責任 → 厳密に異常系をテスト
  - エンティティ：既に妥当な値を使う前提 → 異常系テストは最小限でよい(値オブジェクトで十分なテストをしている場合、最小限いい場合が多いか。)
  - サービス層やAPI：ユーザー入力が来る層 → 正常/異常/境界値をしっかりテスト

## DBアクセスなどを伴わないテストの場合のプロンプト

claude sonnet4 のAgentモードを使い、GithubCopilotに単体テストを作成させる場合のプロンプトを考えてみる。

この章では、「実際に稼働しているDBへのアクセスを伴わない場合」のテストを含めた、通常の単体テストを作成する場合のプロンプトとする。

```
`fastapi/app/domain/items`ディレクトリ内のPythonモジュールについて、unittest.mockは利用せず、pytestとpytest-mockのみを利用して単体テストコード作成してください。なお、テストケース作成時には以下の11点を守って作成して下さい。
(1) 1モジュールにつき、1テストファイルを作成、テストファイル名は「test_(module_name).py」とする
(2) 1テストファイルは、テストケースごとに1テスト関数を作成し、テスト関数の関数名は必ず英語で作成する。ただし、__init__.pyファイルについてのテストケースを作成する必要はないです。
(3) 内容については、対象モジュールについて対応する1テストファイルでc0,c1カバレッジ100%をみたし、正常系・異常系・エッジケースを網羅する単体テストコードを作成してください。
(4) docstringは必ず日本語で作成し、作成したテスト関数のテストが正常系・異常系・エッジケースのどれに該当するかをdocstringにて「正常系:」、「異常系:」、「エッジケース:」を記載すること。
(5) 単体テストの観点で必要なテストを作成すること
(6) 作成したテストモジュールは`fastapi/tests`ディレクトリ内に配置すること。対象ソースファイルと同階層に配置することは禁止する。例えば、対象のモジュールが`fastapi/app/domain/items/xxx.py`であるならば、これに対するテストモジュールは`fastapi/tests/domain/items/test_xxx.py`として作成すること。
(7) モジュールが非同期の場合、テストには`@pytest.mark.anyio`を使用すること。
(8) Lintチェックにかかるテストケースを作成してほしくないです。なので、`docker compose exec ruff-fastapi basedpyright /fastapi/tests`コマンド、`docker compose exec ruff-fastapi ruff check /fastapi/tests`コマンドを実行した際に、エラーが発生しないようにしてください。
(9) テストの実行コマンドは、`docker compose exec pytest-fastapi pytest tests`を使用してください。また、作成したテストについてカバレッジが条件をみたしているかどうかの確認には、`docker compose exec pytest-fastapi pytest tests \
  --cov=app --cov-branch \
  --cov-report=term-missing:skip-covered`コマンドを使ってください。
(10) このプロジェクトでは、docker compose を使用していて、プロジェクトの最上位ディレクトリにdocker-compose.ymlファイルがあります。
(11) テストを作成する過程で、python仮想環境の作成はしないでださい。
```



## DBアクセスを伴うテストの場合のプロンプト

```
✅ integrate_tests に配置すべき主なテストの種類
1. DBアクセスを伴うテスト（モックなし）

典型例：

SQLAlchemy ORM / リポジトリを通じてレコードを読み書き

実際のPostgreSQLとやり取りして、CRUD処理が正しく行えるか確認

配置理由：ユースケース層やリポジトリ層の 実際の動作検証

2. HTTP経由のエンドポイントテスト（FastAPIの依存関係込み）

例：

TestClient や AsyncClient を使って /items/ や /users/login などのエンドポイントを叩く

実DBにアクセスしつつ、FastAPIの DI（依存性注入）も通る

配置理由：エンドツーエンドに近い形でコントローラ層（=ルーター）+ユースケース+DB層の一貫動作を確認

3. 外部APIアクセスがあるが、あえてモック化しないもの

例：

HTTPクライアント（httpxやrequests）を使って外部APIを叩く処理

モックせずに 実サーバ or ステージングAPIに接続してテストする

配置理由：統合的に「外部サービスとの連携が正しく機能しているか」を検証

4. メッセージングやキュー（例：Redis, RabbitMQ）との統合テスト

例：

Celeryタスクが正しく呼び出され、期待通りのジョブが実行されるか

配置理由：インフラ層の 非同期ワークフローの一貫動作確認


❌ integrate_tests に配置しない方がよいもの
テスト内容	理由	配置先
モックを使ったユースケース層のテスト	DBや外部APIに依存しないため	tests/
バリデーションロジック（Pydanticなど）の検証	I/Oや外部システムに依存しない	tests/
単体のサービス・クラスのロジック	関心の分離ができておりモックで十分	tests/
✅ まとめ
テストの性質	tests/ に配置	integrate_tests/ に配置
DBや外部APIをモック化してテスト	✅	❌
DBや外部APIに実際にアクセスする	❌	✅
FastAPIアプリを起動し、エンドポイントを叩く	❌	✅
Pydanticバリデーションなどの軽量なロジック	✅	❌
```