import boto3
import uuid
from datetime import datetime

class DynamodbGateway:
    def get_all_items(table_name):
        """
        Retrieves all items from the DynamoDB table using the table name.
        """
        # Get the table resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        # Scan the table to get all items
        response = table.scan()

        # Return the items
        return response['Items']
    
    def create_item(table_name, item_data):
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
        
        # Put the item in the table
        response = table.put_item(Item=item_data)
        
        return response, item_data