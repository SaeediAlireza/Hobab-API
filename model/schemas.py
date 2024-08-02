from pydantic import BaseModel
from datetime import datetime, time


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
    start_work_time: time
    end_work_time: time


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
class AgesAddReqest(BaseModel):
    start_age: int
    end_age: int


class AgesInfoResponse(BaseModel):
    id: int
    start_age: int
    end_age: int

    class Config:
        orm_mode = True


# length class


class LenghtAddReqest(BaseModel):
    start_lenght: int
    end_lenght: int


class LenghtInfoResponse(BaseModel):
    id: int
    start_lenght: int
    end_lenght: int

    class Config:
        orm_mode = True


# weight class


class WeightAddReqest(BaseModel):
    start_weight: int
    end_weight: int


class WeightInfoResponse(BaseModel):
    id: int
    start_weight: int
    end_weight: int

    class Config:
        orm_mode = True


# location


class LocationAddReqest(BaseModel):
    description: str


class LocationInfoResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True


# pool type


class PoolTypeAddReqest(BaseModel):
    description: str


class PoolTypeInfoResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True


# caviar breed


class CaviarBreedAddReqest(BaseModel):
    name: str


class CaviarBreedInfoResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# fish breed


class FishBreedAddReqest(BaseModel):
    name: str


class FishBreedInfoResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# fish


class FishAddReqest(BaseModel):
    birth_of_fish: datetime
    fish_breed_id: int


class FishInfoResponse(BaseModel):
    id: int
    birth_of_fish: datetime
    fish_breed: FishBreedInfoResponse

    class Config:
        orm_mode = True


# pool


class PoolAddReqest(BaseModel):
    birth_of_fish: datetime
    fish_breed_id: int


class PoolInfoResponse(BaseModel):
    id: int
    birth_of_fish: datetime
    fish_breed: FishBreedInfoResponse

    class Config:
        orm_mode = True


# caviar


class CaviarAddReqest(BaseModel):
    weight: int
    lenght: int
    time_of_birth: datetime
    weight_class_id: int
    length_class_id: int
    ages_id: int
    pool_id: int
    caviar_breed_id: int


class CaviarInfoResponse(BaseModel):
    id: int
    weight: int
    lenght: int
    time_of_birth: datetime
    weight_class_id: WeightInfoResponse
    length_class_id: LenghtInfoResponse
    ages_id: AgesInfoResponse
    pool_id: PoolInfoResponse
    caviar_breed_id: CaviarBreedInfoResponse

    class Config:
        orm_mode = True


# shift

# task
