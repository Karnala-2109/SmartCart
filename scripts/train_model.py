import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/ml_features.csv")

print("Dataset shape:", df.shape)


# ==========================================
# 2. FEATURES AND TARGET
# ==========================================

X = df.drop("purchased", axis=1)

y = df["purchased"]

# Remove ID columns
X = X.drop(
    ["customer_id", "product_id"],
    axis=1
)

print("Features shape:", X.shape)
print("Target shape:", y.shape)


# ==========================================
# 3. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# ==========================================
# 4. SCALING
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# ==========================================
# 5. LOGISTIC REGRESSION
# ==========================================

logistic_model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

logistic_model.fit(
    X_train_scaled,
    y_train
)

logistic_pred = logistic_model.predict(
    X_test_scaled
)

logistic_prob = logistic_model.predict_proba(
    X_test_scaled
)[:, 1]


# ==========================================
# 6. DECISION TREE
# ==========================================

decision_tree_model = DecisionTreeClassifier(
    random_state=42,
    max_depth=5
)

decision_tree_model.fit(
    X_train,
    y_train
)

tree_pred = decision_tree_model.predict(
    X_test
)

tree_prob = decision_tree_model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# 7. RANDOM FOREST
# ==========================================

random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

random_forest_model.fit(
    X_train,
    y_train
)

rf_pred = random_forest_model.predict(
    X_test
)

rf_prob = random_forest_model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# 8. MODEL EVALUATION FUNCTION
# ==========================================

def evaluate_model(
    model_name,
    y_test,
    predictions,
    probabilities
):

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    print("\n========================================")
    print(model_name)
    print("========================================")

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    return {
        "model": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc
    }


# ==========================================
# 9. EVALUATE ALL THREE MODELS
# ==========================================

results = []

results.append(
    evaluate_model(
        "Logistic Regression",
        y_test,
        logistic_pred,
        logistic_prob
    )
)

results.append(
    evaluate_model(
        "Decision Tree",
        y_test,
        tree_pred,
        tree_prob
    )
)

results.append(
    evaluate_model(
        "Random Forest",
        y_test,
        rf_pred,
        rf_prob
    )
)


# ==========================================
# 10. MODEL COMPARISON
# ==========================================

results_df = pd.DataFrame(results)

print("\n\n========================================")
print("MODEL COMPARISON")
print("========================================")

print(
    results_df.to_string(index=False)
)


# ==========================================
# 11. SELECT BEST MODEL
# ==========================================

best_index = results_df["f1"].idxmax()

best_model_name = results_df.loc[
    best_index,
    "model"
]

print(
    f"\nBest Model based on F1 Score: "
    f"{best_model_name}"
)


# ==========================================
# 12. SAVE BEST MODEL
# ==========================================

os.makedirs("models", exist_ok=True)

if best_model_name == "Logistic Regression":

    best_model = logistic_model

elif best_model_name == "Decision Tree":

    best_model = decision_tree_model

else:

    best_model = random_forest_model


joblib.dump(
    best_model,
    "models/purchase_model.pkl"
)


# Save scaler
joblib.dump(
    scaler,
    "models/scaler.pkl"
)


# Save feature names
joblib.dump(
    X.columns.tolist(),
    "models/feature_columns.pkl"
)


print("\n========================================")
print("MODEL SAVING")
print("========================================")

print("Best model saved:")
print("models/purchase_model.pkl")

print("Scaler saved:")
print("models/scaler.pkl")

print("Feature columns saved:")
print("models/feature_columns.pkl")