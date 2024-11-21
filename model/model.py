from model.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Time
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(999))
    password = Column(String(999))
    name = Column(String(999))
    user_type_id = Column(Integer, ForeignKey("user_types.id"))
    start_work_time = Column(Time)
    end_work_time = Column(Time)

    type = relationship("UserType", back_populates="type_users")

    shifts = relationship("Shift", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class UserType(Base):

    __tablename__ = "user_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))

    type_users = relationship("User", back_populates="type")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    input = Column(Boolean)
    amount = Column(Integer)
    transaction_time = Column(DateTime)
    last_amount = Column(Integer)
    items_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    item = relationship("Item", back_populates="transactions")
    user = relationship("User", back_populates="transactions")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    seen = Column(Boolean)  # NOT DONE
    alert_time = Column(DateTime)
    item_id = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="alerts")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))
    count = Column(Integer)
    limit = Column(Integer)  # NOT DONE
    quantity_id = Column(Integer, ForeignKey("quantities.id"))
    categorie_id = Column(Integer, ForeignKey("categories.id"))

    transactions = relationship("Transaction", back_populates="item")
    alerts = relationship("Alert", back_populates="item")

    quantity = relationship("Quantity", back_populates="items")
    categorie = relationship("Categorie", back_populates="items")


class SubCategorie(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, index=True)
    dom_categorie_id = Column(Integer, ForeignKey("categories.id"))
    sub_categorie_id = Column(Integer, ForeignKey("categories.id"))

    dom = relationship(
        "Categorie", back_populates="dom_categorie", foreign_keys=[dom_categorie_id]
    )
    sub = relationship(
        "Categorie", back_populates="sub_categorie", foreign_keys=[sub_categorie_id]
    )


class Categorie(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))

    items = relationship("Item", back_populates="categorie")

    dom_categorie = relationship(
        "SubCategorie",
        back_populates="dom",
        foreign_keys="SubCategorie.dom_categorie_id",
    )
    sub_categorie = relationship(
        "SubCategorie",
        back_populates="sub",
        foreign_keys="SubCategorie.sub_categorie_id",
    )


class Quantity(Base):
    __tablename__ = "quantities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))

    items = relationship("Item", back_populates="quantity")


class Ages(Base):
    __tablename__ = "ageses"

    id = Column(Integer, primary_key=True, index=True)
    start_age = Column(Integer)
    end_age = Column(Integer)

    caviars = relationship("Caviar", back_populates="ages")


class LengthClass(Base):
    __tablename__ = "length_classes"

    id = Column(Integer, primary_key=True, index=True)
    start_length = Column(Integer)
    end_length = Column(Integer)

    caviars = relationship("Caviar", back_populates="length_class")


class WeightClass(Base):
    __tablename__ = "weight_classes"

    id = Column(Integer, primary_key=True, index=True)
    start_weight = Column(Integer)
    end_weight = Column(Integer)

    caviars = relationship("Caviar", back_populates="weight_class")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(999))

    pools = relationship("Pool", back_populates="location")
    tasks = relationship("Task", back_populates="location")


class PoolType(Base):
    __tablename__ = "pool_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))
    description = Column(String(999))

    pools = relationship("Pool", back_populates="pool_type")


class CaviarBreed(Base):
    __tablename__ = "caviar_breeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))
    description = Column(String(999))

    caviars = relationship("Caviar", back_populates="caviar_breed")


class FishBreed(Base):
    __tablename__ = "fish_breeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))
    description = Column(String(999))

    fishes = relationship("Fish", back_populates="fish_breed")


class Fish(Base):
    __tablename__ = "fishes"

    id = Column(Integer, primary_key=True, index=True)
    birth_of_fish = Column(DateTime)
    fish_breed_id = Column(Integer, ForeignKey("fish_breeds.id"))

    fish_breed = relationship("FishBreed", back_populates="fishes")
    pools = relationship("Pool", back_populates="fish")


class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(999))
    location_id = Column(Integer, ForeignKey("locations.id"))
    fish_id = Column(Integer, ForeignKey("fishes.id"))
    pool_type_id = Column(Integer, ForeignKey("pool_types.id"))

    location = relationship("Location", back_populates="pools")
    fish = relationship("Fish", back_populates="pools")
    pool_type = relationship("PoolType", back_populates="pools")

    caviars = relationship("Caviar", back_populates="pool")
    tasks = relationship("Task", back_populates="pool")


class Caviar(Base):
    __tablename__ = "caviars"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer)
    length = Column(Integer)
    time_of_birth = Column(DateTime)
    weight_class_id = Column(Integer, ForeignKey("weight_classes.id"))
    length_class_id = Column(Integer, ForeignKey("length_classes.id"))
    ages_id = Column(Integer, ForeignKey("ageses.id"))
    pool_id = Column(Integer, ForeignKey("pools.id"))
    caviar_breed_id = Column(Integer, ForeignKey("caviar_breeds.id"))

    weight_class = relationship("WeightClass", back_populates="caviars")
    length_class = relationship("LengthClass", back_populates="caviars")
    ages = relationship("Ages", back_populates="caviars")
    pool = relationship("Pool", back_populates="caviars")
    caviar_breed = relationship("CaviarBreed", back_populates="caviars")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    description = Column(String(999))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="shifts")

    tasks = relationship("Task", back_populates="shift")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(999))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    pool_id = Column(Integer, ForeignKey("pools.id"))
    Location_id = Column(Integer, ForeignKey("locations.id"))

    shift = relationship("Shift", back_populates="tasks")
    pool = relationship("Pool", back_populates="tasks")
    location = relationship("Location", back_populates="tasks")
