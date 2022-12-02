"""
variables for login.py
"""
# app secret key
SECRETKEY_KEY='secret_key'

# for oatuh setup
GOOGLE_CLIENT_ID_KEY='GOOGLE_CLIENT_ID'
GOOGLE_CLIENT_SECRET_KEY='GOOGLE_CLIENT_SECRET'
OAUTHLIB_INSECURE_TRANSPORT_KEY='OAUTHLIB_INSECURE_TRANSPORT'
OAUTHLIB_RELAX_TOKEN_SCOPE_KEY='OAUTHLIB_RELAX_TOKEN_SCOPE'
BLUE_PRINT_SCOPE_PROFILE='profile'
BLUE_PRINT_SCOPE_EMAIL='email'

# for google data
GOOGLE_DATA_KEY='google_data'
GOOGLE_ID_KEY='id'
GOOGLE_EMAIL_KEY='email'
GOOGLE_NAME_KEY='name'

# for google url
GOOGLE_LOGIN='google.login'

# google endpoints
GOOGLE_USER_INFO_ENDPOINT='/oauth2/v2/userinfo'
GOOGLE_REVOKE_TOKEN_URL='https://accounts.google.com/o/oauth2/revoke'

# google token keys
GOOGLE_ACCESS_TOKEN_KEY='access_token'

# for sql
SQL_ROW_COUNT_KEY='count(*)'
SQL_COUNT_USER_QUERY='select count(*) from user where user_id = {}'