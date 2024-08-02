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


class UserInfoResponse(BaseModel):
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


class TransactionAddRequest(BaseModel):
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
class AgesAddRequest(BaseModel):
    start_age: int
    end_age: int


class AgesInfoResponse(BaseModel):
    id: int
    start_age: int
    end_age: int

    class Config:
        orm_mode = True


# length class


class LengthAddRequest(BaseModel):
    start_length: int
    end_length: int


class LengthInfoResponse(BaseModel):
    id: int
    start_length: int
    end_lentgth: int

    class Config:
        orm_mode = True


# weight class


class WeightAddRequest(BaseModel):
    start_weight: int
    end_weight: int


class WeightInfoResponse(BaseModel):
    id: int
    start_weight: int
    end_weight: int

    class Config:
        orm_mode = True


# location


class LocationAddRequest(BaseModel):
    description: str


class LocationInfoResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True


# pool type


class PoolTypeAddRequest(BaseModel):
    description: str


class PoolTypeInfoResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True


# caviar breed


class CaviarBreedAddRequest(BaseModel):
    name: str


class CaviarBreedInfoResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# fish breed


class FishBreedAddRequest(BaseModel):
    name: str


class FishBreedInfoResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# fish


class FishAddRequest(BaseModel):
    birth_of_fish: datetime
    fish_breed_id: int


class FishInfoResponse(BaseModel):
    id: int
    birth_of_fish: datetime
    fish_breed: FishBreedInfoResponse

    class Config:
        orm_mode = True


# pool


class PoolAddRequest(BaseModel):
    birth_of_fish: datetime
    fish_breed_id: int


class PoolInfoResponse(BaseModel):
    id: int
    birth_of_fish: datetime
    fish_breed: FishBreedInfoResponse

    class Config:
        orm_mode = True


# caviar


class CaviarAddRequest(BaseModel):
    weight: int
    length: int
    time_of_birth: datetime
    weight_class_id: int
    length_class_id: int
    ages_id: int
    pool_id: int
    caviar_breed_id: int


class CaviarInfoResponse(BaseModel):
    id: int
    weight: int
    length: int
    time_of_birth: datetime
    weight_class_id: WeightInfoResponse
    length_class_id: LengthInfoResponse
    ages_id: AgesInfoResponse
    pool_id: PoolInfoResponse
    caviar_breed_id: CaviarBreedInfoResponse

    class Config:
        orm_mode = True


# shift


class ShiftAddRequest(BaseModel):
    start_time: time
    end_time: time
    description: str
    user_id: int


class ShiftInfoResponse(BaseModel):
    id: int
    start_time: time
    end_time: time
    description: str
    user: UserInfoResponse

    class Config:
        orm_mode = True


# task


class TaskAddRequest(BaseModel):
    description: str
    shift_id: int
    pool_id: int
    Location_id: int


class TaskInfoResponse(BaseModel):
    id: int
    description: str
    shift: ShiftInfoResponse
    pool: PoolInfoResponse
    Location: LocationInfoResponse

    class Config:
        orm_mode = True
