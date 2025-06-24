from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}

@app.get("/abc")
async def abc():
    return {"message": "ABC"}


#--パスパラメータによるget--
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # 例えば、DBからuser_idに対応するユーザ情報を取得する処理をここに記述する
    

