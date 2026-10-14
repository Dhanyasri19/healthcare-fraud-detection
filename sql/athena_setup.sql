-- Replace YOUR_BUCKET and the JSON schema/fields with your actual dataset.
-- In Athena, first set the query result location to:
-- s3://YOUR_BUCKET/athena-results/

CREATE DATABASE IF NOT EXISTS healthcare_fraud_db;

-- This example assumes one JSON object per line and flat fields.
-- LOCATION should point to the prefix containing the JSON data, not a local Windows path.
CREATE EXTERNAL TABLE IF NOT EXISTS healthcare_fraud_db.insurance_claims (
    claim_id string,
    patient_id string,
    hospital_id string,
    doctor_id string,
    treatment_code string,
    treatment_cost double,
    insurance_claim_amount double,
    claim_date string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('ignore.malformed.json' = 'true')
LOCATION 's3://YOUR_BUCKET/raw-data/'
TBLPROPERTIES ('has_encrypted_data'='false');

-- Inspect a few records
SELECT * FROM healthcare_fraud_db.insurance_claims LIMIT 10;

-- Example rule-based review query; this is a screening rule, not proof of fraud.
SELECT claim_id, treatment_code, treatment_cost, insurance_claim_amount,
       insurance_claim_amount / NULLIF(treatment_cost, 0) AS claim_ratio
FROM healthcare_fraud_db.insurance_claims
WHERE treatment_cost > 0
  AND insurance_claim_amount / treatment_cost > 1.5;
