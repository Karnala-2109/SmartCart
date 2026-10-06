import pandas as pd
import numpy as np


# =========================================================
# SMARTCART - DATA CLEANING
# =========================================================

print("\n==========================================")
print("SmartCart Data Cleaning Started")
print("==========================================")


# =========================================================
# 1. LOAD DATA
# =========================================================

customers = pd.read_csv(
    "data/customers.csv"
)

products = pd.read_csv(
    "data/products.csv"
)

orders = pd.read_csv(
    "data/orders.csv"
)

activity = pd.read_csv(
    "data/customer_activity.csv"
)


# =========================================================
# 2. DISPLAY ORIGINAL SHAPES
# =========================================================

print("\nOriginal dataset sizes:")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Activity:", activity.shape)


# =========================================================
# 3. REMOVE DUPLICATE RECORDS
# =========================================================

customers = customers.drop_duplicates()

products = products.drop_duplicates()

orders = orders.drop_duplicates()

activity = activity.drop_duplicates()


# =========================================================
# 4. CONVERT DATA TYPES
# =========================================================

customers["customer_id"] = pd.to_numeric(
    customers["customer_id"],
    errors="coerce"
)

customers["age"] = pd.to_numeric(
    customers["age"],
    errors="coerce"
)

customers["total_purchases"] = pd.to_numeric(
    customers["total_purchases"],
    errors="coerce"
)

customers["total_spending"] = pd.to_numeric(
    customers["total_spending"],
    errors="coerce"
)

customers["average_order_value"] = pd.to_numeric(
    customers["average_order_value"],
    errors="coerce"
)

customers["website_visits"] = pd.to_numeric(
    customers["website_visits"],
    errors="coerce"
)

customers["registration_date"] = pd.to_datetime(
    customers["registration_date"],
    errors="coerce"
)


products["product_id"] = pd.to_numeric(
    products["product_id"],
    errors="coerce"
)

products["price"] = pd.to_numeric(
    products["price"],
    errors="coerce"
)

products["rating"] = pd.to_numeric(
    products["rating"],
    errors="coerce"
)

products["stock"] = pd.to_numeric(
    products["stock"],
    errors="coerce"
)

products["discount"] = pd.to_numeric(
    products["discount"],
    errors="coerce"
)


orders["order_id"] = pd.to_numeric(
    orders["order_id"],
    errors="coerce"
)

orders["customer_id"] = pd.to_numeric(
    orders["customer_id"],
    errors="coerce"
)

orders["product_id"] = pd.to_numeric(
    orders["product_id"],
    errors="coerce"
)

orders["quantity"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
)

orders["price"] = pd.to_numeric(
    orders["price"],
    errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)


activity["customer_id"] = pd.to_numeric(
    activity["customer_id"],
    errors="coerce"
)

activity["product_id"] = pd.to_numeric(
    activity["product_id"],
    errors="coerce"
)


# =========================================================
# 5. CLEAN CUSTOMER AGE
# =========================================================

# Valid age should be between 18 and 100

invalid_age = (
    (customers["age"] < 18)
    | (customers["age"] > 100)
)

customers.loc[
    invalid_age,
    "age"
] = np.nan


# Fill missing age with median

customers["age"] = customers["age"].fillna(
    customers["age"].median()
)


# =========================================================
# 6. CLEAN PRODUCT PRICE
# =========================================================

# Price cannot be zero or negative

products.loc[
    products["price"] <= 0,
    "price"
] = np.nan


# Fill missing price with median

products["price"] = products["price"].fillna(
    products["price"].median()
)


# =========================================================
# 7. CLEAN PRODUCT RATING
# =========================================================

# Rating must be between 0 and 5

invalid_rating = (
    (products["rating"] < 0)
    | (products["rating"] > 5)
)

products.loc[
    invalid_rating,
    "rating"
] = np.nan


# Fill missing rating with median

products["rating"] = products["rating"].fillna(
    products["rating"].median()
)


# =========================================================
# 8. CLEAN PRODUCT STOCK
# =========================================================

# Stock cannot be negative

products.loc[
    products["stock"] < 0,
    "stock"
] = 0


# =========================================================
# 9. CLEAN DISCOUNT
# =========================================================

# Discount must be between 0 and 100

products.loc[
    (products["discount"] < 0)
    | (products["discount"] > 100),
    "discount"
] = 0


# =========================================================
# 10. REMOVE INVALID CUSTOMER IDs FROM ORDERS
# =========================================================

valid_customer_ids = set(
    customers["customer_id"].dropna()
)

orders = orders[
    orders["customer_id"].isin(
        valid_customer_ids
    )
]


# =========================================================
# 11. REMOVE INVALID PRODUCT IDs FROM ORDERS
# =========================================================

valid_product_ids = set(
    products["product_id"].dropna()
)

orders = orders[
    orders["product_id"].isin(
        valid_product_ids
    )
]


# =========================================================
# 12. CLEAN ORDER QUANTITY
# =========================================================

orders = orders[
    orders["quantity"] > 0
]


# =========================================================
# 13. CLEAN ORDER PRICE
# =========================================================

orders = orders[
    orders["price"] > 0
]


# =========================================================
# 14. CLEAN CUSTOMER ACTIVITY
# =========================================================

activity = activity[
    activity["customer_id"].isin(
        valid_customer_ids
    )
]

activity = activity[
    activity["product_id"].isin(
        valid_product_ids
    )
]


# =========================================================
# 15. FILL CUSTOMER MISSING VALUES
# =========================================================

customers["gender"] = customers[
    "gender"
].fillna("Unknown")

customers["city"] = customers[
    "city"
].fillna("Unknown")


# =========================================================
# 16. FILL ACTIVITY MISSING VALUES
# =========================================================

activity_columns = [
    "product_views",
    "cart_additions",
    "wishlist_additions",
    "previous_purchases",
    "time_spent",
    "purchased"
]

for column in activity_columns:

    activity[column] = activity[column].fillna(0)


# =========================================================
# 17. SAVE CLEANED DATA
# =========================================================

customers.to_csv(
    "data/customers_cleaned.csv",
    index=False
)

products.to_csv(
    "data/products_cleaned.csv",
    index=False
)

orders.to_csv(
    "data/orders_cleaned.csv",
    index=False
)

activity.to_csv(
    "data/customer_activity_cleaned.csv",
    index=False
)


# =========================================================
# 18. FINAL CHECK
# =========================================================

print("\n==========================================")
print("Cleaned dataset sizes")
print("==========================================")

print(
    "Customers:",
    customers.shape
)

print(
    "Products:",
    products.shape
)

print(
    "Orders:",
    orders.shape
)

print(
    "Customer Activity:",
    activity.shape
)


print("\n==========================================")
print("Remaining missing values")
print("==========================================")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nActivity:")
print(activity.isnull().sum())


print("\n==========================================")
print("Data Cleaning Completed Successfully!")
print("==========================================")