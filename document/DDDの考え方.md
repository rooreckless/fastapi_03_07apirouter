```
# [DI] ... …… FastAPI Depends() による 依存性注入ポイント

# [DIP] ... …… 抽象 ↔ 具象 の結合箇所（依存性の逆転が効いている部分）
```

```shell
myapp/
├─ domain/            ← ①ドメイン層
│   ├─ user.py          ←エンティティ(↓の値オブジェクトをインポート)
│   └─ value_objects.py ←値オブジェクト
├─ repository/        ← ②インターフェース(④の抽象クラス)
│   └─ user.py
├─ usecase/           ← ③ユースケース層(⑤から呼ばれ、②に依存しておいて④を操作する(対象は①))
│   └─ create_user.py
├─ infra/             ← ④リポジトリ層(②を継承し具体化したもの。ORMモデルがある)
│   └─ sqlalchemy_repo.py
├─ db.py              ← 共通 DB セッション依存性
└─ main.py            ← ⑤ Presentation（FastAPI）エンドポイント
```
#------

① domain/user.py
ビジネスルール中心。外部ライブラリゼロ＝上位層に依存しない
主にエンティティの方
```python
# ①domain/user.py
from domain.value_objects import Email　# 値オブジェクトをインポート

# Userクラスはドメイン駆動設計における「エンティティ」(エンティティは、user_idなどもつべき。つまり「user_idが一致しているかどうかでUserの一致を判断」できるようにしておく)
class User:
    """① ドメインモデル エンティティ: 業務ルールと振る舞いを保持　ユーザーを一意に識別し、振る舞いを持つ"""

    def __init__(self, user_id: int, name: str, email: Email):
        # ビジネスバリデーション
        # 引数のemail: Emailが値オブジェクト
        if "@" not in email:
            raise ValueError("Invalid email")
        self.id = user_id
        self.name = name
        
        self.email = email

    def change_email(self, new_email: Email):
        if "@" not in new_email:
            raise ValueError("Invalid email format")
        self.email = new_email

```

① domain/value_objects.py
こっちは値オブジェクトの方
```python
# domain/value_objects.py

class Email:
    """① ドメインモデル 値オブジェクト: """
    def __init__(self, address: str):
        #__2つ使っているメソッドは「マジックメソッド」
        # コンストラクタ
        if "@" not in address:
            raise ValueError("Invalid email format")
        self.value = address

    def __eq__(self, other):
        # 「==」演算時、つまりEmailクラスオブジェクト同士を==した時に「オブジェクト同士の「等価性（==）」の定義」。
        return isinstance(other, Email) and self.value == other.value

    def __str__(self):
        # str(Emailオブジェクト)や、print(Emailオブジェクト)を実行した時の挙動を定義。表示用の文字列を返すための定義。
        return self.value
    def __repr__(self):
         # repr(Emailオブジェクト)で、対話モードで表示できる。デバッグ用の文字列を返します（開発者向け）。
        return f"Email('{self.value}')"

    #-----
    # 他のマジックメソッド
    # メソッド名 | タイミング／用途	| 説明
    #-------------------------
    # __call__	   obj() のように呼ばれたとき	インスタンスを関数のように呼び出す振る舞いを定義。
    # __len__	   len(obj) の結果
    # __getitem__  obj["key"] の挙動
    # __setitem__  obj["key"] = val の挙動
    # __iter__ / __next__	イテレーション（for文など）

```

|概念|説明|主な特徴|
|---|---|---|
|エンティティ|一意の識別子（ID）を持ち、永続的な同一性（identity）を持つオブジェクト|属性が変わってもIDで同一と判断|
|値オブジェクト|識別子を持たず、属性の内容で同一性を判断されるオブジェクト|イミュータブル（変更不可）が理想|


② repository/user.py
抽象インターフェース。ここには実装を書かない → 上位層が依存先に選ぶ“契約”

```python
# repository/user.py
from abc import ABC, abstractmethod
from domain.user import User

class UserRepository(ABC):
    """② 抽象リポジトリ: 永続化契約だけを宣言"""

    # [DIP] ③ UseCase はこの抽象に依存する
    @abstractmethod
    def save(self, user: User) -> None:
        """永続化処理（ここの実装は ④ が担う）"""

```

③ usecase/create_user.py
ユースケースは抽象(UserRepository)に依存 → DIP 準拠

```python
# usecase/create_user.py
from domain.user import User
from repository.user import UserRepository  # [DIP] ← 抽象へ依存

class CreateUserUseCase:
    """③ アプリケーション層: ビジネス操作をまとめる"""

    def __init__(self, repo: UserRepository):
        # 上位層は抽象(UserRepository)②だけ知ればよい
        self.repo = repo

    def execute(self, name: str, email: str) -> User:
        user = User(name, email)       # ① ドメインモデルの生成
        self.repo.save(user)           # 抽象へ依頼 → 実装は知らない
        return user

```

④ infra/sqlalchemy_repo.py
SQLAlchemy で抽象を実装する＝DIPの“下位実装”

```python
# infra/sqlalchemy_repo.py
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from repository.user import UserRepository             # [DIP] 抽象を実装
from domain.user import User                           # 型注釈だけで利用

class Base(DeclarativeBase):  # SQLAlchemy ベース
    pass

class UserORM(Base):          # ORMモデル（DBスキーマ）
    __tablename__ = "users"
    id:    Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    name:  Mapped[str]
    email: Mapped[str]

class SQLAlchemyUserRepository(UserRepository):
    """④ 具象リポジトリ: 永続化の詳細を肩代わり"""

    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> None:   # [DIP] 抽象メソッドを実装
        orm = UserORM(name=user.name, email=user.email)
        self.db.add(orm)
        self.db.commit()

```

db.py
SQLAlchemy セッションを依存性として提供

```python
# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from infra.sqlalchemy_repo import Base
from fastapi import Depends

engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
Base.metadata.create_all(engine)

def get_db() -> Session:
    """共通 DB セッション依存性"""
    # ⑤が、「④の具象を作りつつ、②の抽象の型で返すところ」で、このget_dbをDIしている
    db = SessionLocal()
    try:
        yield db            # [DI] FastAPI がリクエスト毎に生成
    finally:
        db.close()

```

⑤ main.py
Presentation層：DIチェーンを組み、DIPを成立させる“配線レイヤー”


```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from repository.user import UserRepository
from infra.sqlalchemy_repo import SQLAlchemyUserRepository  # 具象
from usecase.create_user import CreateUserUseCase           # ユースケース

app = FastAPI()

# ---------- 配線関数（DI Provider） ----------

def get_repo(db: Session = Depends(get_db)) -> UserRepository:
    """④具象を生成しつつ ② 抽象の型で返す"""
    # ここの引数dbは、共通で使うDBセッションの開始と終了の関数でDependsでラップ。
    return SQLAlchemyUserRepository(db)  # [DI] [DIP]

def get_usecase(repo: UserRepository = Depends(get_repo)) -> CreateUserUseCase:
    """③ユースケースを生成"""
    return CreateUserUseCase(repo)       # [DI]

# ---------- Presentation 層エンドポイント ----------

@app.post("/users")
def create_user(
    name:  str,
    email: str,
    uc: CreateUserUseCase = Depends(get_usecase)  # [DI]
):
    try:
        user = uc.execute(name, email)　#③で用意したものを実行
        return {"name": user.name, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

```

```
⑤ main.py (FastAPI) ──[DI]──▶ ③ CreateUserUseCase
                                │
                                └── repo: ② UserRepository(抽象)  ← [DIP] 上位が抽象に依存
                                        ▲
                                        │ ④ SQLAlchemyUserRepository (具象) ── implements
                                        │          │
                                        │          └── uses ORMモデル UserORM
                                        └── Session 由来: get_db()  [DI]


DIポイント：⑤の配線関数でDepends(get_db), ⑤の配線関数でDepends(get_repo), ⑤のエンドポイントの引数Depends(get_usecase)

DIPポイント：CreateUserUseCase ←依存→ UserRepository（抽象）
実装は SQLAlchemyUserRepository が担当し、上位層は知らない

```