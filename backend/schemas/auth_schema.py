from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None
    id: int | None = None
    exp: int | None = None


class UserAuth(BaseModel):
    username: str
    password: str
