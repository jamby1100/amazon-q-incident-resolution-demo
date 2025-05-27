import requests
import os
import json

class HttpGateway:
    @staticmethod
    def post(url, data):
        """
        Make a POST request to the specified URL with the given data
        
        Args:
            url (str): The URL to send the POST request to
            data (dict): The data to send in the request body
            
        Returns:
            tuple: (response_data, status_code)
        """
        try:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500