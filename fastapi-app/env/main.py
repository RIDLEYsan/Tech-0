from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Integer)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/products/{barcode}")
def get_product(barcode: str):
    db = SessionLocal()
    product = db.query(Product).filter(Product.code == barcode).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
