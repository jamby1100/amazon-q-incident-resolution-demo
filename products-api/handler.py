import json
import os
import uuid
from gateways.dynamodb_gateway import DynamodbGateway
from gateways.s3_gateway import S3Gateway

def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def create_product(event, context):
    body = json.loads(event["body"])

    # Validate required fields
    if "image" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Image URL is required for this request"})
        }
    
    # Ensure product has an ID
    if "id" not in body:
        body["id"] = str(uuid.uuid4())

    response, item_data = DynamodbGateway.create_item(os.getenv("PRODUCTS_TABLE"), body)

    S3Gateway.upload_from_url(body["image"], os.getenv("S3_BUCKET_NAME"), item_data["id"])

    response = {"statusCode": 200, "body": json.dumps(item_data)}

    return response

def get_products(event, context):
    items = DynamodbGateway.get_all_items(os.getenv("PRODUCTS_TABLE"))
    response = {"statusCode": 200, "body": json.dumps(items)}

    return response