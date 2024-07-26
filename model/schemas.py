from pydantic import BaseModel


# login
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# user type
class UserTypeAddRequest(BaseModel):
    name: str


class UserTypeInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# user
class UserAddRequest(BaseModel):
    user_name: str
    password: str
    name: str
    user_type_id: int


class UserResponseInfo(BaseModel):
    user_name: str
    password: str
    name: str
    type: UserTypeInfo

    class Config:
        orm_mode = True


# quantity


class QuantityAddRequest(BaseModel):
    name: str


class QuantityInfoResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
