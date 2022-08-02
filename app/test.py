import auth
import settings
import enums
import main


def test_sign():
    token = auth.get_token()
    address = auth.authenticate(token)
    assert address == settings.ADMIN_WALLET_ADDRESS


def test_authorize():
    role = auth.authorize(settings.ADMIN_WALLET_ADDRESS)
    assert role == enums.Roles.admin.value


def test_routing():
    paths = [
        '/market?symbol=BTCUSDT',
        '/market/asset/',
    ]
    for path in paths:
        service, _ = main.get_host(path)
        assert service == 'market'
