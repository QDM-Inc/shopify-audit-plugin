from flask import Blueprint

shopify_bp = Blueprint(
    'shopify_bp', __name__,
    url_prefix='/shopify',
    template_folder='templates',
    static_folder='static',
    cli_group='shopify'
)

from . import oauth
