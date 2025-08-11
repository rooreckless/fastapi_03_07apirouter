# fastapi/tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    # ルータ構成に合わせて適宜変更
    resp = client.get("/items")  # 例: /items が 200 を返すなら
    assert resp.status_code == 200
