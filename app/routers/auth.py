from fastapi import APIRouter, Request, Response, status
from dishka.integrations.fastapi import inject, FromDishka
from app.auth.auth_service import AuthService, AuthUtils
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserIn, UserOut
from app.exceptions import UserAlreadyExistsException, UserNotFoundException
from datetime import datetime
from fastapi.responses import JSONResponse

auth_router: APIRouter = APIRouter(tags=['Авторизация и Аутентификация'])



@auth_router.post(
        '/register', 
        status_code=status.HTTP_201_CREATED,
        description='Эндпоинт для регистрации пользователя',
)
@inject
async def register(
        user: UserIn,
        user_repository: FromDishka[UserRepository],
        auth_utils: FromDishka[AuthUtils],
) -> UserOut | None:
    exist_user: User = await user_repository.find_one_or_none(username=user.username)
    
    if exist_user:
        raise UserAlreadyExistsException()
    
    current_date_time: datetime = datetime.now()

    hashed_password: str = auth_utils.get_password_hash(user.password)

    new_user: User = await user_repository.add(
        **user.model_dump(exclude="password"),
        hashed_password=hashed_password,
        registered_at=current_date_time,
    )
    return UserOut.model_validate(new_user)



@auth_router.post(
        '/login', 
        status_code=status.HTTP_200_OK,
        description='Эндпоинт для аутентификации пользователя'
)
@inject
async def login_user(
    response: Response,
    user: UserIn,
    auth_service: FromDishka[AuthService],
    auth_utils: FromDishka[AuthUtils],
) -> str:

    user: UserOut | None = await auth_service.authenticate_user(
        username=user.username, 
        password=user.password
    )

    if not user:
        raise UserNotFoundException()

    access_token: str = auth_utils.create_access_token({"sub": str(user.id)})

    response.set_cookie(
        'user_access_token', access_token, httponly=True,
    )
    return access_token




@auth_router.post(
        '/logout', 
        status_code=status.HTTP_200_OK,
        description='Эндпоинт для выходиа из системы'
)
async def logout_user(
    response: Response,
    request: Request,
) -> JSONResponse:
    
    cookies: str | None = request.cookies.get('user_access_token')
    if cookies:
        response.delete_cookie(key='user_access_token')
    return JSONResponse(content={'detail': 'success logout'})