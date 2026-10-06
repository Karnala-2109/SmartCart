from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import OrderItem
from app.schemas import OrderItemCreate, OrderItemResponse


router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)


# ==========================================
# CREATE ORDER ITEM
# ==========================================

@router.post("/", response_model=OrderItemResponse)
def create_order_item(
    order_item_data: OrderItemCreate,
    db: Session = Depends(get_db)
):

    order_item = OrderItem(
        order_id=order_item_data.order_id,
        product_id=order_item_data.product_id,
        quantity=order_item_data.quantity,
        price=order_item_data.price
    )

    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    return order_item


# ==========================================
# GET ALL ORDER ITEMS
# ==========================================

@router.get("/", response_model=list[OrderItemResponse])
def get_order_items(
    db: Session = Depends(get_db)
):

    order_items = db.query(OrderItem).all()

    return order_items


# ==========================================
# GET ORDER ITEM BY ID
# ==========================================

@router.get(
    "/{order_item_id}",
    response_model=OrderItemResponse
)
def get_order_item(
    order_item_id: int,
    db: Session = Depends(get_db)
):

    order_item = (
        db.query(OrderItem)
        .filter(OrderItem.order_item_id == order_item_id)
        .first()
    )

    if not order_item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    return order_item


# ==========================================
# UPDATE ORDER ITEM
# ==========================================

@router.put(
    "/{order_item_id}",
    response_model=OrderItemResponse
)
def update_order_item(
    order_item_id: int,
    order_item_data: OrderItemCreate,
    db: Session = Depends(get_db)
):

    order_item = (
        db.query(OrderItem)
        .filter(OrderItem.order_item_id == order_item_id)
        .first()
    )

    if not order_item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    order_item.order_id = order_item_data.order_id
    order_item.product_id = order_item_data.product_id
    order_item.quantity = order_item_data.quantity
    order_item.price = order_item_data.price

    db.commit()
    db.refresh(order_item)

    return order_item


# ==========================================
# DELETE ORDER ITEM
# ==========================================

@router.delete("/{order_item_id}")
def delete_order_item(
    order_item_id: int,
    db: Session = Depends(get_db)
):

    order_item = (
        db.query(OrderItem)
        .filter(OrderItem.order_item_id == order_item_id)
        .first()
    )

    if not order_item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    db.delete(order_item)
    db.commit()

    return {
        "message": "Order item deleted successfully"
    }