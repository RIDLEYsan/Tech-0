import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Product API"}


@app.on_event("startup")
def startup_event():
    db = next(get_db())
    test_product_code = "123456"
    existing_product = (
        db.query(models.Product)
        .filter(models.Product.code == test_product_code)
        .first()
    )
    if existing_product is None:
        test_product = models.Product(
            code=test_product_code, name="Test Product", price=9.99
        )
        db.add(test_product)
        db.commit()
        logger.info("Test product added to database")
    else:
        logger.info("Test product already exists in database")

    # データベースの状態を確認
    products = db.query(models.Product).all()
    logger.info(f"Current products in database: {[(p.code, p.name) for p in products]}")


@app.get("/api/products/{barcode}", response_model=schemas.Product)
def get_product(barcode: str, db: Session = Depends(get_db)):
    logger.info(f"Searching for product with barcode: {barcode}")
    try:
        product = (
            db.query(models.Product).filter(models.Product.code == barcode).first()
        )
        if product is None:
            logger.warning(f"Product with barcode {barcode} not found")
            raise HTTPException(
                status_code=404, detail=f"Product with barcode {barcode} not found"
            )
        logger.info(f"Product found: {product.name}")
        return product
    except Exception as e:
        logger.error(f"An error occurred while fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/api/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new product: {product.name}")
    try:
        db_product = models.Product(
            code=product.code, name=product.name, price=product.price
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Product created successfully: {db_product.name}")
        return db_product
    except Exception as e:
        logger.error(f"An error occurred while creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/api/purchase/")
def purchase_products(
    purchase_items: List[schemas.ProductPurchase], db: Session = Depends(get_db)
):
    try:
        total_amount = sum(item.price * item.quantity for item in purchase_items)
        new_transaction = models.Transaction(total_amt=total_amount)
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        for item in purchase_items:
            product = (
                db.query(models.Product)
                .filter(models.Product.code == item.code)
                .first()
            )
            if product:
                transaction_detail = models.TransactionDetail(
                    trd_id=new_transaction.trd_id,
                    prd_id=product.id,
                    prd_code=product.code,
                    prd_name=product.name,
                    prd_price=product.price,
                )
                db.add(transaction_detail)
            else:
                raise HTTPException(
                    status_code=404, detail=f"Product with code {item.code} not found"
                )

        db.commit()
        return {"message": "Purchase recorded successfully"}
    except Exception as e:
        logger.error(f"An error occurred while recording purchase: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
