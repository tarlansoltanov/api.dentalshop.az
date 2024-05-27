import requests
import xmltodict
from django.conf import settings
from django.core.mail import send_mail

from server.apps.order.models import Order
from server.apps.promo.models import Promo
from server.settings.components import config


def get_discount(code: str, order: Order) -> int:
    """Get discount for user."""
    if not code:
        return 0

    if code == order.user.code:
        return order.user.discount

    promo = Promo.objects.filter(code=code).first()

    if not promo or not promo.is_valid() or promo.is_used(order.user):
        return 0

    promo.usages.create(order=order)
    return promo.discount


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


def send_new_order_email(order: Order):
    """Send email notification to the admin about new order."""

    subject = f"Yeni Satış №{order.id}"
    body = f"Yeni satış №{order.id} yaradıldı."

    body += "\n\nMəhsullar:"
    for item in order.items.all():
        body += f"\n{item.product.name} - {item.quantity} ədəd"

    body += f"\n\nToplam: {order.get_total()} AZN"

    recipients = ["info@dentalshop.az"]

    send_mail(subject=subject, message=body, from_email=settings.EMAIL_HOST_USER, recipient_list=recipients)
