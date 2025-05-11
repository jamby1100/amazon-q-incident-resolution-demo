import boto3
import requests
from io import BytesIO
import os

class S3Gateway:
    @classmethod
    def upload_from_url(cls, url, bucket, key):
        payload = {}
        headers = {}

        print("I am reading from: ", url)
        response = requests.get(url, headers=headers, data=payload, verify=False)
        
        if response.status_code == 200:
            image_binary = response.content
            print("and the image bin is unshown")
            print("and the bucket is: ", os.getenv("PRODUCTS_BUCKET"))

            s3_client = boto3.client('s3')
            
            response = s3_client.put_object(
                Body=image_binary,
                Bucket=os.getenv("PRODUCTS_BUCKET"),
                Key=key,
            )