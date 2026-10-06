import os
import numpy as np
import pandas as pd

# --------------------------------------------------
# Basic configuration
# --------------------------------------------------

np.random.seed(42)

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

# --------------------------------------------------
# 1. Generate Customers
# --------------------------------------------------

NUM_CUSTOMERS = 120

customer_ids = np.arange(1, NUM_CUSTOMERS + 1)

cities = [
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Vijayawada",
    "Tirupati",
    "Kochi",
    "Calicut",
    "Mumbai",
    "Delhi",
    "Pune"
]

genders = ["Male", "Female"]

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "age": np.random.randint(18, 61, NUM_CUSTOMERS),
    "gender": np.random.choice(genders, NUM_CUSTOMERS),
    "city": np.random.choice(cities, NUM_CUSTOMERS),
    "registration_date": pd.date_range(
        start="2023-01-01",
        periods=NUM_CUSTOMERS,
        freq="7D"
    ),
    "total_purchases": np.random.randint(1, 30, NUM_CUSTOMERS),
    "total_spending": np.round(
        np.random.uniform(500, 100000, NUM_CUSTOMERS),
        2
    ),
    "average_order_value": np.round(
        np.random.uniform(500, 5000, NUM_CUSTOMERS),
        2
    ),
    "website_visits": np.random.randint(10, 300, NUM_CUSTOMERS)
})

customers.to_csv(
    f"{DATA_DIR}/customers.csv",
    index=False
)

# --------------------------------------------------
# 2. Generate Products
# --------------------------------------------------

NUM_PRODUCTS = 60

product_ids = np.arange(1, NUM_PRODUCTS + 1)

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Beauty",
    "Sports",
    "Books"
]

product_names = [
    f"Product {i}"
    for i in product_ids
]

products = pd.DataFrame({
    "product_id": product_ids,
    "product_name": product_names,
    "category": np.random.choice(
        categories,
        NUM_PRODUCTS
    ),
    "price": np.round(
        np.random.uniform(100, 50000, NUM_PRODUCTS),
        2
    ),
    "rating": np.round(
        np.random.uniform(2.5, 5.0, NUM_PRODUCTS),
        1
    ),
    "stock": np.random.randint(
        0,
        200,
        NUM_PRODUCTS
    ),
    "discount": np.random.randint(
        0,
        31,
        NUM_PRODUCTS
    )
})

products.to_csv(
    f"{DATA_DIR}/products.csv",
    index=False
)

# --------------------------------------------------
# 3. Generate Orders
# --------------------------------------------------

NUM_ORDERS = 700

order_ids = np.arange(1, NUM_ORDERS + 1)

order_customer_ids = np.random.choice(
    customer_ids,
    NUM_ORDERS
)

order_product_ids = np.random.choice(
    product_ids,
    NUM_ORDERS
)

quantities = np.random.randint(
    1,
    5,
    NUM_ORDERS
)

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

order_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "Pending"
]

order_dates = pd.date_range(
    start="2025-01-01",
    end="2026-09-30",
    periods=NUM_ORDERS
)

# Get product prices for orders
product_price_map = products.set_index(
    "product_id"
)["price"].to_dict()

order_prices = [
    round(
        product_price_map[product_id] * quantity,
        2
    )
    for product_id, quantity
    in zip(order_product_ids, quantities)
]

orders = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": order_customer_ids,
    "product_id": order_product_ids,
    "quantity": quantities,
    "order_date": order_dates,
    "price": order_prices,
    "payment_method": np.random.choice(
        payment_methods,
        NUM_ORDERS
    ),
    "order_status": np.random.choice(
        order_statuses,
        NUM_ORDERS
    )
})

orders.to_csv(
    f"{DATA_DIR}/orders.csv",
    index=False
)

# --------------------------------------------------
# 4. Generate Customer Activity
# --------------------------------------------------

activity_rows = []

for customer_id in customer_ids:

    # Each customer interacts with around 12 products
    selected_products = np.random.choice(
        product_ids,
        12,
        replace=False
    )

    for product_id in selected_products:

        product_views = np.random.randint(
            1,
            30
        )

        cart_additions = np.random.randint(
            0,
            10
        )

        wishlist_additions = np.random.randint(
            0,
            6
        )

        previous_purchases = np.random.randint(
            0,
            5
        )

        time_spent = np.random.randint(
            10,
            600
        )

        # Generate purchase probability
        purchase_probability = (
            0.05
            + min(product_views / 100, 0.25)
            + min(cart_additions / 20, 0.30)
            + min(wishlist_additions / 20, 0.15)
            + min(previous_purchases / 10, 0.20)
        )

        purchase_probability = min(
            purchase_probability,
            0.95
        )

        purchased = np.random.binomial(
            1,
            purchase_probability
        )

        activity_rows.append({
            "customer_id": customer_id,
            "product_id": product_id,
            "product_views": product_views,
            "cart_additions": cart_additions,
            "wishlist_additions": wishlist_additions,
            "previous_purchases": previous_purchases,
            "time_spent": time_spent,
            "purchased": purchased
        })

activity = pd.DataFrame(activity_rows)

activity.to_csv(
    f"{DATA_DIR}/customer_activity.csv",
    index=False
)

# --------------------------------------------------
# 5. Print Dataset Information
# --------------------------------------------------

print("\n======================================")
print("SmartCart Dataset Generation Complete")
print("======================================")

print("\nCustomers:")
print(customers.shape)

print("\nProducts:")
print(products.shape)

print("\nOrders:")
print(orders.shape)

print("\nCustomer Activity:")
print(activity.shape)

print("\nFiles created:")

print("1. data/customers.csv")
print("2. data/products.csv")
print("3. data/orders.csv")
print("4. data/customer_activity.csv")

print("\n======================================")
print("Done!")
print("======================================")