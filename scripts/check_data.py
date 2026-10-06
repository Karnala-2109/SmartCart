import pandas as pd


# ==========================================
# SmartCart - Dataset Checking
# ==========================================

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")
activity = pd.read_csv("data/customer_activity.csv")


# ==========================================
# 1. Dataset Shapes
# ==========================================

print("\n========== DATASET SHAPES ==========")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("Customer Activity:", activity.shape)


# ==========================================
# 2. Customers
# ==========================================

print("\n========== CUSTOMERS ==========")

print(customers.head())

print("\nMissing values:")
print(customers.isnull().sum())

print("\nDuplicate rows:")
print(customers.duplicated().sum())


# ==========================================
# 3. Products
# ==========================================

print("\n========== PRODUCTS ==========")

print(products.head())

print("\nMissing values:")
print(products.isnull().sum())

print("\nDuplicate rows:")
print(products.duplicated().sum())


# ==========================================
# 4. Orders
# ==========================================

print("\n========== ORDERS ==========")

print(orders.head())

print("\nMissing values:")
print(orders.isnull().sum())

print("\nDuplicate rows:")
print(orders.duplicated().sum())


# ==========================================
# 5. Customer Activity
# ==========================================

print("\n========== CUSTOMER ACTIVITY ==========")

print(activity.head())

print("\nMissing values:")
print(activity.isnull().sum())

print("\nDuplicate rows:")
print(activity.duplicated().sum())


# ==========================================
# 6. Data Types
# ==========================================

print("\n========== DATA TYPES ==========")

print("\nCustomers:")
print(customers.dtypes)

print("\nProducts:")
print(products.dtypes)

print("\nOrders:")
print(orders.dtypes)

print("\nCustomer Activity:")
print(activity.dtypes)


# ==========================================
# 7. Unique IDs
# ==========================================

print("\n========== UNIQUE IDS ==========")

print(
    "Unique customer IDs:",
    customers["customer_id"].nunique()
)

print(
    "Unique product IDs:",
    products["product_id"].nunique()
)

print(
    "Unique order IDs:",
    orders["order_id"].nunique()
)


# ==========================================
# 8. Basic Statistics
# ==========================================

print("\n========== CUSTOMER STATISTICS ==========")

print(
    customers[
        [
            "age",
            "total_purchases",
            "total_spending",
            "average_order_value",
            "website_visits"
        ]
    ].describe()
)


print("\n========== PRODUCT STATISTICS ==========")

print(
    products[
        [
            "price",
            "rating",
            "stock",
            "discount"
        ]
    ].describe()
)


print("\n========== ORDER STATISTICS ==========")

print(
    orders[
        [
            "quantity",
            "price"
        ]
    ].describe()
)


# ==========================================
# 9. Categories
# ==========================================

print("\n========== PRODUCT CATEGORIES ==========")

print(
    products["category"].value_counts()
)


# ==========================================
# 10. Payment Methods
# ==========================================

print("\n========== PAYMENT METHODS ==========")

print(
    orders["payment_method"].value_counts()
)


# ==========================================
# 11. Order Status
# ==========================================

print("\n========== ORDER STATUS ==========")

print(
    orders["order_status"].value_counts()
)


print("\n==========================================")
print("Dataset checking completed successfully!")
print("==========================================")