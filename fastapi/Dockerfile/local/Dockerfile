FROM python:3.12-slim

# 必要ならビルド系も（psycopg2 等で必要になる時がある）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# uv インストール
RUN pip install --no-cache-dir uv

WORKDIR /fastapi

# 依存（キャッシュが効く層）
COPY ./fastapi/pyproject.toml ./pyproject.toml
COPY ./fastapi/uv.lock* ./

# uvを使って、依存パッケージをインストールする コンテナイメージの/fastapi/.venv に同期する（lock があれば --frozen で厳密適用）
# --group devを指定することで、pyproject.tomlのdependency-groupsのうち、devのパッケージも追加適用される
# ただし、uv.lockがない場合は、pyproject.tomlの内容を元にパッケージをインストールするが、uv.lockは生成しないで(コンテナイメージにあるが、volumes=ローカルにはでてこない)適用される
# pyproject.tomlを更新したら、ローカルでuv lockを使い、uv.lockも更新してください。でないと、uv sync --frozenでエラーになる可能性があるからです。(一応elseの方で起動できるけど。)
# RUN if [ -f uv.lock ]; then \
#       uv sync --frozen --group dev; \
#     else \
#       uv lock && uv sync --group dev; \
#     fi

# 引数: dev 依存を含めるか？
ARG INCLUDE_DEV=false

# .venv へ同期（ロックがあれば --frozen で厳密適用）
RUN if [ -f uv.lock ]; then \
      if [ "$INCLUDE_DEV" = "true" ]; then uv sync --frozen --group dev; else uv sync --frozen; fi; \
    else \
      if [ "$INCLUDE_DEV" = "true" ]; then uv lock && uv sync --group dev; else uv lock && uv sync; fi; \
    fi


# .venv を PATH に通す（以降 uvicorn 等が見える）
ENV VIRTUAL_ENV=/fastapi/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY ./fastapi/app ./app

# デフォ起動（compose 側で上書きしてもOK）
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
