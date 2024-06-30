from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(13), unique=True, index=True)
    name = Column(String(50))
    price = Column(Integer)


class Transaction(Base):
    __tablename__ = "transactions"

    trd_id = Column(Integer, primary_key=True, index=True)
    datetime = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    emp_cd = Column(String(10))
    store_cd = Column(String(5))
    pos_no = Column(String(3))
    total_amt = Column(Integer)


class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    trd_id = Column(Integer, ForeignKey("transactions.trd_id"), primary_key=True)
    dtl_id = Column(Integer, primary_key=True, autoincrement=True)
    prd_id = Column(Integer, ForeignKey("products.id"))
    prd_code = Column(String(13))
    prd_name = Column(String(50))
    prd_price = Column(Integer)
