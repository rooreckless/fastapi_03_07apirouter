# app/dto/category_dto.py
# スキーマ
# # dtoディレクトリは、リクエストとレスポンスのデータ構造を定義するためのモデル(Pydanticモデル)を管理するフォルダです。
# # このフォルダに配置するファイルは、APIを通じて送受信されるデータの形式と検証ルールを指定します。
# # このファイルにより、データのバリデーションが自動で行われ、APIの利用者に対して一貫したデータ形式を保証します。

from pydantic import BaseModel

class CategoryCreateDTO(BaseModel):
    category_name: str

class CategoryUpdateDTO(CategoryCreateDTO):
    pass
    # class Config:
    #     from_attributes = True

class CategoryReadDTO(CategoryCreateDTO):
    category_id: int

    class Config:
        # orm_mode = True
        from_attributes = True