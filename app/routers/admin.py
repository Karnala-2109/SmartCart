from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter(
    prefix="/admin",
    tags=["Admin Analytics"]
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


@router.get("/analytics")
def admin_analytics():

    try:

        # --------------------------------
        # Load datasets
        # --------------------------------

        customers = pd.read_csv(
            os.path.join(
                BASE_DIR,
                "data",
                "customers.csv"
            )
        )

        products = pd.read_csv(
            os.path.join(
                BASE_DIR,
                "data",
                "products.csv"
            )
        )

        orders = pd.read_csv(
            os.path.join(
                BASE_DIR,
                "data",
                "orders.csv"
            )
        )

        segments = pd.read_csv(
            os.path.join(
                BASE_DIR,
                "data",
                "customer_segments.csv"
            )
        )

        # --------------------------------
        # Basic Admin Analytics
        # --------------------------------

        total_customers = len(customers)

        total_products = len(products)

        total_orders = len(orders)

        # price already represents total price
        total_revenue = orders["price"].sum()

        # --------------------------------
        # Customer Segment Counts
        # --------------------------------

        segment_counts = (
            segments["segment"]
            .value_counts()
            .to_dict()
        )

        # --------------------------------
        # Top-Selling Products
        # --------------------------------

        top_products = (
            orders.groupby("product_id")
            .agg(
                total_quantity_sold=("quantity", "sum"),
                total_revenue=("price", "sum")
            )
            .reset_index()
            .sort_values(
                "total_quantity_sold",
                ascending=False
            )
            .head(5)
        )

        top_products["product_id"] = (
            top_products["product_id"]
            .astype(int)
        )

        top_products = top_products.merge(
            products[
                [
                    "product_id",
                    "product_name"
                ]
            ],
            on="product_id",
            how="left"
        )

        top_selling_products = []

        for _, row in top_products.iterrows():

            top_selling_products.append({
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "total_quantity_sold": int(
                    row["total_quantity_sold"]
                ),
                "total_revenue": round(
                    float(row["total_revenue"]),
                    2
                )
            })

        # --------------------------------
        # Sales Summary
        # --------------------------------

        average_order_value = (
            total_revenue / total_orders
            if total_orders > 0
            else 0
        )

        highest_order_value = (
            orders["price"].max()
            if not orders.empty
            else 0
        )

        lowest_order_value = (
            orders["price"].min()
            if not orders.empty
            else 0
        )

        sales_summary = {
            "average_order_value": round(
                float(average_order_value),
                2
            ),
            "highest_order_value": round(
                float(highest_order_value),
                2
            ),
            "lowest_order_value": round(
                float(lowest_order_value),
                2
            )
        }

        # --------------------------------
        # Final Response
        # --------------------------------

        return {
            "total_customers": total_customers,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": round(
                float(total_revenue),
                2
            ),
            "customer_segments": segment_counts,
            "top_selling_products": top_selling_products,
            "sales_summary": sales_summary
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )