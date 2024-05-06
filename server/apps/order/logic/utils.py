import requests
import xmltodict

from server.apps.order.models import Order
from server.apps.user.models import User
from server.settings.components import config


def get_discount(code: str, user: User) -> int:
    """Get discount for user."""
    discount = 0

    if code == user.code:
        discount = user.discount

    return discount


def get_xml_request_order(
    redirect_url: str,
    amount: int,
    installments: int = 0,
    merchant: str = "E1000010",
    language: str = "AZ",
) -> dict:
    """Get XML request for payment order."""
    data = {
        "TKKPG": {
            "Request": {
                "Operation": "CreateOrder",
                "Language": language,
                "Order": {
                    "OrderType": "Purchase",
                    "Merchant": merchant,
                    "Amount": int(amount * 100),
                    "Currency": "944",
                    "Description": f"TAKSIT={installments}" if installments > 0 else "xxxxxxxx",
                    "ApproveURL": f"{redirect_url}?status=approved",
                    "CancelURL": f"{redirect_url}?status=canceled",
                    "DeclineURL": f"{redirect_url}?status=declined",
                },
            }
        }
    }

    xml = xmltodict.unparse(data)

    return xml


def send_payment_order(url: str, order: Order, installments: int = 0) -> dict:
    """Send payment order to bank."""
    xml = get_xml_request_order(url, order.get_total(), installments)

    response = requests.post(
        "https://tstpg.kapitalbank.az:5443/Exec",
        data=xml,
        cert=(config("BANK_CERT"), config("BANK_KEY")),
        allow_redirects=True,
        verify=False,
    )

    data = xmltodict.parse(response.text)

    return data["TKKPG"]["Response"]["Order"]


def get_payment_redirect_url(url: str, order: Order, installments: int) -> str:
    """Get payment redirect URL."""
    response = send_payment_order(url, order, installments)

    order.payments.create(
        bank_session_id=response["SessionID"],
        bank_order_id=response["OrderID"],
        installments=installments,
    )

    return f'{response["URL"]}?ORDERID={response["OrderID"]}&SESSIONID={response["SessionID"]}'


def format_xml_response(data: str) -> dict:
    """Format XML response."""
    return xmltodict.parse(data)
