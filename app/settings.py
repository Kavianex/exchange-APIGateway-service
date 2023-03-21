import os

ADMIN_WALLET_ADDRESS = os.getenv(
    'ADMIN_WALLET_ADDRESS',
    ''
).lower()
TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXPIRE_TIME', 4 * 3600 * 1000))
APIKEY_EXPIRE_TIME = int(
    os.getenv('APIKEY_EXPIRE_TIME', 370 * 24 * 3600 * 1000))
SERVICE_HOSTS = {
    "api": os.getenv('API_HOST', 'http://127.0.0.1:8002'),
}
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(',')
