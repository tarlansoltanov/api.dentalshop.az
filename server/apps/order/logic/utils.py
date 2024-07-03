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
                    "Merchant": config("BANK_MERCHANT"),
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
        config("BANK_URL"),
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

    subject = f"Yeni Sifariş №{order.id}"

    body = "<h1>Yeni sifarişiniz var.</h1>"

    body += "<style>"
    body += "table { border-collapse: collapse; width: 100%; border: 1px solid #ddd; }"
    body += "th, td { text-align: left; padding: 8px; }"
    body += "th { background-color: #f2f2f2; }"
    body += "a[role='button'] { background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }"  # noqa: E501
    body += "</style>"

    body += "</br>"

    body += f"Sifariş №{order.id}"

    body += "</br></br>"

    body += "<table> <tr> <th>Məhsul</th> <th>Qiymət</th> <th>Ədəd</th> <th>Toplam</th> </tr>"

    for item in order.items.all():
        body += "<tr>"
        body += f"<td>{item.product.name}</td>"
        body += f"<td>{item.price:.2f} AZN</td>"
        body += f"<td>{item.quantity} ədəd</td>"
        body += f"<td>{item.get_total():.2f} AZN</td>"
        body += "</tr>"

    body += "</table>"

    body += "</br>"
    body += f"\nToplam: {order.get_total()} AZN"
    body += "</br>"
    body += f"\nÖdəmə Tipi: {order.get_payment_method_display()}"
    body += "</br></br>"

    body += "<hr>"

    body += "</br>"
    body += f"\nMüştəri: {order.user.first_name} ({order.user.last_name})"
    body += "</br>"
    body += f"\nƏlaqə: <a href='tel:+994{order.user.phone}'>+994{order.user.phone}</a>"
    body += "</br>"
    body += f"\nÜnvan: {order.address}"
    body += "</br>"
    body += f"\nQeyd: {order.note}"
    body += "</br></br>"

    body += "<hr></br>"

    body += (
        f"<a role='button' href='https://api.dentalshop.az/admin/order/order/{order.id}/change/'>Sifariş detalları</a>"
    )

    recipients = ["info@dentalshop.az"]

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        html_message=body,
    )
