import json
import os
import boto3
import re
from botocore.exceptions import ClientError

sns = boto3.client("sns")

TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

# Simple email regex for basic server-side validation
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

CORS_HEADERS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
}


def lambda_handler(event, context):
    # Handle CORS pre-flight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    # Parse body
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _error(400, "Invalid JSON in request body.")

    account_email = (body.get("email") or "").strip()
    reason        = (body.get("reason") or "Not provided").strip()

    # Validate
    if not account_email:
        return _error(400, "Email address is required.")
    if not EMAIL_RE.match(account_email):
        return _error(400, "Please provide a valid email address.")
    if len(reason) > 2000:
        return _error(400, "Reason must be 2000 characters or fewer.")

    # Publish to SNS topic – SNS delivers it to your subscribed email
    subject = "Account Deletion Request – Holiday Currency Converter"
    message = (
        f"A user has submitted an account deletion request.\n\n"
        f"Account Email : {account_email}\n"
        f"Reason        : {reason}\n\n"
        "Please process this request within 30 days."
    )

    try:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=subject,
            Message=message,
        )
    except ClientError as e:
        print(f"SNS error: {e.response['Error']['Message']}")
        return _error(502, "Failed to send request. Please try again later.")

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({"message": "Your deletion request has been received."}),
    }


def _error(status, message):
    return {
        "statusCode": status,
        "headers": CORS_HEADERS,
        "body": json.dumps({"error": message}),
    }
