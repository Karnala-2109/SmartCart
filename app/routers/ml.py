from fastapi import APIRouter, HTTPException
import pandas as pd
import joblib
import os

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)


# =========================================================
# FILE PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


CUSTOMERS_FILE = os.path.join(
    DATA_DIR,
    "customers.csv"
)


PRODUCTS_FILE = os.path.join(
    DATA_DIR,
    "products.csv"
)


ORDERS_FILE = os.path.join(
    DATA_DIR,
    "orders.csv"
)


ACTIVITY_FILE = os.path.join(
    DATA_DIR,
    "customer_activity.csv"
)


SEGMENTS_FILE = os.path.join(
    DATA_DIR,
    "customer_segments.csv"
)


# =========================================================
# LOAD ML FILES
# =========================================================

purchase_model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "purchase_model.pkl"
    )
)


scaler = joblib.load(
    os.path.join(
        MODEL_DIR,
        "scaler.pkl"
    )
)


feature_columns = joblib.load(
    os.path.join(
        MODEL_DIR,
        "feature_columns.pkl"
    )
)


segmentation_model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "customer_segmentation.pkl"
    )
)


segmentation_scaler = joblib.load(
    os.path.join(
        MODEL_DIR,
        "segmentation_scaler.pkl"
    )
)


segmentation_features = joblib.load(
    os.path.join(
        MODEL_DIR,
        "segmentation_features.pkl"
    )
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def load_customers():

    return pd.read_csv(
        CUSTOMERS_FILE
    )


def load_products():

    return pd.read_csv(
        PRODUCTS_FILE
    )


def load_orders():

    return pd.read_csv(
        ORDERS_FILE
    )


def load_activity():

    return pd.read_csv(
        ACTIVITY_FILE
    )


# =========================================================
# 1. PURCHASE PREDICTION
# =========================================================

@router.get("/predict-purchase")
def predict_purchase(

    customer_age: int,

    total_purchases: int,

    total_spending: float,

    average_order_value: float,

    website_visits: int,

    product_price: float,

    product_rating: float,

    product_views: int,

    cart_additions: int,

    wishlist_additions: int,

    previous_purchases: int,

    time_spent: float

):

    input_data = pd.DataFrame(
        [[
            customer_age,
            total_purchases,
            total_spending,
            average_order_value,
            website_visits,
            product_price,
            product_rating,
            product_views,
            cart_additions,
            wishlist_additions,
            previous_purchases,
            time_spent
        ]],
        columns=feature_columns
    )


    scaled_data = scaler.transform(
        input_data
    )


    prediction = purchase_model.predict(
        scaled_data
    )[0]


    probability = purchase_model.predict_proba(
        scaled_data
    )[0][1]


    result = (
        "Will Purchase"
        if prediction == 1
        else "Will Not Purchase"
    )


    return {

        "prediction": int(
            prediction
        ),

        "result": result,

        "purchase_probability": round(
            float(probability),
            3
        )

    }


# =========================================================
# 2. CUSTOMER SEGMENT
# =========================================================

@router.get("/customer-segment/{customer_id}")
def customer_segment(
    customer_id: int
):

    customers = load_customers()

    orders = load_orders()

    activity = load_activity()


    customer = customers[
        customers["customer_id"] ==
        customer_id
    ]


    if customer.empty:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )


    customer_orders = orders[
        orders["customer_id"] ==
        customer_id
    ]


    customer_activity = activity[
        activity["customer_id"] ==
        customer_id
    ]


    total_purchases = len(
        customer_orders
    )


    total_spending = (
        customer_orders["price"]
        .sum()
        if "price" in customer_orders.columns
        else 0
    )


    average_order_value = (

        total_spending /
        total_purchases

        if total_purchases > 0
        else 0

    )


    product_views = (
        customer_activity[
            "product_views"
        ].sum()
    )


    cart_additions = (
        customer_activity[
            "cart_additions"
        ].sum()
    )


    wishlist_additions = (
        customer_activity[
            "wishlist_additions"
        ].sum()
    )


    time_spent = (
        customer_activity[
            "time_spent"
        ].sum()
    )


    purchase_frequency = (
        total_purchases
    )


    data = pd.DataFrame(
        [[
            total_purchases,
            total_spending,
            average_order_value,
            product_views,
            cart_additions,
            wishlist_additions,
            time_spent,
            purchase_frequency
        ]],
        columns=segmentation_features
    )


    scaled_data = (
        segmentation_scaler.transform(
            data
        )
    )


    cluster = int(
        segmentation_model.predict(
            scaled_data
        )[0]
    )


    # Simple business-friendly labels

    if cluster == 0:

        segment = "At-Risk"

    elif cluster == 1:

        segment = "Occasional"

    elif cluster == 2:

        segment = "Regular"

    elif cluster == 3:

        segment = "Loyal"

    else:

        segment = "High Value"


    return {

        "customer_id": customer_id,

        "cluster": cluster,

        "segment": segment

    }


# =========================================================
# 3. RECOMMENDATIONS
# =========================================================

@router.get("/recommendations/{customer_id}")
def recommendations(
    customer_id: int
):

    customers = load_customers()

    products = load_products()

    orders = load_orders()


    customer = customers[
        customers["customer_id"] ==
        customer_id
    ]


    if customer.empty:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )


    customer_orders = orders[
        orders["customer_id"] ==
        customer_id
    ]


    purchased_products = set()


    if not customer_orders.empty:

        if "product_id" in customer_orders.columns:

            purchased_products = set(
                customer_orders[
                    "product_id"
                ].astype(int)
            )


    # -----------------------------------------------------
    # Recommend products not already purchased
    # -----------------------------------------------------

    recommended_products = products[
        ~products["product_id"].isin(
            purchased_products
        )
    ].copy()


    # Highest rated products first

    recommended_products = (
        recommended_products
        .sort_values(
            by=[
                "rating",
                "price"
            ],
            ascending=[
                False,
                False
            ]
        )
        .head(20)
    )


    # Fallback

    if recommended_products.empty:

        recommended_products = (
            products
            .sort_values(
                by="rating",
                ascending=False
            )
            .head(20)
        )


    result = []


    for _, product in (
        recommended_products.iterrows()
    ):

        result.append({

            "product_id": int(
                product["product_id"]
            ),

            "product_name":
                product["product_name"],

            "category":
                product["category"],

            "price": float(
                product["price"]
            ),

            "rating": float(
                product["rating"]
            ),

            "stock": int(
                product["stock"]
            )

        })


    return result


# =========================================================
# 4. CUSTOMER DASHBOARD
# =========================================================

@router.get("/customer-dashboard/{customer_id}")
def customer_dashboard(
    customer_id: int
):

    customers = load_customers()

    products = load_products()

    orders = load_orders()

    activity = load_activity()


    # -----------------------------------------------------
    # CUSTOMER
    # -----------------------------------------------------

    customer = customers[
        customers["customer_id"] ==
        customer_id
    ]


    if customer.empty:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )


    customer_row = (
        customer.iloc[0]
    )


    # -----------------------------------------------------
    # CUSTOMER ORDERS
    # -----------------------------------------------------

    customer_orders = orders[
        orders["customer_id"] ==
        customer_id
    ]


    # -----------------------------------------------------
    # CUSTOMER ACTIVITY
    # -----------------------------------------------------

    customer_activity = activity[
        activity["customer_id"] ==
        customer_id
    ]


    # -----------------------------------------------------
    # PURCHASE SUMMARY
    # -----------------------------------------------------

    total_purchases = len(
        customer_orders
    )


    if (
        "price" in
        customer_orders.columns
    ):

        total_spending = float(
            customer_orders[
                "price"
            ].sum()
        )

    else:

        total_spending = 0.0


    if total_purchases > 0:

        average_order_value = (
            total_spending /
            total_purchases
        )

    else:

        average_order_value = 0.0


    purchase_frequency = (
        total_purchases
    )


    # -----------------------------------------------------
    # ACTIVITY SUMMARY
    # -----------------------------------------------------

    if customer_activity.empty:

        product_views = 0

        cart_additions = 0

        wishlist_additions = 0

        time_spent = 0

    else:

        product_views = int(
            customer_activity[
                "product_views"
            ].sum()
        )


        cart_additions = int(
            customer_activity[
                "cart_additions"
            ].sum()
        )


        wishlist_additions = int(
            customer_activity[
                "wishlist_additions"
            ].sum()
        )


        time_spent = int(
            customer_activity[
                "time_spent"
            ].sum()
        )


    # -----------------------------------------------------
    # CUSTOMER SEGMENT
    # -----------------------------------------------------

    segmentation_data = pd.DataFrame(
        [[
            total_purchases,

            total_spending,

            average_order_value,

            product_views,

            cart_additions,

            wishlist_additions,

            time_spent,

            purchase_frequency
        ]],
        columns=segmentation_features
    )


    segmentation_scaled = (
        segmentation_scaler.transform(
            segmentation_data
        )
    )


    cluster = int(
        segmentation_model.predict(
            segmentation_scaled
        )[0]
    )


    if cluster == 0:

        segment = "At-Risk"

    elif cluster == 1:

        segment = "Occasional"

    elif cluster == 2:

        segment = "Regular"

    elif cluster == 3:

        segment = "Loyal"

    else:

        segment = "High Value"


    # -----------------------------------------------------
    # RECOMMENDED PRODUCTS
    # -----------------------------------------------------

    purchased_products = set()


    if not customer_orders.empty:

        if "product_id" in customer_orders.columns:

            purchased_products = set(
                customer_orders[
                    "product_id"
                ].astype(int)
            )


    recommended_products = products[
        ~products["product_id"].isin(
            purchased_products
        )
    ].copy()


    recommended_products = (
        recommended_products
        .sort_values(
            by=[
                "rating",
                "price"
            ],
            ascending=[
                False,
                False
            ]
        )
        .head(20)
    )


    if recommended_products.empty:

        recommended_products = (
            products
            .sort_values(
                by="rating",
                ascending=False
            )
            .head(20)
        )


    recommendations_list = []


    for _, product in (
        recommended_products.iterrows()
    ):

        recommendations_list.append({

            "product_id": int(
                product["product_id"]
            ),

            "product_name":
                product["product_name"],

            "category":
                product["category"],

            "price": float(
                product["price"]
            ),

            "rating": float(
                product["rating"]
            ),

            "stock": int(
                product["stock"]
            )

        })


    # -----------------------------------------------------
    # FINAL DASHBOARD RESPONSE
    # -----------------------------------------------------

    return {

        "customer": {

            "customer_id": int(
                customer_row[
                    "customer_id"
                ]
            ),

            "name": str(
                customer_row.get(
                    "name",
                    "N/A"
                )
            ),

            "email": str(
                customer_row.get(
                    "email",
                    "N/A"
                )
            ),

            "age": int(
                customer_row["age"]
            ),

            "gender": str(
                customer_row.get(
                    "gender",
                    "N/A"
                )
            ),

            "location": str(
                customer_row.get(
                    "city",
                    "N/A"
                )
            )

        },


        "purchase_summary": {

            "total_purchases":
                int(total_purchases),

            "total_spending":
                round(
                    total_spending,
                    2
                ),

            "average_order_value":
                round(
                    average_order_value,
                    2
                ),

            "purchase_frequency":
                int(purchase_frequency)

        },


        "activity_summary": {

            "product_views":
                int(product_views),

            "cart_additions":
                int(cart_additions),

            "wishlist_additions":
                int(wishlist_additions),

            "time_spent":
                int(time_spent)

        },


        "customer_segment": {

            "segment":
                segment,

            "cluster":
                cluster

        },


        "recommendations":
            recommendations_list

    }