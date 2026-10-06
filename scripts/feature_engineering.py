import pandas as pd
import os

# =========================================================
# 1. LOAD CLEANED DATA
# =========================================================

customers = pd.read_csv("data/customers_cleaned.csv")
products = pd.read_csv("data/products_cleaned.csv")
activity = pd.read_csv("data/customer_activity_cleaned.csv")

print("Customers shape:", customers.shape)
print("Products shape:", products.shape)
print("Activity shape:", activity.shape)


# =========================================================
# 2. SELECT CUSTOMER FEATURES
# =========================================================

customer_features = customers[
    [
        "customer_id",
        "age",
        "total_purchases",
        "total_spending",
        "average_order_value",
        "website_visits"
    ]
]


# =========================================================
# 3. SELECT PRODUCT FEATURES
# =========================================================

product_features = products[
    [
        "product_id",
        "price",
        "rating"
    ]
]


# =========================================================
# 4. MERGE ACTIVITY + CUSTOMER DATA
# =========================================================

features = activity.merge(
    customer_features,
    on="customer_id",
    how="left"
)

print("\nAfter customer merge:", features.shape)


# =========================================================
# 5. MERGE PRODUCT DATA
# =========================================================

features = features.merge(
    product_features,
    on="product_id",
    how="left"
)

print("After product merge:", features.shape)


# =========================================================
# 6. RENAME COLUMNS
# =========================================================

features = features.rename(
    columns={
        "age": "customer_age",
        "price": "product_price",
        "rating": "product_rating"
    }
)


# =========================================================
# 7. SELECT ML FEATURES
# =========================================================

feature_columns = [
    "customer_id",
    "product_id",
    "customer_age",
    "total_purchases",
    "total_spending",
    "average_order_value",
    "website_visits",
    "product_price",
    "product_rating",
    "product_views",
    "cart_additions",
    "wishlist_additions",
    "previous_purchases",
    "time_spent",
    "purchased"
]

features = features[feature_columns]


# =========================================================
# 8. CHECK MISSING VALUES
# =========================================================

print("\nMissing values:")
print(features.isnull().sum())


# =========================================================
# 9. CHECK DUPLICATES
# =========================================================

print("\nDuplicate rows:", features.duplicated().sum())


# =========================================================
# 10. CREATE DATA FOLDER IF NEEDED
# =========================================================

os.makedirs("data", exist_ok=True)


# =========================================================
# 11. SAVE ML DATASET
# =========================================================

output_file = "data/ml_features.csv"

features.to_csv(
    output_file,
    index=False
)


# =========================================================
# 12. DISPLAY FINAL INFORMATION
# =========================================================

print("\nML feature dataset created successfully!")

print("Output file:", output_file)

print("Final shape:", features.shape)

print("\nFeature columns:")
print(features.columns.tolist())

print("\nTarget distribution:")
print(features["purchased"].value_counts())

print("\nFirst 5 rows:")
print(features.head())