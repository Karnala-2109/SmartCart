from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Wishlist
from app.schemas import WishlistCreate, WishlistResponse


router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


@router.post("/", response_model=WishlistResponse)
def create_wishlist_item(
    wishlist_data: WishlistCreate,
    db: Session = Depends(get_db)
):
    wishlist_item = Wishlist(
        customer_id=wishlist_data.customer_id,
        product_id=wishlist_data.product_id
    )

    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)

    return wishlist_item


@router.get("/", response_model=list[WishlistResponse])
def get_wishlist_items(
    db: Session = Depends(get_db)
):
    wishlist_items = db.query(Wishlist).all()
    return wishlist_items


@router.get(
    "/{wishlist_id}",
    response_model=WishlistResponse
)
def get_wishlist_item(
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    wishlist_item = (
        db.query(Wishlist)
        .filter(Wishlist.wishlist_id == wishlist_id)
        .first()
    )

    if not wishlist_item:
        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found"
        )

    return wishlist_item


@router.put(
    "/{wishlist_id}",
    response_model=WishlistResponse
)
def update_wishlist_item(
    wishlist_id: int,
    wishlist_data: WishlistCreate,
    db: Session = Depends(get_db)
):
    wishlist_item = (
        db.query(Wishlist)
        .filter(Wishlist.wishlist_id == wishlist_id)
        .first()
    )

    if not wishlist_item:
        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found"
        )

    wishlist_item.customer_id = wishlist_data.customer_id
    wishlist_item.product_id = wishlist_data.product_id

    db.commit()
    db.refresh(wishlist_item)

    return wishlist_item


@router.delete("/{wishlist_id}")
def delete_wishlist_item(
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    wishlist_item = (
        db.query(Wishlist)
        .filter(Wishlist.wishlist_id == wishlist_id)
        .first()
    )

    if not wishlist_item:
        raise HTTPException(
            status_code=404,
            detail="Wishlist item not found"
        )

    db.delete(wishlist_item)
    db.commit()

    return {
        "message": "Wishlist item deleted successfully"
    }