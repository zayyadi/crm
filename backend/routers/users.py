from fastapi.responses import JSONResponse
from datetime import timedelta

from pydantic import EmailStr
from app.models.models import User
from starlette.responses import Response as resp
from app.schemas.schemas import (
    PasswordReset,
    UserCreate,
    UserRead,
    UserLogin,
    UserUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from routers.mail import send_mail
from app.auth.auth import (
    validate_user,
    create_access_token,
    get_user,
    hash,
    expire_time,
    client,
    OAuth2PasswordBearerCookie,
    verify_password,
)
import os


router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


@router.post(
    "/register",
    response_model=UserRead,
)
async def create_user(user: UserCreate):
    hashed_password = verify_password(user.password)
    user.password = hashed_password
    user = await User.create(**user.dict())
    return user


async def get_user_by_email(email: str):
    email = await User.get_email(email)
    return email


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    user_data = {}
    user_data["data"] = user

    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)

    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "message": "User Logged in Successfully.",
        "data": user_data,
        "status": status.HTTP_200_OK,
    }


@router.post("/token")
async def token(user: UserLogin):
    try:
        users = await get_user(user.email)

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, users.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=expire_time)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    user_data = {}

    user_data["data"] = users

    # user_log = models.
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        os.getenv("TOKEN_NAME"),
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "message": "User Logged in Successfully.",
        "data": user_data,
        "orgid": users.orgid,
        "status": status.HTTP_200_OK,
    }


security = OAuth2PasswordBearer(tokenUrl="/auth/login")
security2 = OAuth2PasswordBearerCookie(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.get_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(*roles):
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return role_checker


router.patch(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)


async def update_user_password(
    id: str,
    user_schema: UserUpdate,
    current_user: int = Depends(get_current_user),
):
    hashed_password = hash(user_schema.password)
    user_schema.password = hashed_password
    user = await User.update(id=id, **user_schema.dict())
    return {
        "status": status.HTTP_202_ACCEPTED,
        "message": "user updated successfully!",
    }


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    id: EmailStr,
    # request: Request,
    response: Response,
):
    try:
        user = await User.delete_by_email(email=id)
        if user == 0:
            raise HTTPException(status_code=404, detail="Record not found")
    except HTTPException as e:
        raise
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, "orig") else f"{e}",
        }
    response.status_code = status.HTTP_204_NO_CONTENT
    return {"message": "SUccessfully deleted"}


@router.post("/send_token")
async def send_token(
    email: EmailStr,
):
    user = await User.get_email(email=email)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {email} not found")
    # token = await send_mail(email)
    token_response = await send_mail(email)
    token = token_response.body

    return {"token": token}


@router.post("/password_reset")
async def reset_password(
    email: EmailStr,
    otp: str,
    password_schema: PasswordReset,
):
    key = f"{email}otp"
    cached_data = client.get(key)

    if cached_data:
        data = cached_data.decode("utf-8")
        if otp == data:
            hashed_password = hash(password_schema.password)
            password_schema.password = hashed_password
            # filtered_dict = {key: value for key, value in password_schema.dict().items() if key != password_schema.confirm_password}
            user = await User.update_by_email(
                email=email, **password_schema.dict(exclude_unset=True)
            )
            # password_dict = password_schema.dict(exclude_unset=True)
            # user = await models.get_email(email)
            # for key, value in password_schema.items():
            #     setattr(user, key, value)
            return {"message": "Password changed successfully"}

    raise HTTPException(status_code=401, detail="Invalid OTP or expired token")


@router.get("/logout/")
async def logout(response: resp):
    responses = JSONResponse(content={"message": "Logged out successfully"})
    # response = responses.RedirectResponse(url="/auth/login", status_code=302)

    response.delete_cookie(
        key=os.getenv("TOKEN_NAME"),
    )

    return responses
