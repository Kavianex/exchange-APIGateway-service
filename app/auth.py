from web3.auto import w3
from fastapi import HTTPException
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
import time
import enums
import settings


class AuthException(Exception):
    def __init__(self, name: str):
        self.name = name


def authenticate(authorization: str) -> str:
    wallet_address = ''
    try:
        message, signature = authorization.split(' ')
        now = int(time.time() * 1000)
        info = message.split(':')
        wallet = info[0]
        expire = info[1]
        expire = int(expire)
        time_to_expire = expire - now
        if len(info) > 2 and info[2] == 'APIKEY':
            not_expired = 0 < time_to_expire < settings.APIKEY_EXPIRE_TIME
        else:
            not_expired = 0 < time_to_expire < settings.TOKEN_EXPIRE_TIME
        if not_expired:
            wallet_address = get_address(
                message=message,
                signature=signature
            ).lower()
            if not wallet == wallet_address:
                raise AuthException('InvalidSignature')
        else:
            raise AuthException("TokenExpired")
    except Exception as e:
        if isinstance(e, AuthException):
            raise HTTPException(401, e.name)
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
