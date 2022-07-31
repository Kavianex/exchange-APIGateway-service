from web3.auto import w3
from fastapi import HTTPException
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
import time
try:
    from app import enums, settings
except ImportError:
    import enums
    import settings


def authenticate(authorization: str) -> str:
    wallet_address = ''
    try:
        message, signature = authorization.split(' ')
        now = int(time.time() * 1000)
        wallet, expire = message.split(':')
        expire = int(expire)
        time_to_expire = expire - now
        if 0 < time_to_expire < settings.TOKEN_EXPIRE_TIME:
            wallet_address = get_address(
                message=message,
                signature=signature
            ).lower()
            if not wallet == wallet_address:
                raise Exception('InvalidSignature')
        else:
            raise Exception("TokenExpired")
    except Exception as e:
        if wallet_address:
            raise HTTPException(401, str(e))
        raise HTTPException(401, 'InvalidFormat')
    return wallet_address


def authorize(wallet_address: str) -> str:
    if not wallet_address:
        role = enums.Roles.visitor.value
    elif wallet_address == settings.ADMIN_WALLET_ADDRESS:
        role = enums.Roles.admin.value
    else:
        role = enums.Roles.user.value
    return role


def sign(message: str, private_key: str) -> str:
    message = encode_defunct(text=message)
    private_key = bytes(HexBytes(private_key))
    return w3.eth.account.sign_message(
        message,
        private_key=private_key
    ).signature.hex()


def get_address(message, signature):
    message = encode_defunct(text=message)
    signature = HexBytes(signature)
    address = w3.eth.account.recover_message(message, signature=signature)
    return address


def get_token(wallet: str = settings.ADMIN_WALLET_ADDRESS, private_key: str = settings.TEST_PRIVATE_KEY) -> str:
    expire = int(time.time() * 1000) + settings.TOKEN_EXPIRE_TIME
    message = f"{wallet.lower()}:{expire}"
    signature = sign(message=message, private_key=private_key)
    return f"{message} {signature}"


if __name__ == "__main__":
    token = get_token()
    print(token)
