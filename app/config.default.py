# Do not change the values below!
# If a change is required copy appropriate lines to the /local/config.local.py file and change the values there.

SECRET_KEY = 'please_change_@187%0^&'

# Email config
EMAIL_ADDRESS = 'test@test.com'
EMAIL_PASSWORD = 'test'
EMAIL_SALT = '...'
EMAIL_SECRET = '...'

# MySQL connection
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB_NAME = 'test'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'

# MongoDB connection
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB_NAME = 'test'

MONGODB_AUTH_ENABLED = False

# used only if MONGODB_AUTH_ENABLED = True
MONGODB_USER = 'root'
MONGODB_PASSWORD = 'root'


# Admin credentials - db init
ADMIN_EMAIL = 'admin@admin.com'
ADMIN_PASSWORD = 'admin'

# Customer credentials - db init
CUSTOMER_EMAIL = 'customer@customer.com'
CUSTOMER_PASSWORD = 'customer'

# Security
SECURITY_PASSWORD_SALT = '9873313545127551081313677346265396239529'

SECURITY_FLASH_MESSAGES = True
SECURITY_PASSWORD_LENGTH_MIN = 8

SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_POST_LOGOUT_VIEW = '/'

SECURITY_CHANGEABLE = True
SECURITY_POST_CHANGE_VIEW = '/'
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = \
    'Telco Client Context Aggregation Service - Your password has been changed'

SECURITY_REGISTERABLE = False
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = False
SECURITY_TWO_FACTOR = False
SECURITY_TWO_FACTOR_REQUIRED = False
SECURITY_UNIFIED_SIGNIN = False
SECURITY_PASSWORDLESS = False
SECURITY_TRACKABLE = True
SECURITY_WEBAUTHN = False
SECURITY_MULTI_FACTOR_RECOVERY_CODES = False
