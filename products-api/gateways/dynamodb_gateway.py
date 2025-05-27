import boto3
import uuid
from datetime import datetime
from decimal import Decimal
import json

class DynamodbGateway:
    @classmethod
    def convert_floats(cls, obj):
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: cls.convert_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [cls.convert_floats(elem) for elem in obj]
        else:
            return obj
            
    @classmethod
    def convert_decimals(cls, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: cls.convert_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [cls.convert_decimals(elem) for elem in obj]
        else:
            return obj
        
    @classmethod
    def get_all_items(cls, table_name):
        """
        Retrieves all items from the DynamoDB table using the table name.
        """
        # Get the table resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        # Scan the table to get all items
        response = table.scan()
        
        # Convert Decimal values to float for JSON serialization
        items = cls.convert_decimals(response['Items'])

        # Return the items
        return items
    
    @classmethod
    def create_item(cls, table_name, item_data):
        """
        Creates a new item in the DynamoDB table using the table name.
        """
        # Get the table resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        # Add a unique ID and timestamp if not provided
        if 'id' not in item_data:
            item_data['id'] = str(uuid.uuid4())
        
        if 'createdAt' not in item_data:
            item_data['createdAt'] = datetime.now().isoformat()
        
        # Convert floats to Decimal for DynamoDB
        dynamo_item = cls.convert_floats(item_data)
        
        # Put the item in the table
        response = table.put_item(Item=dynamo_item)
        
        # Convert any Decimal values back to float for JSON serialization
        serializable_item = cls.convert_decimals(item_data)
        
        return response, serializable_item