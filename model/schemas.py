from typing import List
from pydantic import BaseModel
from datetime import datetime, time


# login
class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str
    name: str


class TokenData(BaseModel):
    username: str | None = None


# user type
class UserTypeAddRequest(BaseModel):
    name: str


class UserTypeUpdateRequest(BaseModel):
    id: int
    name: str


class UserTypeInfo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# user
class UserAddRequest(BaseModel):
    user_name: str
    password: str
    name: str
    user_type_id: int
    start_work_time: time
    end_work_time: time


class UserUpdateRequest(BaseModel):
    id: int
    user_name: str
    name: str
    user_type_id: int
    start_work_time: time
    end_work_time: time

    class Config:
        from_attributes = True


class UserInfoResponse(BaseModel):
    id: int
    user_name: str
    name: str
    type: UserTypeInfo
    start_work_time: time
    end_work_time: time

    class Config:
        from_attributes = True


# quantity
class QuantityAddRequest(BaseModel):
    name: str


class QuantityInfoResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# sub category
class SubCategoryAddRequest(BaseModel):
    dom_categorie_id: int
    sub_categorie_id: int


class CategoryInfoBase(BaseModel):
    id: int
    name: str


class SubCategoryInfoResponse(BaseModel):
    # dom: CategoryInfoBase
    sub: CategoryInfoBase


# category
class CategoryAddRequest(BaseModel):
    name: str


class CategoryInfoResponse(BaseModel):
    id: int
    name: str
    dom_categorie: List[SubCategoryInfoResponse]


# item
class ItemAddRequest(BaseModel):
    name: str
    count: int
    limit: int
    quantity_id: int
    categorie_id: int


class ItemInfoResponse(BaseModel):
    id: int
    name: str
    count: int
    limit: int
    quantity_id: int
    quantity: QuantityInfoResponse
    categorie: CategoryInfoBase


# alert
class AlertInfoResponse(BaseModel):
    id: int
    item: ItemInfoResponse


# transaction
class TransactionAddRequest(BaseModel):
    input: bool
    amount: int
    transaction_time: datetime
    items_id: int
    user_id: int


class TransactionInfoResponse(BaseModel):
    id: int
    input: bool
    amount: int
    transaction_time: datetime
    last_amount: int
    items_id: int
    user_id: int
    user: UserInfoResponse
    item: ItemInfoResponse

    class Config:
        from_attributes = True


class TransactionItemResponse(BaseModel):
    id: int
    name: str
    count: int
    quantity_id: int
    quantity: QuantityInfoResponse
    categorie_id: int
    transactions: List[TransactionInfoResponse]


# ages
class AgesAddRequest(BaseModel):
    start_age: int
    end_age: int


class AgesInfoResponse(BaseModel):
    id: int
    start_age: int
    end_age: int

    class Config:
        from_attributes = True


# length class
class LengthAddRequest(BaseModel):
    start_length: int
    end_length: int


class LengthInfoResponse(BaseModel):
    id: int
    start_length: int
    end_length: int

    class Config:
        from_attributes = True


# weight class
class WeightAddRequest(BaseModel):
    start_weight: int
    end_weight: int


class WeightInfoResponse(BaseModel):
    id: int
    start_weight: int
    end_weight: int

    class Config:
        from_attributes = True


# location
class LocationAddRequest(BaseModel):
    description: str


class LocationInfoResponse(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True


# pool type
class PoolTypeAddRequest(BaseModel):
    description: str
    name: str


class PoolTypeInfoResponse(BaseModel):
    id: int
    description: str
    name: str

    class Config:
        from_attributes = True


# caviar breed
class CaviarBreedAddRequest(BaseModel):
    name: str
    description: str


class CaviarBreedInfoResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


# fish breed
class FishBreedAddRequest(BaseModel):
    name: str
    description: str


class FishBreedInfoResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


# fish
class FishAddRequest(BaseModel):
    birth_of_fish: datetime
    fish_breed_id: int


class FishInfoResponse(BaseModel):
    id: int
    birth_of_fish: datetime
    fish_breed: FishBreedInfoResponse

    class Config:
        from_attributes = True


# pool
class PoolAddRequest(BaseModel):
    description: str
    location_id: int
    fish_id: int
    pool_type_id: int


class PoolInfoResponse(BaseModel):
    id: int
    description: str
    location_id: int
    fish_id: int
    pool_type_id: int

    class Config:
        from_attributes = True


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
    weight_class_id: int
    length_class_id: int
    ages_id: int
    pool_id: int
    caviar_breed_id: int

    class Config:
        from_attributes = True


class CaviarPredictionRequest(BaseModel):
    age: float
    length: float


# shift
class ShiftAddRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    description: str
    user_id: int


class ShiftInfoResponse(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    description: str
    user: UserInfoResponse

    class Config:
        from_attributes = True


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
    location: LocationInfoResponse

    class Config:
        from_attributes = True


# special


class PoolFishLocationInfoResponse(BaseModel):
    fishes: List[FishInfoResponse]
    locations: List[LocationInfoResponse]
    pool_types: List[PoolTypeInfoResponse]

    class Config:
        from_attributes = True
