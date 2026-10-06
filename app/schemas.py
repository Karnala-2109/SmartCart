from pydantic import BaseModel, Field


# ========================================
# Authentication Schemas
# ========================================

class UserRegister(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=6
    )

    role: str = "customer"


class UserLogin(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=6
    )


# ========================================
# Customer Schemas
# ========================================

class CustomerCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: str

    age: int = Field(
        ge=18,
        le=100
    )

    gender: str

    location: str


class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    age: int
    gender: str
    location: str

    class Config:
        from_attributes = True
        
        # ========================================
# Product Schemas
# ========================================

class ProductCreate(BaseModel):
    product_name: str = Field(
        min_length=2,
        max_length=100
    )

    category: str = Field(
        min_length=2,
        max_length=50
    )

    price: float = Field(
        gt=0
    )

    rating: float = Field(
        ge=0,
        le=5
    )

    stock: int = Field(
        ge=0
    )


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    category: str
    price: float
    rating: float
    stock: int

    class Config:
        from_attributes = True
       
 # ========================================
# Order Schemas
# ========================================

class OrderCreate(BaseModel):
    customer_id: int = Field(
        gt=0
    )

    total_amount: float = Field(
        ge=0
    )

    order_date: str

    status: str = Field(
        min_length=2,
        max_length=30
    )


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    total_amount: float
    order_date: str
    status: str

    class Config:
        from_attributes = True
        # ========================================
# Order Item Schemas
# ========================================

class OrderItemCreate(BaseModel):
    order_id: int = Field(
        gt=0
    )

    product_id: int = Field(
        gt=0
    )

    quantity: int = Field(
        gt=0
    )

    price: float = Field(
        ge=0
    )


class OrderItemResponse(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True
        # ========================================
# Cart Schemas
# ========================================

class CartCreate(BaseModel):
    customer_id: int = Field(
        gt=0
    )

    product_id: int = Field(
        gt=0
    )

    quantity: int = Field(
        gt=0
    )


class CartResponse(BaseModel):
    cart_id: int
    customer_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
        # ========================================
# Wishlist Schemas
# ========================================

class WishlistCreate(BaseModel):
    customer_id: int = Field(
        gt=0
    )

    product_id: int = Field(
        gt=0
    )


class WishlistResponse(BaseModel):
    wishlist_id: int
    customer_id: int
    product_id: int

    class Config:
        from_attributes = True
        # ========================================
# Customer Activity Schemas
# ========================================

class CustomerActivityCreate(BaseModel):
    customer_id: int = Field(
        gt=0
    )

    product_id: int = Field(
        gt=0
    )

    website_visits: int = Field(
        ge=0
    )

    product_views: int = Field(
        ge=0
    )

    cart_additions: int = Field(
        ge=0
    )

    wishlist_additions: int = Field(
        ge=0
    )

    time_spent: int = Field(
        ge=0
    )


class CustomerActivityResponse(BaseModel):
    activity_id: int
    customer_id: int
    product_id: int
    website_visits: int
    product_views: int
    cart_additions: int
    wishlist_additions: int
    time_spent: int

    class Config:
        from_attributes = True