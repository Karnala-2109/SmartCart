from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    customer,
    product,
    order,
    order_item,
    cart,
    wishlist,
    activity,
    ml,
    admin,
    auth
)


app = FastAPI(
    title="SmartCart API",
    description="SmartCart E-Commerce and ML Application",
    version="1.0.0"
)


# -----------------------------
# CORS CONFIGURATION
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# -----------------------------
# GLOBAL ERROR HANDLER
# -----------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "Something went wrong. Please try again later."
        }
    )


# -----------------------------
# API ROUTERS
# -----------------------------

app.include_router(customer.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(order_item.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(activity.router)
app.include_router(ml.router)
app.include_router(admin.router)
app.include_router(auth.router)


# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartCart API"
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }