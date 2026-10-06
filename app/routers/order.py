from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Order, OrderItem, Cart, Product
from app.schemas import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# =========================================================
# CHECKOUT
# CREATE ORDER + ORDER ITEMS + CLEAR CART
# =========================================================

@router.post("/checkout", response_model=OrderResponse)
def checkout(
    customer_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Get all cart items for the customer
    # -----------------------------------------------------

    cart_items = (
        db.query(Cart)
        .filter(
            Cart.customer_id == customer_id
        )
        .all()
    )

    if not cart_items:

        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    # -----------------------------------------------------
    # Calculate total amount
    # -----------------------------------------------------

    total_amount = 0.0

    order_items_data = []

    for cart_item in cart_items:

        product = (
            db.query(Product)
            .filter(
                Product.product_id ==
                cart_item.product_id
            )
            .first()
        )

        if not product:

            raise HTTPException(
                status_code=404,
                detail=
                f"Product {cart_item.product_id} not found"
            )

        quantity = int(
            cart_item.quantity
        )

        price = float(
            product.price
        )

        item_total = (
            price * quantity
        )

        total_amount += item_total

        order_items_data.append({

            "product_id":
                product.product_id,

            "quantity":
                quantity,

            "price":
                price

        })

    # -----------------------------------------------------
    # Create Order
    # -----------------------------------------------------

    order = Order(

        customer_id=customer_id,

        total_amount=total_amount,

        order_date=datetime.now().strftime(
            "%Y-%m-%d"
        ),

        status="Pending"

    )

    db.add(order)

    # Generate order_id before creating OrderItems
    db.flush()

    # -----------------------------------------------------
    # Create Order Items
    # -----------------------------------------------------

    for item in order_items_data:

        order_item = OrderItem(

            order_id=
                order.order_id,

            product_id=
                item["product_id"],

            quantity=
                item["quantity"],

            price=
                item["price"]

        )

        db.add(order_item)

    # -----------------------------------------------------
    # Clear Cart
    # -----------------------------------------------------

    for cart_item in cart_items:

        db.delete(cart_item)

    # -----------------------------------------------------
    # Save everything
    # -----------------------------------------------------

    db.commit()

    db.refresh(order)

    return order


# =========================================================
# CREATE ORDER
# =========================================================

@router.post(
    "/",
    response_model=OrderResponse
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):

    order = Order(

        customer_id=
            order_data.customer_id,

        total_amount=
            order_data.total_amount,

        order_date=
            order_data.order_date,

        status=
            order_data.status

    )

    db.add(order)

    db.commit()

    db.refresh(order)

    return order


# =========================================================
# GET ORDERS
# =========================================================
# Without customer_id:
#     Returns all orders
#
# With customer_id:
#     Returns only that customer's orders
#
# Example:
#     GET /orders/?customer_id=1
# =========================================================

@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_orders(
    customer_id: int | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Order)

    if customer_id is not None:

        query = query.filter(
            Order.customer_id ==
            customer_id
        )

    orders = (
        query
        .order_by(
            Order.order_id.desc()
        )
        .all()
    )

    return orders


# =========================================================
# GET ORDER BY ID
# =========================================================

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(
            Order.order_id ==
            order_id
        )
        .first()
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# =========================================================
# UPDATE ORDER
# =========================================================

@router.put(
    "/{order_id}",
    response_model=OrderResponse
)
def update_order(
    order_id: int,
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(
            Order.order_id ==
            order_id
        )
        .first()
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.customer_id = (
        order_data.customer_id
    )

    order.total_amount = (
        order_data.total_amount
    )

    order.order_date = (
        order_data.order_date
    )

    order.status = (
        order_data.status
    )

    db.commit()

    db.refresh(order)

    return order


# =========================================================
# DELETE ORDER
# =========================================================

@router.delete(
    "/{order_id}"
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(
            Order.order_id ==
            order_id
        )
        .first()
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)

    db.commit()

    return {

        "message":
            "Order deleted successfully"

    }