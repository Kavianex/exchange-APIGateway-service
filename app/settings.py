import os

TEST_PRIVATE_KEY = os.getenv(
    'TEST_PRIVATE_KEY',
    'b25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364'
)
ADMIN_WALLET_ADDRESS = os.getenv(
    'ADMIN_WALLET_ADDRESS',
    '0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E'
).lower()
TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXPIRE_TIME', 4 * 60 * 60 * 1000))
SERVICE_HOSTS = {
    "market": os.getenv('MARKET_HOST', 'http://127.0.0.1:8001'),
    "engine": os.getenv('ENGINE_HOST', 'http://127.0.0.1:8002'),
}
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8000))
