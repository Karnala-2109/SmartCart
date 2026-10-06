from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cart
from app.schemas import CartCreate, CartResponse


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/", response_model=CartResponse)
def create_cart_item(
    cart_data: CartCreate,
    db: Session = Depends(get_db)
):
    cart_item = Cart(
        customer_id=cart_data.customer_id,
        product_id=cart_data.product_id,
        quantity=cart_data.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.get("/", response_model=list[CartResponse])
def get_cart_items(
    db: Session = Depends(get_db)
):
    cart_items = db.query(Cart).all()
    return cart_items


@router.get(
    "/{cart_id}",
    response_model=CartResponse
)
def get_cart_item(
    cart_id: int,
    db: Session = Depends(get_db)
):
    cart_item = (
        db.query(Cart)
        .filter(Cart.cart_id == cart_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    return cart_item


@router.put(
    "/{cart_id}",
    response_model=CartResponse
)
def update_cart_item(
    cart_id: int,
    cart_data: CartCreate,
    db: Session = Depends(get_db)
):
    cart_item = (
        db.query(Cart)
        .filter(Cart.cart_id == cart_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.customer_id = cart_data.customer_id
    cart_item.product_id = cart_data.product_id
    cart_item.quantity = cart_data.quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.delete("/{cart_id}")
def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db)
):
    cart_item = (
        db.query(Cart)
        .filter(Cart.cart_id == cart_id)
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Cart item deleted successfully"
    }