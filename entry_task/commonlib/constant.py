import os


PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
STATIC_URL = PROJECT_PATH + '/static/'

OK = 0
BAD_REQUEST = 1
UNAUTHORIZED = 2

TOKEN_TIME = 7200

