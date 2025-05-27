import json
import os
import uuid
from gateways.dynamodb_gateway import DynamodbGateway
from gateways.s3_gateway import S3Gateway
from gateways.http_gateway import HttpGateway
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch all supported libraries for X-Ray tracing
patch_all()

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
    
    # Add inventory for the product
    inventory_url = os.getenv("INVENTORY_SERVICE_URL", "http://localhost:5000") + "/inventory"
    inventory_data = {
        "sku": item_data["id"],
        "quantity": body.get("initial_quantity", 0)
    }
    
    # Only make the request if there's inventory to add
    if inventory_data["quantity"] > 0:
        print("calling the inventory...")
        print("Inventory_url: ", inventory_url)
        print("inventory_data: ", inventory_data)
        print("=====")
        HttpGateway.post(inventory_url, inventory_data)
    else:
        print("no qty")

    response = {"statusCode": 200, "body": json.dumps(item_data)}

    return response

def get_products(event, context):
    items = DynamodbGateway.get_all_items(os.getenv("PRODUCTS_TABLE"))
    response = {"statusCode": 200, "body": json.dumps(items)}

    return response