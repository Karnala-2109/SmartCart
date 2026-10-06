import os
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# SMARTCART - EXPLORATORY DATA ANALYSIS
# =========================================================

print("\n==========================================")
print("SmartCart EDA Started")
print("==========================================")


# =========================================================
# 1. CREATE OUTPUT FOLDER
# =========================================================

OUTPUT_DIR = "eda_output"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =========================================================
# 2. LOAD CLEANED DATA
# =========================================================

customers = pd.read_csv(
    "data/customers_cleaned.csv"
)

products = pd.read_csv(
    "data/products_cleaned.csv"
)

orders = pd.read_csv(
    "data/orders_cleaned.csv"
)


# Convert dates

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

customers["registration_date"] = pd.to_datetime(
    customers["registration_date"]
)


# =========================================================
# 3. CREATE REVENUE COLUMN
# =========================================================

# =========================================================
# 3. CREATE REVENUE COLUMN
# =========================================================

orders["revenue"] = orders["price"]

# =========================================================
# 4. CATEGORY SALES ANALYSIS
# =========================================================

print("\n========== CATEGORY SALES ==========")

orders_products = orders.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "rating",
            "stock"
        ]
    ],
    on="product_id",
    how="left"
)


category_sales = (
    orders_products
    .groupby("category")["revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)


print(category_sales)


print(
    "\nHighest selling category:",
    category_sales.index[0]
)


# =========================================================
# 5. TOP PRODUCTS BY REVENUE
# =========================================================

print("\n========== TOP PRODUCTS ==========")

top_products = (
    orders_products
    .groupby(
        [
            "product_id",
            "product_name"
        ]
    )["revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)


print(top_products)


# =========================================================
# 6. TOP CUSTOMERS BY REVENUE
# =========================================================

print("\n========== TOP CUSTOMERS ==========")

customer_sales = (
    orders
    .groupby("customer_id")["revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)


top_customer_details = (
    customer_sales
    .reset_index()
    .merge(
        customers[
            [
                "customer_id",
                "city"
            ]
        ],
        on="customer_id",
        how="left"
    )
)


print(top_customer_details)


# =========================================================
# 7. AVERAGE ORDER VALUE
# =========================================================

print("\n========== AVERAGE ORDER VALUE ==========")

average_order_value = orders[
    "revenue"
].mean()


print(
    f"Average Order Value: "
    f"{average_order_value:.2f}"
)


# =========================================================
# 8. PAYMENT METHOD ANALYSIS
# =========================================================

print("\n========== PAYMENT METHODS ==========")

payment_analysis = (
    orders
    .groupby("payment_method")
    .agg(
        order_count=(
            "order_id",
            "count"
        ),
        total_revenue=(
            "revenue",
            "sum"
        )
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
)


print(payment_analysis)


# =========================================================
# 9. CUSTOMER COUNT BY CITY
# =========================================================

print("\n========== CUSTOMERS BY CITY ==========")

city_customers = (
    customers[
        "city"
    ]
    .value_counts()
)


print(city_customers)


# =========================================================
# 10. TOP RATED PRODUCTS
# =========================================================

print("\n========== TOP RATED PRODUCTS ==========")

top_rated_products = (
    products[
        [
            "product_id",
            "product_name",
            "category",
            "rating"
        ]
    ]
    .sort_values(
        "rating",
        ascending=False
    )
    .head(10)
)


print(top_rated_products)


# =========================================================
# 11. REPEAT PURCHASE ANALYSIS
# =========================================================

print("\n========== REPEAT PURCHASE ANALYSIS ==========")

customer_order_counts = (
    orders
    .groupby("customer_id")[
        "order_id"
    ]
    .count()
)


repeat_customers = (
    customer_order_counts >= 2
).sum()


total_customers_with_orders = (
    customer_order_counts.shape[0]
)


if total_customers_with_orders > 0:

    repeat_purchase_percentage = (
        repeat_customers
        / total_customers_with_orders
        * 100
    )

else:

    repeat_purchase_percentage = 0


print(
    f"Customers with repeat purchases: "
    f"{repeat_customers}"
)

print(
    f"Repeat purchase percentage: "
    f"{repeat_purchase_percentage:.2f}%"
)


# =========================================================
# 12. MONTHLY REVENUE
# =========================================================

print("\n========== MONTHLY REVENUE ==========")

orders["month"] = (
    orders["order_date"]
    .dt.to_period("M")
    .astype(str)
)


monthly_revenue = (
    orders
    .groupby("month")[
        "revenue"
    ]
    .sum()
)


print(monthly_revenue)


# =========================================================
# 13. LOW STOCK PRODUCTS
# =========================================================

print("\n========== LOW STOCK PRODUCTS ==========")

LOW_STOCK_LIMIT = 20


low_stock_products = products[
    products["stock"] <= LOW_STOCK_LIMIT
][
    [
        "product_id",
        "product_name",
        "category",
        "stock"
    ]
].sort_values(
    "stock"
)


print(low_stock_products)


# =========================================================
# 14. CHART 1 - CATEGORY SALES
# =========================================================

plt.figure(
    figsize=(10, 6)
)

category_sales.plot(
    kind="bar"
)

plt.title(
    "Sales Revenue by Category"
)

plt.xlabel(
    "Category"
)

plt.ylabel(
    "Revenue"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/category_sales.png"
)

plt.close()


# =========================================================
# 15. CHART 2 - MONTHLY REVENUE
# =========================================================

plt.figure(
    figsize=(12, 6)
)

monthly_revenue.plot(
    kind="line",
    marker="o"
)

plt.title(
    "Monthly Revenue"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Revenue"
)

plt.xticks(
    rotation=45
)

plt.grid(
    True
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/monthly_revenue.png"
)

plt.close()


# =========================================================
# 16. CHART 3 - TOP RATED PRODUCTS
# =========================================================

plt.figure(
    figsize=(10, 6)
)

top_rated_products_plot = (
    top_rated_products
    .sort_values(
        "rating"
    )
)


plt.barh(
    top_rated_products_plot[
        "product_name"
    ],
    top_rated_products_plot[
        "rating"
    ]
)

plt.title(
    "Top Rated Products"
)

plt.xlabel(
    "Rating"
)

plt.ylabel(
    "Product"
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/top_rated_products.png"
)

plt.close()


# =========================================================
# 17. SAVE ANALYSIS RESULTS
# =========================================================

category_sales.to_csv(
    f"{OUTPUT_DIR}/category_sales.csv"
)

top_products.to_csv(
    f"{OUTPUT_DIR}/top_products.csv"
)

customer_sales.to_csv(
    f"{OUTPUT_DIR}/top_customers.csv"
)

monthly_revenue.to_csv(
    f"{OUTPUT_DIR}/monthly_revenue.csv"
)

low_stock_products.to_csv(
    f"{OUTPUT_DIR}/low_stock_products.csv",
    index=False
)


# =========================================================
# 18. FINAL MESSAGE
# =========================================================

print("\n==========================================")
print("EDA Completed Successfully!")
print("==========================================")

print("\nCharts created:")

print(
    "1. eda_output/category_sales.png"
)

print(
    "2. eda_output/monthly_revenue.png"
)

print(
    "3. eda_output/top_rated_products.png"
)

print("\nAnalysis files created:")

print(
    "1. eda_output/category_sales.csv"
)

print(
    "2. eda_output/top_products.csv"
)

print(
    "3. eda_output/top_customers.csv"
)

print(
    "4. eda_output/monthly_revenue.csv"
)

print(
    "5. eda_output/low_stock_products.csv"
)

print("\n==========================================")