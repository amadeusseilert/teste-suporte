
class DevelopmentConfig(object):

    DEBUG = True
    SECRET_KEY = b'\xf3\xf6\xab<\xaeya\xbew\x85\xc1\xf8\x1e\x8e\x8b\xba\x9f\x01\x8f\x05\xbe\x18fZ'
    TESTING = True
    MONGODB_SETTINGS = {'DB': 'user-share'}

    OAUTH_CREDENTIALS = {
        'google': {
            'id': '462256152095-346iqu6hl7l6n04usgkisv6nn9ns33ku.apps.googleusercontent.com',
            'secret': 'Cf_C4MN57srY7WWvXihWp9fE'
        }
        # Add other providers...
    }


class DevelopmentTestingConfig(DevelopmentConfig):
    SERVER_NAME = '127.0.0.1:5000'
    MONGODB_SETTINGS = {'DB': 'user-share-test'}
