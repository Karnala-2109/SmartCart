from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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
# PATH CONFIGURATION
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


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
# FRONTEND STATIC FILES
# -----------------------------

app.mount(
    "/frontend",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="frontend"
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
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }