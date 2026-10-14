"""Update these column names to match your actual JSON dataset."""
DATA_PATH = "data/raw/insurance_claim_dataset_realistic.json"

# Use only fields that really exist in your dataset.
FEATURE_COLUMNS = [
    "treatment_cost",
    "insurance_claim_amount",
]

# Set this to the actual ground-truth label column in your dataset.
# Examples might be "fraud_label" or "is_fraud".
TARGET_COLUMN = "fraud_label"

TEST_SIZE = 0.20
RANDOM_STATE = 42
