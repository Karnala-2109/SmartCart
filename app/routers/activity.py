from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CustomerActivity
from app.schemas import (
    CustomerActivityCreate,
    CustomerActivityResponse
)


router = APIRouter(
    prefix="/activity",
    tags=["Customer Activity"]
)


@router.post(
    "/",
    response_model=CustomerActivityResponse
)
def create_activity(
    activity_data: CustomerActivityCreate,
    db: Session = Depends(get_db)
):
    activity = CustomerActivity(
        customer_id=activity_data.customer_id,
        product_id=activity_data.product_id,
        website_visits=activity_data.website_visits,
        product_views=activity_data.product_views,
        cart_additions=activity_data.cart_additions,
        wishlist_additions=activity_data.wishlist_additions,
        time_spent=activity_data.time_spent
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


@router.get(
    "/",
    response_model=list[CustomerActivityResponse]
)
def get_activities(
    db: Session = Depends(get_db)
):
    activities = db.query(CustomerActivity).all()
    return activities


@router.get(
    "/{activity_id}",
    response_model=CustomerActivityResponse
)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = (
        db.query(CustomerActivity)
        .filter(
            CustomerActivity.activity_id == activity_id
        )
        .first()
    )

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    return activity


@router.put(
    "/{activity_id}",
    response_model=CustomerActivityResponse
)
def update_activity(
    activity_id: int,
    activity_data: CustomerActivityCreate,
    db: Session = Depends(get_db)
):
    activity = (
        db.query(CustomerActivity)
        .filter(
            CustomerActivity.activity_id == activity_id
        )
        .first()
    )

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    activity.customer_id = activity_data.customer_id
    activity.product_id = activity_data.product_id
    activity.website_visits = activity_data.website_visits
    activity.product_views = activity_data.product_views
    activity.cart_additions = activity_data.cart_additions
    activity.wishlist_additions = activity_data.wishlist_additions
    activity.time_spent = activity_data.time_spent

    db.commit()
    db.refresh(activity)

    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = (
        db.query(CustomerActivity)
        .filter(
            CustomerActivity.activity_id == activity_id
        )
        .first()
    )

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    db.delete(activity)
    db.commit()

    return {
        "message": "Activity deleted successfully"
    }