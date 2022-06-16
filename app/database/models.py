from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
)

Base = declarative_base()


class Deliveryman(Base):
    __tablename__ = "deliveryman"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    vehicle = Column(String(50))


class Buyer(Base):
    __tablename__ = "buyer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    cpf = Column(String(11))
    cep = Column(String(8))
    address_number = Column(Integer)
    address_lat = Column(Float)
    address_long = Column(Float)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    value = Column(Float)
    quant = Column(Integer)


class Delivery(Base):
    __tablename__ = "delivery"
    id = Column(Integer, primary_key=True, index=True)
    id_buyer = Column(Integer)
    id_product = Column(Integer)
    id_deliveryman = Column(Integer)
    deliveryman_lat = Column(Float)
    deliveryman_long = Column(Float)
    receiver_cpf = Column(String(11))
    status_delivery = Column(String(50))
