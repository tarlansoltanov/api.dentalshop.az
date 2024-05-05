from hashlib import md5

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context  # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken

from server.apps.user.models import User
from server.settings.components import config


class CustomAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers="ALL:@SECLEVEL=1")
        kwargs["ssl_context"] = context
        return super(CustomAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers="ALL:@SECLEVEL=1")
        kwargs["ssl_context"] = context
        return super(CustomAdapter, self).proxy_manager_for(*args, **kwargs)


def send_otp_code(user: User) -> None:
    """Send OTP code to user phone number."""
    data = {
        "login": config("SMS_LOGIN"),
        "key": md5(config("SMS_PASSWORD").encode()).hexdigest(),
        "sender": config("SMS_SENDER"),
        "scheduled": "NOW",
        "text": f"Sizin OTP kodunuz: {user.generate_otp_code()}",
        "msisdn": f"994{user.phone}",
        "unicode": 0,
    }

    with requests.Session() as session:
        session.mount("https://", CustomAdapter())
        response = session.post("https://click.atlsms.az/index.php?app=json_api_send", json=data)
        response.raise_for_status()

    trans_id = response.json()["transId"]

    if int(trans_id) < 0:
        raise ValueError(f"Something went wrong. Error code: {trans_id}")

    user.otp_trans_id = trans_id
    user.save()


def get_token_pair(user: User) -> dict:
    """Get token pair for user."""
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
