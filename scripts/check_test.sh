#!/bin/bash

# ~/fastapi_03_07apirouterディレクトリで、./scripts/check_test.sh を入力して実行してください。
# fastapi/appのソースコードファイルと、対応する、fastapi/testsのテストコードファイルが存在するかどうかを確認するスクリプト

# スクリプトのあるディレクトリ（絶対パス）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"

SRC_DIR="$PROJECT_ROOT/fastapi/app"
TEST_DIR="$PROJECT_ROOT/fastapi/tests"

echo "==== テスト未作成ファイル一覧（__init__.py は除外） ===="

find "$SRC_DIR" -type f -name "*.py" | while read -r src_file; do
  filename=$(basename "$src_file")

  # __init__.py は除外
  if [ "$filename" = "__init__.py" ]; then
    continue
  fi

  # 相対パスをもとに対応するテストファイルを構築
  relative_path="${src_file#$SRC_DIR/}"
  test_file="$TEST_DIR/${relative_path%.py}"
  test_file_dir=$(dirname "$test_file")
  base_name=$(basename "$test_file")
  test_file="${test_file_dir}/test_${base_name}.py"

  # 絶対パスに変換（realpathで ../ を解消）
  abs_src_file=$(realpath "$src_file")
  abs_test_file=$(realpath -m "$test_file")

  if [ ! -f "$test_file" ]; then
    echo "$abs_src_file → ❌ $abs_test_file (not found)"
  fi
done
