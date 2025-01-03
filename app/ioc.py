from typing import AsyncIterator

from dishka import Provider, Scope, provide, from_context
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.user import User
from app.repositories.user import UserRepository
from app.config import Config
from app.db.postgres import new_session_maker
from app.auth.auth_service import AuthService, AuthUtils
from app.exceptions import TokenAbsentException


class AppProvider(Provider):
    config: Config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(model=User, session=session)
    
    @provide(scope=Scope.APP)
    def get_auth_utils(self, config: Config) -> AuthUtils:
        return AuthUtils(config=config.jwt)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_repository: UserRepository, auth_utils: AuthUtils) -> AuthService:
        return AuthService(user_repository=user_repository, auth_utils=auth_utils)

    @provide(scope=Scope.REQUEST)
    def get_token(self, request: Request) -> str:
        token: str = request.cookies.get("user_access_token")
        if not token:
            raise TokenAbsentException()
        return token

    @provide(scope=Scope.REQUEST)
    async def get_current_user_dependency(
        self,
        auth_service: AuthService,
        token: str,
    ) -> User | None:
        return await auth_service.get_current_user(token=token)