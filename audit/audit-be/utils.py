import requests

# from app import baseURL, apiVersion

baseURL = 'data-oauth-store.myshopify.com'
apiVersion = 'admin/api/2021-10'

def get_response_by_parameter(parameter):
    headers={'Host': baseURL,'X-Shopify-Access-Token': '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','Content-Type': 'application/json'}
    response = requests.get(f'https://{baseURL}/{apiVersion}/{parameter}', headers=headers)
    return response.json()
