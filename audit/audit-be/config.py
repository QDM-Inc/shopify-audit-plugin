class Config(object):
    DEBUG = False
    TESTING = False

    SHOPIFY_API_KEY = 'b0cee3776ce1be45f9ca2b9cbe3671b9'
    SHOPIFY_API_SECRET = '49df7c278c33c22971fe812f1be9fcc4'
    SHOPIFY_OAUTH_REDIRECT_URI_HOST = 'https://8d23-2a06-5b00-cff-ee00-60c2-4813-43cf-e555.ngrok.io'
    ACCESS_TOKEN = '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'


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True