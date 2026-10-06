from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer
from app.schemas import CustomerCreate, CustomerResponse


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# ==========================================
# CREATE CUSTOMER
# ==========================================

@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing_customer = (
        db.query(Customer)
        .filter(Customer.email == customer_data.email)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        age=customer_data.age,
        gender=customer_data.gender,
        location=customer_data.location
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


# ==========================================
# GET ALL CUSTOMERS
# ==========================================

@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db)
):

    customers = db.query(Customer).all()

    return customers


# ==========================================
# GET CUSTOMER BY ID
# ==========================================

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# ==========================================
# UPDATE CUSTOMER
# ==========================================

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.age = customer_data.age
    customer.gender = customer_data.gender
    customer.location = customer_data.location

    db.commit()
    db.refresh(customer)

    return customer


# ==========================================
# DELETE CUSTOMER
# ==========================================

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }