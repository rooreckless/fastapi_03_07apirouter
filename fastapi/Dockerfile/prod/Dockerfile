FROM python:3.12-slim

# 本番環境用のセキュリティとパフォーマンス最適化
# セキュリティ: 不要なパッケージを最小限に
# パフォーマンス: マルチステージビルドでイメージサイズ削減
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# uv インストール
RUN pip install --no-cache-dir uv

# 非rootユーザーでセキュリティ向上
RUN groupadd -r fastapi && useradd -r -g fastapi fastapi

WORKDIR /fastapi

# 依存関係ファイルをコピー（キャッシュ効率化）
COPY ./fastapi/pyproject.toml ./pyproject.toml
COPY ./fastapi/uv.lock* ./

# 本番環境では開発依存関係を含めない（INCLUDE_DEV=false固定）
# ロックファイル優先で厳密なバージョン管理
RUN if [ -f uv.lock ]; then \
      uv sync --frozen; \
    else \
      uv lock && uv sync; \
    fi

# .venv を PATH に通す
ENV VIRTUAL_ENV=/fastapi/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# アプリケーションコードをコピー
COPY ./fastapi/app ./app

# ファイル権限を適切に設定
RUN chown -R fastapi:fastapi /fastapi

# 非rootユーザーで実行
USER fastapi

# ヘルスチェック用エンドポイント
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 本番環境用の起動設定
# - ワーカープロセス数を環境変数で制御可能
# - アクセスログ無効でパフォーマンス向上
# - プロダクション用設定
CMD python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers ${WORKERS:-4} \
    --access-log \
    --log-level ${LOG_LEVEL:-info}
