from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import hashlib
import os

from app.database import get_db
from app.models import User, Customer
from app.schemas import UserRegister, UserLogin


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# JWT CONFIGURATION
# =========================================================

SECRET_KEY = "smartcart-secret-key"
ALGORITHM = "HS256"

security = HTTPBearer()


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password: str) -> str:

    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(
    password: str,
    stored_password: str
) -> bool:

    try:

        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return password_hash.hex() == hash_hex

    except Exception:

        return False


# =========================================================
# REGISTER
# =========================================================

@router.post("/register")
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # CHECK USERNAME
    # -----------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(
            User.username == user_data.username
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # -----------------------------------------------------
    # HASH PASSWORD
    # -----------------------------------------------------

    hashed_password = hash_password(
        user_data.password
    )


    # -----------------------------------------------------
    # CREATE SMARTCART CUSTOMER
    # -----------------------------------------------------

    customer_email = (
        user_data.username.strip().lower()
        + "@smartcart.com"
    )


    # Check whether generated email already exists
    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.email == customer_email
        )
        .first()
    )


    if existing_customer:

        raise HTTPException(
            status_code=400,
            detail=(
                "A SmartCart customer account already "
                "exists for this username."
            )
        )


    new_customer = Customer(

        name=user_data.username,

        email=customer_email,

        age=None,

        gender=None,

        location=None

    )


    db.add(new_customer)

    # Generate customer_id
    db.flush()


    # -----------------------------------------------------
    # CREATE USER AND LINK CUSTOMER
    # -----------------------------------------------------

    new_user = User(

        username=user_data.username,

        password_hash=hashed_password,

        role=user_data.role,

        customer_id=new_customer.customer_id

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "message":
            "User registered successfully",

        "username":
            new_user.username,

        "role":
            new_user.role,

        "customer_id":
            new_user.customer_id

    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.username == user_data.username
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    # -----------------------------------------------------
    # VERIFY PASSWORD
    # -----------------------------------------------------

    if not verify_password(
        user_data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    # -----------------------------------------------------
    # CUSTOMER LINK CHECK
    # -----------------------------------------------------

    if (
        user.role == "customer"
        and user.customer_id is None
    ):

        raise HTTPException(
            status_code=403,
            detail=(
                "This user is not linked to a "
                "SmartCart customer account."
            )
        )


    # -----------------------------------------------------
    # CREATE JWT
    # -----------------------------------------------------

    token_data = {

        "sub":
            user.username,

        "role":
            user.role,

        "customer_id":
            user.customer_id

    }


    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "access_token":
            access_token,

        "token_type":
            "bearer",

        "username":
            user.username,

        "role":
            user.role,

        "customer_id":
            user.customer_id

    }


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials =
        Depends(security),

    db: Session =
        Depends(get_db)
):

    token = credentials.credentials


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        username = payload.get("sub")


        if username is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return user


# =========================================================
# MY PROFILE
# =========================================================

@router.get("/me")
def get_my_profile(
    current_user: User =
        Depends(get_current_user)
):

    return {

        "message":
            "You are authenticated",

        "username":
            current_user.username,

        "role":
            current_user.role,

        "customer_id":
            current_user.customer_id

    }