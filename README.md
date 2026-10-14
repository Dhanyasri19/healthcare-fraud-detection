# Intelligent Healthcare Fraud Detection System with GenAI Chatbot

A mini-project prototype for analyzing healthcare insurance claims, flagging potentially suspicious billing patterns, and presenting results through a query interface.

## Modules

1. **Data Engineering** — stores JSON claim data in Amazon S3 and provides Athena SQL for querying it.
2. **Cloud Engineering** — documents the AWS serverless flow and includes an optional Lambda/API Gateway starter.
3. **AI Engineering** — trains and evaluates a machine-learning classifier in Python; exports predictions for S3.
4. **Security Engineering** — provides an example least-privilege IAM policy template and role design.

> **Implementation status:** This repository is a starter scaffold. Replace the example column names with the exact fields in your dataset, add your trained model/code, and only mark AWS, chatbot, or IAM components as completed after testing them in Learner Lab. The sample chatbot is a local Streamlit prototype; it does not call Amazon Bedrock unless you add that integration.

## Architecture

```text
JSON claims dataset
       |
       v
Amazon S3 (raw data)
       |
       +----> Amazon Athena (SQL queries / data inspection)
       |
       v
Python ML pipeline (Google Colab or local Python)
       |
       v
fraud_results.csv
       |
       v
Amazon S3 (results)
       |
       +----> Streamlit chatbot/demo reads results
       |
       +----> Optional API Gateway + Lambda integration
```

## Repository structure

```text
healthcare-fraud-detection/
├── data/
│   ├── raw/.gitkeep
│   └── processed/.gitkeep
├── notebooks/
│   └── README.md
├── sql/
│   └── athena_setup.sql
├── src/
│   ├── config.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── predict.py
│   └── chatbot_app.py
├── aws/
│   ├── lambda_handler.py
│   └── iam_policy_example.json
├── reports/
│   └── README.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Dataset

Keep the dataset private if it contains real patient information. For GitHub, use synthetic or anonymized sample records. Do not commit AWS credentials, access keys, real patient data, or private Learner Lab details.

Place your JSON file at `data/raw/insurance_claim_dataset_realistic.json`, or set the `DATA_PATH` environment variable to its location.

The starter code expects one JSON object per line (JSON Lines) or a JSON array of objects. If your file uses a different structure, adapt `load_claims()` in `src/preprocess.py`.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Machine-learning workflow

1. Check and edit the feature/target column names in `src/config.py`.
2. Ensure the dataset has a verified target label column, such as `fraud_label` with values `0` and `1`. Do not invent labels from the model output.
3. Run:

```bash
python -m src.train_model
```

4. The script writes a trained model and evaluation report under `artifacts/`, and predictions to `outputs/fraud_results.csv`.
5. Upload the result file to your S3 bucket manually through the AWS Console, or use the AWS SDK only with valid temporary Learner Lab credentials.

If your current model is already trained in Google Colab, you can instead export its predictions there and upload the results. You do not need to retrain solely to use this repository.

## Athena

Edit the bucket and object prefix in `sql/athena_setup.sql` before running it in Athena. Set Athena's query result location to an S3 prefix such as `s3://YOUR-BUCKET/athena-results/`.

The Athena JSON table definition must match the actual structure of the JSON records. For nested or nonstandard JSON, update the schema/SerDe or preprocess to a tabular format first.

## Chatbot demo

Run the local results-query interface:

```bash
streamlit run src/chatbot_app.py
```

It reads `outputs/fraud_results.csv` by default. It is a rule-based query demo, not a generative AI model. For a true GenAI chatbot, connect a supported LLM (for example, Amazon Bedrock) through a backend and pass only the minimum necessary claim context.

## AWS security

- Use IAM roles and least-privilege permissions.
- Keep S3 Block Public Access enabled.
- Use encryption at rest and HTTPS in transit.
- Never put AWS access keys in source code or GitHub.
- Learner Lab credentials are temporary; do not publish them.
- Apply and test role policies in your lab before claiming role-based access control is implemented.

## Reported model result

The project notes currently report accuracy `0.942`, class-1 precision `0.87`, recall `0.74`, and F1-score `0.80` on a 1,000-record test set. Keep these numbers only if they came from the model and dataset included in your final submission. Accuracy alone does not establish real-world fraud detection performance.

## Limitations

This is an academic prototype, not a production healthcare system. A suspicious prediction is a review flag, not proof of fraud. Production use would require validated labels, representative data, privacy controls, bias testing, monitoring, and human investigation.
