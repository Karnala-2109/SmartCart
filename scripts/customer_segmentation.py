import pandas as pd
import joblib
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CUSTOMERS_PATH = os.path.join(
    BASE_DIR, "data", "customers.csv"
)

ORDERS_PATH = os.path.join(
    BASE_DIR, "data", "orders.csv"
)

ACTIVITY_PATH = os.path.join(
    BASE_DIR, "data", "customer_activity.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "customer_segments.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "customer_segmentation.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR, "models", "segmentation_scaler.pkl"
)

FEATURES_PATH = os.path.join(
    BASE_DIR, "models", "segmentation_features.pkl"
)


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

customers = pd.read_csv(CUSTOMERS_PATH)
orders = pd.read_csv(ORDERS_PATH)
activity = pd.read_csv(ACTIVITY_PATH)

print("Customers shape:", customers.shape)
print("Orders shape:", orders.shape)
print("Activity shape:", activity.shape)


# --------------------------------------------------
# Purchase features
# --------------------------------------------------

purchase_data = (
    orders
    .groupby("customer_id")
    .agg(
        total_purchases=("order_id", "count"),
        total_spending=("price", "sum")
    )
    .reset_index()
)

purchase_data["average_order_value"] = (
    purchase_data["total_spending"]
    / purchase_data["total_purchases"]
)


# --------------------------------------------------
# Activity features
# --------------------------------------------------

activity_data = (
    activity
    .groupby("customer_id")
    .agg(
        product_views=("product_views", "sum"),
        cart_additions=("cart_additions", "sum"),
        wishlist_additions=("wishlist_additions", "sum"),
        time_spent=("time_spent", "sum")
    )
    .reset_index()
)


# --------------------------------------------------
# Purchase frequency
# --------------------------------------------------

purchase_frequency = (
    orders
    .groupby("customer_id")
    .size()
    .reset_index(name="purchase_frequency")
)


# --------------------------------------------------
# Merge all customer data
# --------------------------------------------------

segmentation_data = (
    customers[["customer_id"]]
    .merge(
        purchase_data,
        on="customer_id",
        how="left"
    )
    .merge(
        activity_data,
        on="customer_id",
        how="left"
    )
    .merge(
        purchase_frequency,
        on="customer_id",
        how="left"
    )
)


# Fill missing values
segmentation_data = segmentation_data.fillna(0)


# --------------------------------------------------
# Features for K-Means
# --------------------------------------------------

segmentation_features = [
    "total_purchases",
    "total_spending",
    "average_order_value",
    "product_views",
    "cart_additions",
    "wishlist_additions",
    "time_spent",
    "purchase_frequency"
]


print("\nSegmentation features:")
print(segmentation_features)


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

X = segmentation_data[segmentation_features]


# --------------------------------------------------
# Scaling
# --------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# --------------------------------------------------
# Find best number of clusters
# --------------------------------------------------

best_k = 2
best_score = -1

print("\nSilhouette Scores:")

for k in range(2, 7):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels
    )

    print(
        f"K={k} -> "
        f"Silhouette Score={score:.4f}"
    )

    if score > best_score:
        best_score = score
        best_k = k


print("\nBest number of clusters:", best_k)


# --------------------------------------------------
# Final K-Means model
# --------------------------------------------------

final_model = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

segmentation_data["cluster"] = (
    final_model.fit_predict(X_scaled)
)


# --------------------------------------------------
# Save customer segments
# --------------------------------------------------

segmentation_data.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# Save ML files
# --------------------------------------------------

joblib.dump(
    final_model,
    MODEL_PATH
)

joblib.dump(
    scaler,
    SCALER_PATH
)

joblib.dump(
    segmentation_features,
    FEATURES_PATH
)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\nSegmentation completed successfully.")

print("\nCustomer segments:")

print(
    segmentation_data[
        [
            "customer_id",
            "total_purchases",
            "total_spending",
            "average_order_value",
            "product_views",
            "cart_additions",
            "wishlist_additions",
            "time_spent",
            "purchase_frequency",
            "cluster"
        ]
    ].head(10)
)


# --------------------------------------------------
# Files created
# --------------------------------------------------

print("\nFiles created:")

print(OUTPUT_PATH)
print(MODEL_PATH)
print(SCALER_PATH)
print(FEATURES_PATH)