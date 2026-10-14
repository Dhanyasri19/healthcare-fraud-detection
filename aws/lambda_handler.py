"""Optional API Gateway Lambda starter; configure environment variables and permissions first."""
import json
import os
import boto3

s3 = boto3.client("s3")
RESULTS_BUCKET = os.environ.get("RESULTS_BUCKET", "")
RESULTS_KEY = os.environ.get("RESULTS_KEY", "fraud-results/fraud_results.json")

def lambda_handler(event, context):
    if not RESULTS_BUCKET:
        return response(500, {"error": "RESULTS_BUCKET environment variable is not configured"})

    try:
        obj = s3.get_object(Bucket=RESULTS_BUCKET, Key=RESULTS_KEY)
        body = obj["Body"].read().decode("utf-8")
        return response(200, {"message": "Fraud results retrieved", "results": json.loads(body)})
    except Exception:
        # Avoid returning internal exception details to clients.
        return response(500, {"error": "Unable to retrieve fraud results"})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
