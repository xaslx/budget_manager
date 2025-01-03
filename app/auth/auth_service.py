from datetime import datetime, timedelta
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from app.exceptions import IncorrectEmailOrPasswordException, TokenExpiredException, TokenAbsentException, IncorrectTokenException, UserIsNotPresentException
from app.config import JwtConfig
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserOut
from dataclasses import dataclass


pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class AuthUtils:
    config: JwtConfig

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

  
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


    def create_access_token(self, data: dict) -> str:
        to_encode: dict = data.copy()
        expire: datetime = datetime.now() + timedelta(days=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.config.secret_key, self.config.algorithm)

    def valid_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.config.secret_key, self.config.algorithm)
        except ExpiredSignatureError:
            raise TokenExpiredException()
        except JWTError:
            raise IncorrectTokenException
        return payload


@dataclass
class AuthService:

    user_repository: UserRepository
    auth_utils: AuthUtils

    async def authenticate_user(self, username: str, password: str) -> UserOut | None:
        user: User = await self.user_repository.find_one_or_none(username=username)
        if not (user and self.auth_utils.verify_password(password, user.hashed_password)):
            raise IncorrectEmailOrPasswordException()
        return UserOut.model_validate(user)
    

    async def get_current_user(self, token: str) -> User | None:

        payload: dict | None = self.auth_utils.valid_token(token=token)
        user_id: str = payload.get("sub")
        user: User = await UserRepository.find_one_or_none(id=int(user_id))
        if user is None:
            return None
        if not user_id:
            raise UserIsNotPresentException()
        if not user:
            return None
        return user