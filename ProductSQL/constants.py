from secrets import token_hex

DB_URL = "mysql+pymysql://root:@localhost/products"
DB_SECRET_KEY = token_hex(16)

SORT_ORDER_VALUES = ['ASC', 'DESC']

# Pagination and sorting defaults
DEFAULT_LIMIT = 30
DEFAULT_OFFSET = 0
DEFAULT_SORT_BY = 'barcode'
DEFAULT_SORT_ORDER = 'ASC'

# Success messages
SCC_200_OK = dict(status_code=200, message="Operation successful")
SCC_201_CREATED = dict(status_code=201, message="Operation successful")

# Error messages
ERR_400_CLIENT = dict(status_code=400, message="Operation failed, Client Error due to invalid request")
ERR_404_NOT_FOUND = dict(status_code=404, message="Operation failed, Product(s) not found")
ERR_409_EXISTS = dict(status_code=409, message="Operation failed, Product already exists")
ERR_500_INTERNAL = dict(status_code=500, message="Operation failed, Internal Server Error")
