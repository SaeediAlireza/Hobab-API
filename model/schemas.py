from pydantic import BaseModel
from datetime import datetime


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


# category
class CategoryAddRequest(BaseModel):
    name: str


# sub category


class SubCategoryAddRequest(BaseModel):
    dom_categorie_id: int
    sub_categorie_id: int


# item


class ItemAddRequest(BaseModel):
    name: str
    count: int
    quantity_id: int
    category_id: int


# transaction


class TransactionAddReqest(BaseModel):
    input: bool
    amount: int
    transaction_time: datetime
    item_id: int


class TransactionInfoResponse(BaseModel):
    id: int
    input: bool
    amount: int
    transaction_time: datetime
    item_id: int

    class Config:
        orm_mode = True


# ages

# length class

# weight class

# location

# pool type

# caviar breed

# fish type

# fish

# pool

# caviar

# shift

# task
