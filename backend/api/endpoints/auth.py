from datetime import datetime, timedelta
from typing import Annotated

# from api.endpoints.auth import get_current_user
from core.config import settings
from db.session import SessionLocal, get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import Users
from passlib.context import CryptContext

# Import schemas
from schemas.auth_schema import TokenPayload, TokenSchema, UserAuth
from schemas.user_schema import CreateUserRequest, UserResponse
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(db: db_dependency, user_create: CreateUserRequest):
    create_user_model = Users(
        username=user_create.username,
        hashed_password=bcrypt_context.hash(user_create.password),
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)  # To fetch the generated ID

    return create_user_model


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user_auth = UserAuth(username=form_data.username, password=form_data.password)
    user = authenticate_user(user_auth, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(user_auth: UserAuth, db: Session):
    user = db.query(Users).filter(Users.username == user_auth.username).first()
    if not user or not bcrypt_context.verify(user_auth.password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = TokenPayload(
        sub=username,
        id=user_id,
        exp=int((datetime.utcnow() + expires_delta).timestamp()),
    )
    return jwt.encode(
        payload.dict(exclude_none=True),
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if token_data.sub is None or token_data.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": token_data.sub, "id": token_data.id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
