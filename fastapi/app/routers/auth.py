# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.jwt import decode_token
from app.db import get_db
from app.dto.user_dto import UserCreateDTO, UserReadDTO, TokenDTO, UserLoginDTO
from app.usecases.user.create_user import CreateUserUseCase
from app.usecases.user.authenticate_user import AuthenticateUserUseCase
from app.usecases.user.get_user import GetUserUseCase
from app.infrastructure.sqlalchemy.repo_imples.user_repo_impl import SQLAlchemyUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyUserRepository:
    """ユーザーリポジトリの依存性注入"""
    return SQLAlchemyUserRepository(db)


@router.post("/register", response_model=UserReadDTO, status_code=201)
async def register(
    payload: UserCreateDTO, 
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserReadDTO:
    """ユーザー登録エンドポイント"""
    try:
        create_user_usecase = CreateUserUseCase(user_repo)
        return await create_user_usecase.execute(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenDTO)
async def login(
    mail_address: Annotated[str, Form(description="メールアドレス")],
    password: Annotated[str, Form(description="パスワード")],
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> TokenDTO:
    """アプリとしてのログインエンドポイント"""
    # Formを使用してmail_addressフィールドを明確にする
    # --Swagger UIでログインをテストする場合は、右上のauthorizeボタンから行いましょう
    login_data = UserLoginDTO(
        mail_address=mail_address,
        password=password
    )
    
    authenticate_usecase = AuthenticateUserUseCase(user_repo)
    token = await authenticate_usecase.execute(login_data)
    
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return token


@router.post("/token", response_model=TokenDTO)
async def token(
    form: OAuth2PasswordRequestForm = Depends(),
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> TokenDTO:
    """OAuth2標準のトークンエンドポイント（usernameフィールドにメールアドレスを入力）"""
    # OAuth2PasswordRequestFormのusernameフィールドにメールアドレスが入る
    login_data = UserLoginDTO(
        mail_address=form.username,
        password=form.password
    )
    
    authenticate_usecase = AuthenticateUserUseCase(user_repo)
    token = await authenticate_usecase.execute(login_data)
    
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return token


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UserReadDTO:
    """現在のユーザーを取得する依存性関数"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"トークンを受信: {token[:50] if token else 'None'}...")
    
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
        logger.info(f"トークンから抽出したユーザーID: {user_id}")
    except Exception as e:
        logger.error(f"トークンのデコードエラー: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    get_user_usecase = GetUserUseCase(user_repo)
    user = await get_user_usecase.execute(user_id)
    
    if user is None or not user.is_active:
        logger.warning(f"ユーザーが見つからないか非アクティブ: user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or missing user",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    logger.info(f"認証成功: user_id={user.user_id}")
    return user


@router.get("/me", response_model=UserReadDTO)
async def get_me(current_user: UserReadDTO = Depends(get_current_user)) -> UserReadDTO:
    """現在のユーザー情報を取得"""
    return current_user
