uvを使うようになり、pipをパッケージ管理として使わなくなったので、requirements.txtを削除しました。この変更はプロジェクトの実行方法などに影響が大きいので、実行方法などをまとめています。

これからは、pyproject.tomlを使用して管理するようになります。

1. pyproject.tomlを更新して使うパッケージが増えた場合は、このプロジェクトのfastapiディレクトリへ移動してから、`uv lock`コマンドを実行し、`uv.lock`ファイルを更新してください。

```shell
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
3. `docker compose up -d`で起動する

その後にテストやruffチェックがしたい場合は以下のコマンドを実行する(`--profile qa`を使う必要があるのはdocker-compose.ymlでprofilesを指定してるから。)

4 pytest,ruff,basedpyright(pyrightの代替)の実行について

- テスト実行 : `docker compose --profile qa run --rm test pytest`
  - これはtestケースファイルの配置を`fastapi/tests`においているからできること。
  - カバレッジレポートもついたテストをしたいなら、`docker compose --profile qa run --rm test pytest --cov=app --cov-report=term-missing`
    - カバレッジレポートの記載内容は[pytestのすぐに使えるカバレッジ計測](https://qiita.com/kg1/items/e2fc65e4189faf50bfe6)
- ruffによるコードの静的解析 : `docker compose --profile qa run --rm ruff ruff check /fastapi/app`
  - ruffとはの説明は[Pythonの Ruff (linter) でコード整形もできるようになりました](https://qiita.com/ciscorn/items/bf78b7ad8e0e332f891b)
  - 解析と同時に修正したい場合は`--fix`をつける(でも安全なものだけやってくれるから気休め程度) : `docker compose --profile qa run --rm ruff ruff check /fastapi/app --fix`
- ruffによるコード整形(blackなどのフォーマッタの機能) : `docker compose --profile qa run --rm ruff ruff format /fastapi/app`
- pyright(型チェック。vscodeならpylance拡張機能) : `docker compose --profile qa run --rm ruff basedpyright`
  - もし、以下のように`typecheck`サービスをdocker-compose.ymlに記述したなら、
    ```YAML
    typecheck:
    profiles: ["qa"]  # 任意
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
   `docker compose --profile qa run --rm ruff basedpyright`コマンドでもいい。
  - ただし上記2つのコマンドだけだと、「warning=警告」の分もでてきて面倒。`fastapi/pyrightconfig.json`で、黙らせたい`warning`を記述して、`None`にしておこう。

一応、ruffサービスのコンテナは、`command: ["/fastapi/.venv/bin/ruff", "check", "/fastapi/app", "--watch"]`を使っている場合、`docker compose --profile qa up`としておけば、ruffチェックだけは監視してくれます。(でも使わないかな? vscodeのruff拡張とpylance拡張で十分そうだし...。)


---

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