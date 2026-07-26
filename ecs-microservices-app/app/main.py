from fastapi import FastAPI, HTTPException
from mangum import Mangum
import boto3
import os

app = FastAPI(title="Serverless Microservices API")

def get_dynamodb_resource():
    # If executing inside LocalStack Lambda, use LOCALSTACK_HOSTNAME
    if "LOCALSTACK_HOSTNAME" in os.environ:
        host = os.environ["LOCALSTACK_HOSTNAME"]
        port = os.environ.get("EDGE_PORT", "4566")
        endpoint_url = f"http://{host}:{port}"
    else:
        # Fallback or local dev
        endpoint_url = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

    return boto3.resource(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name="us-east-1",
        aws_access_key_id="mock",
        aws_secret_access_key="mock"
    )

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Serverless FastAPI Microservice",
        "provider": "AWS Lambda + API Gateway"
    }

@app.get("/items/{item_id}")
def get_item(item_id: str):
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table("items-table")
        response = table.get_item(Key={"id": item_id})
        item = response.get("Item")
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@app.post("/items")
def create_item(payload: dict):
    if "id" not in payload or "name" not in payload:
        raise HTTPException(status_code=400, detail="Missing 'id' or 'name' in request payload")
    
    try:
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table("items-table")
        table.put_item(Item=payload)
        return {"message": "Item created successfully", "item": payload}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write error: {str(e)}")

# Mangum handler
handler = Mangum(app)