import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response_map200 import InlineResponseMap200  # noqa: E501
from swagger_server.models.order_body import OrderBody  # noqa: E501
from swagger_server.models.orderstatus_body import OrderstatusBody  # noqa: E501
from swagger_server.models.paymentoptions_body import PaymentoptionsBody  # noqa: E501
from swagger_server.models.quote_body import QuoteBody  # noqa: E501
from swagger_server.models.session_body import SessionBody  # noqa: E501
from swagger_server.models.withdrawal_body import WithdrawalBody  # noqa: E501
from swagger_server import util
from flask import jsonify
import logging
logging.basicConfig(level=logging.INFO)




def features_get():  # noqa: E501
    """Get supported features

    Endpoint to retrieve supported features # noqa: E501


    :rtype: InlineResponse200
    """

    object_to_return = {
        "supported_features": [
            {
                "estimates": True,
                "on_chain_fallback": False,
                "quotes": True,
                "webhook": True
            },
            {
                "estimates": True,
                "on_chain_fallback": False,
                "quotes": True,
                "webhook": True
            }
        ]
    }

    return jsonify (object_to_return)


def order_post(body):  # noqa: E501
    """Create an order

    Confirm an order from quote and get payment information in return # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2004
    """
    if connexion.request.is_json:
        body = OrderBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info(f"Received order data: {body}")


        object_to_return = {
            "amount_fiat": 100000,
            "amount_sats": 800000,
            "currency_id": 1,
            "expires_on": "2023-09-20T00:25:11.123000+00:00",
            "order_id": "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",
            "order_status": "placed",
            "payment_info": "",
            "payment_option_id": 1
        }


        return jsonify(object_to_return)
    return 'Something went wrong'


def order_status_post(body):  # noqa: E501
    """Get order status

    This endpoint returns the status of one or more orders based on the session and order ID. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Dict[str, InlineResponseMap200]
    """
    if connexion.request.is_json:
        body = OrderstatusBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def payment_options_post(body):  # noqa: E501
    """Get payment options

    This endpoint provides a list of payment options for different currencies, filtered by an optional currency code. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2006
    """
    if connexion.request.is_json:
        body = PaymentoptionsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def quote_post(body):  # noqa: E501
    """Get a quote or estimate

    Get a an quote or estimate from the provider based on amount of fiat you want to spend # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2003
    """
    if connexion.request.is_json:
        body = QuoteBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def session_post(body):  # noqa: E501
    """Start a session

    Start a session with optional signed proof of ownership. If Proof of Ownership is not required signature can be a random alphanumeric value. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2002
    """
    if connexion.request.is_json:
        body = SessionBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def verify_get():  # noqa: E501
    """Provides token for authentication

    Request a token to be signed by the reciever node as proof of ownership # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def withdrawal_post(body):  # noqa: E501
    """Initiate a withdrawal

    Request lnurlw from the provider. User can provide optional fallback onchain address which will be used if the withdrawal is not claimed before the expiration date # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2005
    """
    if connexion.request.is_json:
        body = WithdrawalBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
