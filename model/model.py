from model.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(999))
    password = Column(String(999))
    name = Column(String(999))
    user_type_id = Column(Integer, ForeignKey("user_types.id"))

    type = relationship("UserType", back_populates="type_users")


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
    items_id = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="transactions")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(999))
    count = Column(Integer)
    quantity_id = Column(Integer, ForeignKey("quantities.id"))
    categorie_id = Column(Integer, ForeignKey("categories.id"))

    transactions = relationship("Transaction", back_populates="item")

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


class LengthClass(Base):
    __tablename__ = "length_classes"

    id = Column(Integer, primary_key=True, index=True)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)


class PoolType(Base):
    __tablename__ = "pool_types"

    id = Column(Integer, primary_key=True, index=True)


class CaviarBredd(Base):
    __tablename__ = "caviar_breeds"

    id = Column(Integer, primary_key=True, index=True)


class WeightClass(Base):
    __tablename__ = "weight_classes"

    id = Column(Integer, primary_key=True, index=True)


class FishType(Base):
    __tablename__ = "fish_type"

    id = Column(Integer, primary_key=True, index=True)


class Fishes(Base):
    __tablename__ = "fishes"

    id = Column(Integer, primary_key=True, index=True)


class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)


class Caviar(Base):
    __tablename__ = "caviars"

    id = Column(Integer, primary_key=True, index=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)


class Shift(Base):
    __tablename__ = "Shifts"

    id = Column(Integer, primary_key=True, index=True)


class A_________(Base):
    __tablename__ = "A________"

    id = Column(Integer, primary_key=True, index=True)
