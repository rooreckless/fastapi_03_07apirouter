# VSCodeでの実行とデバッグとテストの方法

このドキュメントでは、プロジェクトをクローンした直後からVS Codeで開発を開始するまでの手順を説明します。

## 目次

1. [事前準備](#事前準備)
2. [プロジェクトセットアップ](#プロジェクトセットアップ)
3. [VS Codeでのデバッグ実行](#vs-codeでのデバッグ実行)
4. [テスト実行方法](#テスト実行方法)
5. [トラブルシューティング](#トラブルシューティング)

## 事前準備

### 必要なソフトウェア

- **Docker** または **Podman**（データベースコンテナ用）
- **Python 3.11+**
- **uv**（Python依存関係管理ツール）
- **VS Code**
- **Git**

### uvのインストール

```bash
# Linux/macOS/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### VS Code拡張機能

以下の拡張機能をインストールしてください：

- **Python** (`ms-python.python`)
- **Python Debugger** (`ms-python.debugpy`)
- **Ruff** (`charliermarsh.ruff`)

## プロジェクトセットアップ

### 1. プロジェクトのクローン

```bash
git clone [リポジトリURL]
cd fastapi_03_07apirouter
```

### 2. Python仮想環境とパッケージのセットアップ

```bash
# fastapiディレクトリに移動
cd fastapi

# uv syncで依存関係をインストール（仮想環境も自動作成）
uv sync

# 開発用依存関係も含めてインストール（推奨）
uv sync --group dev
```

### 3. VS Codeでプロジェクトを開く

```bash
# プロジェクトルートでVS Codeを開く
cd ..
code .
```

### 4. Python インタープリターの設定

VS Code内で：

1. `Ctrl+Shift+P` でコマンドパレットを開く
2. `Python: Select Interpreter` を実行
3. `./fastapi/.venv/bin/python` を選択

**注意**: プロジェクトルート直下の `.venv` ではなく、`fastapi/.venv` を選択してください。

## VS Codeでのデバッグ実行

### データベースコンテナの起動

デバッグ実行前に、必ずデータベースコンテナを起動してください：

```bash
# プロジェクトルートディレクトリで実行
docker-compose up postgres

# または Podman を使用している場合
podman-compose up postgres
```

### デバッグ設定

プロジェクトには2つのデバッグ設定が用意されています：

#### 1. FastAPI Debug
- 基本的なデバッグ設定
- ホスト: `0.0.0.0`（外部からのアクセス可能）

#### 2. FastAPI Debug (Local DB) 【推奨】
- ローカル開発用の詳細設定
- ホスト: `127.0.0.1`（ローカルのみ）
- ログレベル: debug

### デバッグ実行手順

1. **データベースコンテナが起動していることを確認**
2. `Ctrl+Shift+D` で「実行とデバッグ」パネルを開く
3. プルダウンから `FastAPI Debug (Local DB)` を選択
4. `F5` キーまたは緑の再生ボタンでデバッグ開始
5. ブラウザで `http://localhost:8000` にアクセス

### API ドキュメントへのアクセス

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### ブレークポイントの設定

- コードの行番号左側をクリックしてブレークポイントを設定
- デバッグ実行中にブレークポイントで停止
- 変数の値を確認したり、ステップ実行が可能

## テスト実行方法

### 1. VS Code内でのテスト実行

#### テストエクスプローラーを使用

1. `Ctrl+Shift+P` でコマンドパレットを開く
2. `Python: Configure Tests` を実行
3. `pytest` を選択
4. テストディレクトリ (`tests`) を選択
5. サイドバーの「テスト」アイコンからテストを実行

#### 個別テストファイルの実行

```bash
# fastapiディレクトリで実行
cd fastapi

# 単一テストファイル
uv run pytest tests/test_main.py

# 特定のテスト関数
uv run pytest tests/test_main.py::test_read_root

# カバレッジ付きで全テスト実行
uv run pytest --cov=app --cov-report=html
```

### 2. 統合テストの実行

```bash
# 統合テスト用のデータベースが必要
docker-compose up postgres -d

# 統合テスト実行
cd fastapi
uv run pytest integrate_tests/
```

### 3. コード品質チェック

```bash
# fastapiディレクトリで実行
cd fastapi

# Ruffによるリント
uv run ruff check .

# Ruffによる自動修正
uv run ruff check . --fix

# フォーマット
uv run ruff format .

# 型チェック
uv run basedpyright
```

## 環境変数の設定

プロジェクトでは環境変数を以下のファイルで管理しています：

### 環境別ファイル構成

- `.envs/local/env_local`: ローカル開発環境用（Docker Compose）
- `.envs/local/env_debug`: VS Code デバッグ実行用（localhost接続）
- `.envs/production/env_prod`: 本番環境用

### 各ファイルの用途

- **env_local**: Docker Compose実行時に使用。コンテナ間通信用の設定
- **env_debug**: VS Code デバッグ実行時に使用。localhost接続用の設定
- **env_prod**: 本番環境デプロイ時に使用

デバッグ実行では `.envs/local/env_debug` が自動的に読み込まれます。

## よく使用するコマンド

```bash
# 開発サーバーの起動（コマンドライン）
cd fastapi
uv run uvicorn app.main:app --reload

# 新しい依存関係の追加
uv add 新しいパッケージ名

# 開発用依存関係の追加
uv add --group dev 開発用パッケージ名

# 仮想環境のシェルに入る
uv shell
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. `No module named 'uvicorn'` エラー

```bash
# fastapiディレクトリで依存関係を再インストール
cd fastapi
uv sync
```

#### 2. Python インタープリターが見つからない

VS Codeで：
1. `Ctrl+Shift+P` → `Python: Select Interpreter`
2. `./fastapi/.venv/bin/python` を選択

#### 3. データベース接続エラー

```bash
# PostgreSQLコンテナの状態を確認
docker ps
docker-compose logs postgres

# コンテナを再起動
docker-compose down
docker-compose up postgres
```

#### 4. ポート8000が使用中

```bash
# ポートを使用しているプロセスを確認
lsof -i :8000

# プロセスを終了（PIDを確認してから）
kill -9 [PID]
```

#### 5. VS Codeでデバッグが開始できない

1. Python インタープリターが正しく設定されているか確認
2. `.envs/local/vscode` ファイルが存在するか確認
3. PostgreSQLコンテナが起動しているか確認
4. VS Codeを再起動

### ログの確認

```bash
# FastAPIアプリケーションのログ
# VS Codeのデバッグコンソールまたはターミナルで確認

# PostgreSQLコンテナのログ
docker-compose logs postgres

# uvicornの詳細ログ（手動実行時）
uv run uvicorn app.main:app --reload --log-level debug
```

## 開発ワークフロー

### 1. 新機能開発の流れ

1. データベースコンテナを起動
2. VS Codeでデバッグ実行
3. コードを編集（ホットリロード有効）
4. ブレークポイントでデバッグ
5. テスト実行
6. コード品質チェック

### 2. プルリクエスト前のチェック

```bash
cd fastapi

# すべてのテストが通ることを確認
uv run pytest

# コードフォーマットとリントチェック
uv run ruff format .
uv run ruff check .

# 型チェック
uv run basedpyright
```

## その他の便利な情報

### VS Code設定ファイルについて

- `.vscode/launch.json`: デバッグ設定
- `.vscode/settings.json`: ワークスペース設定

これらのファイルは既にプロジェクトに含まれているため、追加設定は不要です。

### 開発に便利なVS Code拡張機能（オプション）

- **GitLens** (`eamodio.gitlens`): Git履歴の可視化
- **Thunder Client** (`rangav.vscode-thunder-client`): API テストツール
- **SQLite Viewer** (`qwtel.sqlite-viewer`): SQLiteファイルの表示
- **Docker** (`ms-azuretools.vscode-docker`): Dockerコンテナ管理

---

このガイドに従って環境をセットアップすれば、すぐにVS Codeでの開発を開始できます。
問題が発生した場合は、まずトラブルシューティングセクションを確認してください。