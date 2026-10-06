import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. LOAD DATA
# ==========================================

products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")

print("Products shape:", products.shape)
print("Orders shape:", orders.shape)


# ==========================================
# 2. PREPARE PRODUCT DATA
# ==========================================

products["category"] = products["category"].fillna("").astype(str)

products["rating"] = products["rating"].fillna(0)

# Combine product information
products["product_text"] = (
    products["category"]
    + " "
    + products["rating"].astype(str)
)


# ==========================================
# 3. CONVERT PRODUCTS INTO NUMERIC FEATURES
# ==========================================

vectorizer = TfidfVectorizer()

product_vectors = vectorizer.fit_transform(
    products["product_text"]
)


# ==========================================
# 4. CALCULATE PRODUCT SIMILARITY
# ==========================================

similarity_matrix = cosine_similarity(
    product_vectors
)

print("\nProduct similarity matrix created.")

print(
    "Similarity matrix shape:",
    similarity_matrix.shape
)


# ==========================================
# 5. RECOMMEND PRODUCTS FOR A CUSTOMER
# ==========================================

def recommend_products(customer_id, top_n=5):

    # Find products purchased by customer
    customer_orders = orders[
        orders["customer_id"] == customer_id
    ]

    if customer_orders.empty:

        print(
            f"\nNo purchase history found for "
            f"customer {customer_id}"
        )

        return products.head(top_n)[
            [
                "product_id",
                "category",
                "price",
                "rating"
            ]
        ]


    # Get purchased product IDs
    purchased_product_ids = (
        customer_orders["product_id"]
        .unique()
    )


    # Find product indexes
    purchased_indexes = []

    for product_id in purchased_product_ids:

        matching_indexes = products.index[
            products["product_id"] == product_id
        ].tolist()

        purchased_indexes.extend(
            matching_indexes
        )


    if not purchased_indexes:

        return products.head(top_n)[
            [
                "product_id",
                "category",
                "price",
                "rating"
            ]
        ]


    # ==========================================
    # CALCULATE RECOMMENDATION SCORES
    # ==========================================

    scores = similarity_matrix[
        purchased_indexes
    ].mean(axis=0)


    # Create recommendation dataframe
    recommendation_data = products.copy()

    recommendation_data["similarity_score"] = (
        scores
    )


    # Remove products already purchased
    recommendation_data = recommendation_data[
        ~recommendation_data["product_id"].isin(
            purchased_product_ids
        )
    ]


    # Sort by similarity
    recommendation_data = (
        recommendation_data
        .sort_values(
            "similarity_score",
            ascending=False
        )
    )


    # Return top products
    recommendations = recommendation_data.head(
        top_n
    )


    return recommendations[
        [
            "product_id",
            "category",
            "price",
            "rating",
            "similarity_score"
        ]
    ]


# ==========================================
# 6. TEST RECOMMENDATION SYSTEM
# ==========================================

test_customer_id = orders["customer_id"].iloc[0]

print(
    f"\nRecommendations for customer "
    f"{test_customer_id}:"
)

recommendations = recommend_products(
    test_customer_id,
    top_n=5
)

print(recommendations)


# ==========================================
# 7. COMPLETED
# ==========================================

print("\n========================================")
print("RECOMMENDATION SYSTEM COMPLETED")
print("========================================")