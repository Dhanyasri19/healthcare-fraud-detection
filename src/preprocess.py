import json
import pandas as pd

def load_claims(path: str) -> pd.DataFrame:
    """Load either a JSON array/object or newline-delimited JSON records."""
    try:
        data = pd.read_json(path)
        if isinstance(data, pd.Series):
            data = data.to_frame().T
        return data
    except ValueError:
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return pd.json_normalize(records)

def prepare_features(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    missing = [c for c in feature_columns if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing feature columns: {missing}. "
            f"Available columns: {list(df.columns)}. Update src/config.py."
        )

    X = df[feature_columns].copy()
    for col in feature_columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")
    X = X.replace([float("inf"), float("-inf")], pd.NA)
    return X
