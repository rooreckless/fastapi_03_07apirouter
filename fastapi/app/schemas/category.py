# schemasディレクトリは、リクエストとレスポンスのデータ構造を定義するためのモデル(Pydanticモデル)を管理するフォルダです。
# このフォルダに配置するファイルは、APIを通じて送受信されるデータの形式と検証ルールを指定します。
# このファイルにより、データのバリデーションが自動で行われ、APIの利用者に対して一貫したデータ形式を保証します。

from pydantic import BaseModel

class Category(BaseModel):
    category_id: int
    category_name: str