from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.config import DATA_PATH, FEATURE_COLUMNS, TARGET_COLUMN, TEST_SIZE, RANDOM_STATE
from src.preprocess import load_claims, prepare_features

def main():
    df = load_claims(DATA_PATH)
    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' not found. "
            f"Available columns: {list(df.columns)}. "
            "Set TARGET_COLUMN to an existing, verified label."
        )

    X = prepare_features(df, FEATURE_COLUMNS)
    y = df[TARGET_COLUMN]
    valid = y.notna()
    X, y = X.loc[valid], y.loc[valid]

    if y.nunique() < 2:
        raise ValueError("The target must contain at least two classes (e.g., 0 and 1).")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    report = classification_report(y_test, pred, output_dict=True, zero_division=0)
    print("Accuracy:", round(accuracy_score(y_test, pred), 4))
    print(classification_report(y_test, pred, zero_division=0))
    print("Confusion matrix:\n", confusion_matrix(y_test, pred))

    Path("artifacts").mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)
    joblib.dump({"model": model, "features": FEATURE_COLUMNS}, "artifacts/fraud_model.joblib")
    with open("artifacts/evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    result = df.loc[X.index].copy()
    result["predicted_label"] = model.predict(X)
    result["fraud_status"] = result["predicted_label"].map(
        lambda value: "Suspicious" if str(value) == "1" else "Normal"
    )
    result.to_csv("outputs/fraud_results.csv", index=False)
    print("Saved outputs/fraud_results.csv")

if __name__ == "__main__":
    main()
