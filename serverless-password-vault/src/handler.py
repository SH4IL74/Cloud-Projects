import json
import os
import random
import string
import time
import uuid
import boto3

# Detect LocalStack environment endpoint
endpoint_url = os.environ.get("AWS_ENDPOINT_URL")
if not endpoint_url and os.environ.get("LOCALSTACK_HOSTNAME"):
    endpoint_url = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
    endpoint_url=endpoint_url,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test")
)

TABLE_NAME = os.environ.get("TABLE_NAME", "vault-records")
table = dynamodb.Table(TABLE_NAME)


def generate_password(length=16, use_uppercase=True, use_digits=True, use_symbols=True):
    characters = list(string.ascii_lowercase)
    guaranteed = [random.choice(string.ascii_lowercase)]

    if use_uppercase:
        characters.extend(string.ascii_uppercase)
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_digits:
        characters.extend(string.digits)
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        characters.extend(symbols)
        guaranteed.append(random.choice(symbols))

    remaining_length = max(0, length - len(guaranteed))
    random_chars = [random.choice(characters) for _ in range(remaining_length)]

    password_list = guaranteed + random_chars
    random.shuffle(password_list)
    return "".join(password_list)


def evaluate_strength(password):
    score = 0
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1

    if score >= 4:
        return "STRONG"
    elif score >= 2:
        return "MEDIUM"
    return "WEAK"


def lambda_handler(event, context):
    try:
        http_method = event.get("httpMethod", "")
        path = event.get("path", "")

        # 1. POST /generate
        if http_method == "POST" and "generate" in path:
            body = {}
            raw_body = event.get("body")
            if raw_body:
                try:
                    body = json.loads(raw_body)
                except Exception:
                    body = {}

            length = int(body.get("length", 16))
            use_upper = bool(body.get("use_uppercase", True))
            use_digits = bool(body.get("use_digits", True))
            use_symbols = bool(body.get("use_symbols", True))
            label = str(body.get("label", "Default-Secret"))

            generated_pwd = generate_password(length, use_upper, use_digits, use_symbols)
            strength = evaluate_strength(generated_pwd)
            record_id = str(uuid.uuid4())
            created_at = int(time.time())

            # Save to DynamoDB
            table.put_item(
                Item={
                    "id": record_id,
                    "label": label,
                    "length": length,
                    "strength": strength,
                    "created_at": created_at
                }
            )

            return {
                "statusCode": 201,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "id": record_id,
                    "label": label,
                    "generated_password": generated_pwd,
                    "strength": strength,
                    "length": length,
                    "created_at": created_at,
                    "message": "Password generated and metadata stored in DynamoDB successfully!"
                })
            }

        # 2. GET /passwords
        elif http_method == "GET" and "passwords" in path:
            response = table.scan()
            items = response.get("Items", [])

            # Convert DynamoDB Decimal types if needed
            for item in items:
                if "created_at" in item:
                    item["created_at"] = int(item["created_at"])
                if "length" in item:
                    item["length"] = int(item["length"])

            return {
                "statusCode": 200,
                "isBase64Encoded": False,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"records": items})
            }

        # 3. Default Fallback
        return {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"status": "Serverless Password Vault is Live!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }