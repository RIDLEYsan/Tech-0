from pydantic import BaseModel


class ProductBase(BaseModel):
    code: str
    name: str
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductPurchase(BaseModel):
    code: str
    quantity: int
