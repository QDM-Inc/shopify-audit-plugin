import hashlib
import hmac
import urllib

import jwt
import requests
from flask import request, redirect, current_app, abort

from shopify.routes import shopify_bp


@shopify_bp.route('/oauth/register', methods=['GET'])
def register_shopify_shop():
    if not is_valid_hmac(request.query_string.decode("utf-8")):
        abort(401)

    token_data = None
    try:
        encoded_token = request.args.get('state')
        token_data = jwt.decode(encoded_token, current_app.config['SHOPIFY_API_KEY'], algorithms='HS256')
    except Exception as err:
        abort(401)

    shop_url = request.args.get('shop')
    if token_data['shop_url'] != shop_url:
        abort(401)

    keys = {
        'client_id': current_app.config['SHOPIFY_API_KEY'],
        'client_secret': current_app.config['SHOPIFY_API_SECRET'],
        'code': request.args.get('code')
    }
    result = requests.post(f'https://{shop_url}/admin/oauth/access_token', json=keys)
    if result.status_code != 200:
        return result.content, 401

    access_token = result.json()['access_token']

    print(access_token)
    return redirect(f'https://{shop_url}/admin')


@shopify_bp.route('/oauth', methods=['GET'])
def authenticate_shopify():
    if not is_valid_hmac(request.query_string.decode("utf-8")):
        abort(401)

    shop_url = request.args.get('shop')
    token_payload = {'shop_url': shop_url}

    auth_url = build_shopify_auth_url(token_payload)
    return redirect(auth_url)


def is_valid_hmac(query_params):
    url_params = dict(urllib.parse.parse_qsl(query_params))
    hmac_value = request.args.get("hmac")

    del url_params['hmac']

    ordered_params = {k: url_params[k] for k in sorted(url_params)}
    ordered_qs = urllib.parse.urlencode(ordered_params)

    h = hmac.new(current_app.config["SHOPIFY_API_SECRET"].encode(), ordered_qs.encode(), digestmod=hashlib.sha256)
    return hmac.compare_digest(h.hexdigest(), hmac_value)


def build_shopify_auth_url(token_payload):
    encoded = jwt.encode(token_payload, current_app.config['SHOPIFY_API_KEY'], algorithm='HS256')

    query_params = urllib.parse.urlencode({
        'client_id': current_app.config["SHOPIFY_API_KEY"].encode(),
        'scope': 'read_orders,read_checkouts,read_customers,read_products,read_marketing_events',
        'redirect_uri': f'{current_app.config["SHOPIFY_OAUTH_REDIRECT_URI_HOST"]}/shopify/oauth/register',
        'state': encoded,
        'grant_options[]': 'value'
    })
    url_parts = urllib.parse.ParseResult(scheme='https', netloc=token_payload['shop_url'], path='admin/oauth/authorize',
                                         query=query_params, params='', fragment='')

    return urllib.parse.urlunparse(url_parts)
