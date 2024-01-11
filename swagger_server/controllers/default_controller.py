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
from datetime import datetime, timedelta
import logging
logging.basicConfig(level=logging.INFO)

def features_get():  # noqa: E501
    """Get supported features

    Endpoint to retrieve supported features # noqa: E501

    :rtype: InlineResponse200
    """

    #todo: find out if we can support multiple options (for example with and without estimates)
    response = InlineResponse200(supported_features=[
        {"estimates": True, "on_chain_fallback": False, "quotes": True, "webhook": True},
        {"estimates": True, "on_chain_fallback": False, "quotes": False, "webhook": True}
    ])
    return jsonify(response)

def order_post(body):  # noqa: E501
    """Create an order

    Confirm an order from quote and get payment information in return # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2004
    """
    if connexion.request.is_json:
        body = OrderBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info(f"Received post data to /order data: {body}")
        logging.info(f"quote_id: {body.quote_id}")
        logging.info(f"session_id: {body.session_id}")
        logging.info(f"webhook_url: {body.webhook_url}")

        #todo: fetch quote from external source. hardcoded for now.

        expires_on = datetime.utcnow() + timedelta(minutes=+5)
        expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        quote = InlineResponse2003(
            quote_id="9ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",
            amount_fiat=100000,
            currency_id=1,
            payment_option_id=1,
            amount_sats=800000,
            is_estimate=False,
            btc_price=6942000,
            order_fee=0,
            expires_on=expires_on_formatted
        )

        #todo: generate an order_id (or consider reusing the quote_id?)
        order_id = "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6"

        # Check if the quote is still valid
        try:
            expiration_date = datetime.strptime(quote.expires_on, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            current_time = datetime.now()

            # Compare the current time with the expiration time
            assert current_time < expiration_date
        except Exception as e:
            logging.error(f"Error validating quote: {e}")
            return f"Error validating quote: {e}"

        if quote.is_estimate:
            # todo: fetch the btc_price that we will actually use
            btc_price=6942000
            amount_fiat=1
            amount_sats=1
            logging.info (f"This quote was an estimate {quote.btc_price}. The order was created with price {btc_price}. amount_fiat {amount_fiat}. amount_sats {amount_sats}")
        else:
            btc_price=quote.btc_price
            amount_fiat=quote.amount_fiat
            amount_sats=quote.amount_sats
            logging.info (f"This order was a fixed quote. The order was created with price {btc_price}. amount_fiat {amount_fiat}. amount_sats {amount_sats}")

        test=payment_info_post()
        response = InlineResponse2004(
            order_id=order_id,
            order_status="placed",
            amount_fiat=amount_fiat,
            currency_id=quote.currency_id,
            payment_option_id=quote.payment_option_id,
            amount_sats=quote.amount_sats,
            expires_on=quote.expires_on,
            payment_info=test
# Add the necessary payment info here
            #payment_info={  # Add the necessary payment info here
            #    # Example: "payment_method": "bank_transfer"
            #}
        )
        return jsonify(response)
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
        logging.info(f"Received post data to /order-status data: {body}")
        logging.info(f"order_id: {body.order_id}")
        logging.info(f"session_id: {body.session_id}")

        orders = {}

        #todo: fetch orders based on order_id
        if (body.order_id == '8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6'):
            logging.info(f"order_id: {body.order_id} found.")
            orders[body.order_id] = InlineResponseMap200(amount_fiat=100000, currency_id=1, payment_option_id=1, amount_sats=800000, btc_price=6942000, order_fee=0, order_status="finished", order_status_date=datetime.strptime("2023-09-20T00:25:11.123Z", "%Y-%m-%dT%H:%M:%S.%fZ"))

        #todo: fetch orders based on session_id
        if (body.session_id == 'd7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5'):
            logging.info(f"session_id: {body.session_id} found.")
            orders['8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6'] = InlineResponseMap200(amount_fiat=100000, currency_id=1, payment_option_id=1, amount_sats=800000, btc_price=6942000, order_fee=0, order_status="finished", order_status_date=datetime.strptime("2023-09-20T00:25:11.123Z", "%Y-%m-%dT%H:%M:%S.%fZ"))
            orders['00000000-0000-0000-0000-000000000000'] = InlineResponseMap200(amount_fiat=100000, currency_id=1, payment_option_id=1, amount_sats=800000, btc_price=6942000, order_fee=0, order_status="finished", order_status_date=datetime.strptime("2023-09-20T00:25:11.123Z", "%Y-%m-%dT%H:%M:%S.%fZ"))
            orders['00000000-0000-0000-0000-000000000001'] = InlineResponseMap200(amount_fiat=100000, currency_id=1, payment_option_id=1, amount_sats=800000, btc_price=6942000, order_fee=0, order_status="finished", order_status_date=datetime.strptime("2023-09-20T00:25:11.123Z", "%Y-%m-%dT%H:%M:%S.%fZ"))

        #todo: handle case where session id and/or order id is wrong
        return jsonify(orders)

    return 'Something went wrong'


def payment_options_post(body):  # noqa: E501
    """Get payment options

    This endpoint provides a list of payment options for different currencies, filtered by an optional currency code. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2006
    """
    response = InlineResponse2006(
        currencies=[
            {
                "eur": {
                    "currency_code": "EUR",
                    "currency_id": 1,
                    "payment_options": [
                        {
                            "fee_rate": 0.005,
                            "id": 1,
                            "max_amount": 100000,
                            "min_amount": 1000,
                            "option": "SEPA"
                        }
                    ]
                }
            }
        ]
    )
    if connexion.request.is_json:
        body = PaymentoptionsBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info(f"Received post data to /payment-options data: {body}")
        logging.info(f"currency_code: {body.currency_code}")
        logging.info(f"session_id: {body.session_id}")

        return jsonify(response.to_dict())
    #return the payments options even if the post data is invalid or not json
    return jsonify(response.to_dict())


def quote_post(body):  # noqa: E501
    """Get a quote or estimate

    Get a an quote or estimate from the provider based on amount of fiat you want to spend # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2003
    """
    if connexion.request.is_json:
        body = QuoteBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info(f"Received post data to /quote data: {body}")
        logging.info(f"currency_id: {body['currency_id']}")
        logging.info(f"payment_option_id: {body['payment_option_id']}")
        logging.info(f"session_id: {body['session_id']}")

        #todo: generate and persist an actual quote
        # $50000 = 1 BTC
        btc_price=(50000*100) # in cents
        sat_price = btc_price / 100000000

        is_estimate = False
        order_fee=0 # in cents
        currency_id = 1
        payment_option_id = 1
        
        quote_id = "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6"

        if body.get('amount_btc') and not body.get('amount_fiat'):
            logging.info(f"amount_fiat: {body['amount_btc']}")
            print(f"{body['session_id']} is asking for a quote to exchange {body['amount_btc']} BTC and get currency_id {body['currency_id']}")
            #todo: consider fees
            amount_sats=body['amount_btc']
            amount_fiat = amount_sats * sat_price # in cents
        elif body.get('amount_fiat') and not body.get('amount_btc'):
            #todo: consider fees
            amount_fiat=body['amount_fiat']
            amount_sats = amount_fiat / sat_price
            print(f"{body['session_id']} is asking for a quote to exchange {body['amount_fiat']} currency_id {body['currency_id']} and get BTC")
        else:
            raise ValueError("Error: Either both or none of the values are present")

        #Enforce limits
        #todo get limits from : payment_options_post
        #check that order size is within a $10 or 10000 sats for testing
        max_this_amount_of_euro=10
        fiat_limit = max_this_amount_of_euro * 100 # in cents

        bitcoin_limit = 0.00010000
        sat_limit = bitcoin_limit * 100000000

        if (amount_fiat > fiat_limit):
            return f"Something went wrong: amount_fiat is greater than {fiat_limit}"
        if (amount_sats > sat_limit):
            return f"Something went wrong: amount_sats is greater than {sat_limit}"

        expires_on = datetime.utcnow() + timedelta(minutes=5)
        expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        quote = InlineResponse2003(
            quote_id=quote_id,
            amount_fiat=amount_fiat,
            currency_id=currency_id,
            payment_option_id=payment_option_id,
            amount_sats=amount_sats,
            is_estimate=is_estimate,
            btc_price=btc_price,
            order_fee=order_fee,
            expires_on=expires_on_formatted
        )
        return jsonify(quote)
    return 'Something went wrong'


def session_post(body):  # noqa: E501
    """Start a session

    Start a session with optional signed proof of ownership. If Proof of Ownership is not required signature can be a random alphanumeric value. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2002
    """
    if connexion.request.is_json:
        body = SessionBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info(f"Received post data to /session data: {body}")
        logging.info(f"app_id: {body.app_id}")
        logging.info(f"node_pubkey: {body.node_pubkey}")
        logging.info(f"session_id: {body.session_id}")
        logging.info(f"signature: {body.signature}")

        app_id = "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",

        expires_on = datetime.utcnow() + timedelta(minutes=60)
        expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        object_to_return = { "app_id": app_id, "expires_on": expires_on_formatted, "session_id": body.session_id }
        return jsonify(object_to_return)
    return 'Something went wrong'


def verify_get():  # noqa: E501
    """Provides token for authentication

    Request a token to be signed by the reciever node as proof of ownership # noqa: E501


    :rtype: InlineResponse2001
    """

    expires_on = datetime.utcnow() + timedelta(minutes=60)
    expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

    #todo: generate a session_id and token
    session_id = "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
    token = "yyq6qpj2a"

    object_to_return = { "expires_on": expires_on_formatted, "session_id": session_id, "token": token }
    return jsonify(object_to_return)


def withdrawal_post(body):  # noqa: E501
    """Initiate a withdrawal

    Request lnurlw from the provider. User can provide optional fallback onchain address which will be used if the withdrawal is not claimed before the expiration date # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2005
    """
    if connexion.request.is_json:
        body = WithdrawalBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info(f"Received post data to /withdrawal data: {body}")
        logging.info(f"failback_onchain: {body.failback_onchain}")
        logging.info(f"order_id: {body.order_id}")
        logging.info(f"session_id: {body.session_id}")
        expires_on = datetime.utcnow() + timedelta(minutes=30)
        expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        object_to_return = {
  "lnurlw": "LNURL...",
  "order_id": "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",
  "withdrawal_expiration_date": expires_on_formatted
        }
        return jsonify(object_to_return)
    return 'Something went wrong'
