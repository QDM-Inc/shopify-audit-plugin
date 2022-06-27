import requests

# from app import baseURL, apiVersion
from flask import current_app

baseURL = 'kyc-test-store.myshopify.com'
apiVersion = 'admin/api/2021-10'

def get_response_by_parameter(parameter):
    headers={'Host': baseURL,'X-Shopify-Access-Token': current_app.config["ACCESS_TOKEN"],'Content-Type': 'application/json'}
    response = requests.get(f'https://{baseURL}/{apiVersion}/{parameter}', headers=headers)
    return response.json()
