from pathlib import Path
import joblib
from src.preprocess import load_claims, prepare_features

def predict_file(input_path: str, output_path: str = "outputs/fraud_results.csv"):
    bundle = joblib.load("artifacts/fraud_model.joblib")
    model, features = bundle["model"], bundle["features"]
    df = load_claims(input_path)
    X = prepare_features(df, features)
    df["predicted_label"] = model.predict(X)
    df["fraud_status"] = df["predicted_label"].map(
        lambda value: "Suspicious" if str(value) == "1" else "Normal"
    )
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    predict_file("data/raw/insurance_claim_dataset_realistic.json")
