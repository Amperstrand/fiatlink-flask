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
from datetime import datetime, timedelta

import logging
logging.basicConfig(level=logging.INFO)
import uuid

#todo: move this to the right place
from swagger_server.controllers.currency_manager import CurrencyManager 
from swagger_server.controllers.currency_manager import PaymentInfo
from swagger_server.controllers.currency_manager import PaymentOption

currencies = CurrencyManager()
all_currencies = currencies()  # Get all currencies
eur_currency = currencies('eur')  # Get only EUR currency
chf_currency = currencies('chf')  # Get only CHF currency

def create_random_quote_uuid():
    #todo: this should be a random uuid. for now it is sequential to make testing easier
    #first quote_id as defined in the examples
    first_quote_id = "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6"
    increment_value = len(quotes_data_store)
    first_quote_id_as_uuid = uuid.UUID(first_quote_id)
    # Convert the UUID to a list of its 16 bytes
    byte_list = list(first_quote_id_as_uuid.bytes)

    # Start from the last byte and increment, handling overflow
    for i in range(len(byte_list) - 1, -1, -1):
        # Increment the current byte
        increment_value, remainder = divmod(byte_list[i] + increment_value, 256)
        byte_list[i] = remainder
        # If there is no carry-over, break
        if increment_value == 0:
            break

    # Convert the byte list back to bytes
    incremented_bytes = bytes(byte_list)
    # Convert back to UUID
    return str(uuid.UUID(bytes=incremented_bytes))

# Gobal data store to keep track of quotes. TODO: this should be a database
quotes_data_store = {}

# Global data store to keep track of orders TODO: this should be a database
orders_data_store = {}

# Global data store to keep track of when orders were placed by the /order endpoint
placed_data_store = {}

# Global data store to keep track of when orders were marked as filled (paid for). TODO: for now this is done by the /order-status endpoint if an order is more then 10 seconds old.
filled_data_store = {}

# Global data store to keep track of when orders were marked as filled (paid out). TODO: for now this is done after calling /withdrawal.
finished_data_store = {}

#todo: multiple payouts and payout status

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
    return (response)

def order_post(body):  # noqa: E501
    """Create an order

    Confirm an order from quote and get payment information in return # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2004
    """
    if connexion.request.is_json:
        body = OrderBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info("Received post data to /session - " + ", ".join([f"{key}: {value}" for key, value in vars(body).items()]))
        #logging.info(f"Received post data to /order data: {body}")
        #logging.info(f"quote_id: {body.quote_id}")
        #logging.info(f"session_id: {body.session_id}")
        #logging.info(f"webhook_url: {body.webhook_url}")

        #todo: prevent race conditions where two orders can be placed using the same quote
        #todo: fetch quote from database instead of temporary global variable data store
        try:
            quote = quotes_data_store[body.quote_id]
            logging.info(quote)
        except Exception as e:
            logging.error(f"Error fetching quote: {e}")
            return f"Error fetching quote: {e}. Hint: you need to request a /quote first"

        #Check if an order already exists for this quote
        if body.quote_id in orders_data_store:
            order = orders_data_store[body.quote_id]
            logging.error(f"An order already exists for this quote: {body.quote_id}")
            return(f"An order already exists for this quote: {body.quote_id}")

        order_id = body.quote_id

        # Check if the quote is still valid
        try:
            expiration_date = datetime.strptime(quote.expires_on, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            current_time = datetime.utcnow()

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

        #not used but also work:
        #credit_card_payment_info = PaymentInfo.get_payment_info(3).to_dict()
        #bank_transfer_payment_info = PaymentInfo.get_payment_info(5).to_dict()

        order = InlineResponse2004(
            order_id=order_id,
            order_status="placed",
            amount_fiat=amount_fiat,
            currency_id=quote.currency_id,
            payment_option_id=quote.payment_option_id,
            amount_sats=quote.amount_sats,
            expires_on=quote.expires_on,

            # Add the necessary payment info here
            #todo: this fails. Maybe bank_transfer_payment_info should return a dict instead of an object as default
            #payment_info=[credit_card_payment_info.to_dict()]
            #payment_info=[payment_method_from_quote.to_dict()]
            #payment_info=[bank_transfer_payment_info]
            #payment_info={}

            #todo: consider changeing the type so that the to_dict() conversion is not needed
            payment_info=PaymentInfo.get_payment_info(quote.payment_option_id).to_dict()
        )

        #create the order
        orders_data_store[order_id] = order
        placed_data_store[order_id] = datetime.utcnow()
        return (order)
    return 'Something went wrong'

def order_status_post(body):  # noqa: E501

    #todo: order status can also be this:
    #refunded - status when fiat payment was refunded

    """Get order status

    This endpoint returns the status of one or more orders based on the session and order ID. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Dict[str, InlineResponseMap200]
    """

    if connexion.request.is_json:
        body = OrderstatusBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info("Received post data to /session - " + ", ".join([f"{key}: {value}" for key, value in vars(body).items()]))
        #logging.info(f"Received post data to /order-status data: {body}")
        #logging.info(f"order_id: {body.order_id}")
        #logging.info(f"session_id: {body.session_id}")

        orders = {}

        #todo: work on this logic

        if body.order_id and body.order_id not in orders_data_store:
            logging.warning(f"No order found with order id {body.order_id}")
            return {'message': 'No order found with the provided order ID'}

        elif body.order_id and body.order_id in finished_data_store:
            #finished - status when user successfully withdrew the funds
            logging.warning(f"Order {body.order_id} is in the finished_data_store. The order was marked as finished and paid out at {finished_data_store[body.order_id]}.")
            order = orders_data_store[body.order_id]
            assert order.order_status == 'finished'
            orders= {order.order_id: order}
            return(orders)

        elif body.order_id and body.order_id in filled_data_store:
            #filled - status when order is executed and user can withdraw it
            logging.warning(f"Order {body.order_id} is in the filled_data_store. This means the order was marked paid for at {filled_data_store[body.order_id]}.")
            order = orders_data_store[body.order_id]
            assert order.order_status == 'filled'
            orders= {order.order_id: order}
            return(orders)

        elif body.order_id and body.order_id in placed_data_store:
            #placed - status upon user confirmation of the quote / pending payment
            logging.warning(f"Order {body.order_id} is in the placed_data_store. An order for the quote was created at {placed_data_store[body.order_id]}.")
            order = orders_data_store[body.order_id]

            #todo: check if the order has been paid and update the status here
            current_time = datetime.utcnow()
            placed_time = placed_data_store[body.order_id]
            total_seconds_difference = (current_time - placed_time).total_seconds()

            if total_seconds_difference > 10:
                logging.info ("The difference is more than 10 seconds. This means the order should be paid since all orders get paid when you check the status after 10 seconds.")
                #todo: don't overwrite the timestamp

                #UPDATE THE ORDER STATUS TO FILLED (it has been paid)
                logging.warning(f"Marking the order {body.order_id} as paid. This is a dummy call that should be done from its own API endpoint")
                filled_data_store[body.order_id] = datetime.utcnow()
                new_order_status='filled'
                orders_data_store[body.order_id].order_status = new_order_status

                order = orders_data_store[body.order_id]
                assert order.order_status == 'filled'
                orders = {order.order_id: order}

            else:
                logging.info (f"Chech the /status endpoint again for order {body.order_id} in {(10 - total_seconds_difference)} seconds to mark this order as filled.")
                assert order.order_status == 'placed'
                orders = {order.order_id: order}

            return(orders)


        #todo: fetch orders based on session_id
        if (body.session_id == 'd7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5'):
            logging.info(f"session_id: {body.session_id} found.")
            logging.info(f"Returning all orders for session_id: {body.session_id}.")
            logging.info(orders_data_store)
            return (orders_data_store)

    #todo: handle case where session id is wrong (applies to all functions)
    return 'Something went wrong'

def payment_options_post(body):  # noqa: E501
    """Get payment options

    This endpoint provides a list of payment options for different currencies, filtered by an optional currency code. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2006
    """

    logging.info('all_currencies:')
    logging.info(all_currencies)
    logging.info('eur_currencies:')
    logging.info(eur_currency)
    logging.info('chf_currency:')
    logging.info(chf_currency)

    single_currency=False

    if connexion.request.is_json:
        body = PaymentoptionsBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info("Received post data to /session - " + ", ".join([f"{key}: {value}" for key, value in vars(body).items()]))
        #logging.info(f"Received post data to /payment-options data: {body}")
        #logging.info(f"currency_code: {body.currency_code}")
        #logging.info(f"session_id: {body.session_id}")

        if (body.currency_code):
             single_currency=(body.currency_code).lower()

    #return all currencies unless a specific currency was asked for

    logging.info(single_currency)

#todo: what to do if single_currency is not found. fix this
#    if single_currency and single_currency not in currencies:
#        return ("unsupported currency. try calling this endpoint again with no currency specified to get a list of all currencies")
     
    if single_currency:
        #return_object = [currencies[single_currency].to_dict()]
        #return_object = { single_currency.lower(): currencies [single_currency.lower()]}
        #return_object = { single_currency.lower(): currencies [single_currency.lower()]}
        return_object = currencies(single_currency.lower())
    else:
        return_object = all_currencies
    logging.info(return_object)

    return (InlineResponse2006(return_object))


def quote_post(body):  # noqa: E501
    """Get a quote or estimate

    Get a an quote or estimate from the provider based on amount of fiat you want to spend # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2003
    """
    if connexion.request.is_json:
        body = QuoteBody.from_dict(connexion.request.get_json())  # noqa: E501
        #logging.info("Received post data to /session - " + ", ".join([f"{key}: {value}" for key, value in vars(body).items()]))
        logging.info(f"Received post data to /quote data: {body}")
        logging.info(f"currency_id: {body['currency_id']}")
        logging.info(f"payment_option_id: {body['payment_option_id']}")
        logging.info(f"session_id: {body['session_id']}")

        #todo: why doesn't this work?
        #logging.info(f"session_id: {body.session_id}")

        # $50000 = 1 BTC
        btc_price=(50000*100) # in cents
        sat_price = btc_price / 100000000

        is_estimate = False
        order_fee=0 # in cents
        currency_id = body['currency_id']
        payment_option_id = body['payment_option_id']
        
        quote_id = create_random_quote_uuid()

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

        #todo: get currency by id instead of string code
        #1 is eur
        #2 is chf
        currency_code='eur'
        payment_options = currencies(currency_code)

        logging.info(f"payment_options for {currency_code}:")
        logging.info(payment_options)

        #logging.info(f"this is the hardcoded payment option which works:")
        #logging.info(PaymentOption("Bank transfer", 5, 0.01, 10, 10000000))
        #logging.info(payment_option)
        #logging.info(payment_option.to_dict())

#fix this
        payment_option=payment_options[currency_code] ['payment_options'][0]
        logging.info(payment_option)


        #payment_option=(currencies.get_payment_option(currency_code, quote.payment_option))
        #nearly works:
        payment_option=(currencies.get_payment_option(currency_code, payment_option_id)).to_dict()

        logging.info('todo: select the right payment_option_id here. Need to search for it, not use index')

        if payment_option:
            logging.info("Payment Option Found:")
            logging.info(payment_option)
        else:
            logging.info("Payment Option Not Found. Something must be wrong")
            return("Payment option Not Found. Something must be wrong")

        min_amount_fiat=payment_option['min_amount']
        max_amount_fiat=payment_option['max_amount']

        min_amount_sats = 1
        max_amount_sats = 21 * 1000000 * 100000000

        if (amount_fiat < min_amount_fiat):
            return f"Something went wrong: amount_fiat is less than {min_amount_fiat}"
        if (amount_fiat > max_amount_fiat):
            return f"Something went wrong: amount_fiat is greater than {max_amount_fiat}"
        if (amount_sats < min_amount_sats):
            return f"Something went wrong: amount_sats is less than {min_amount_sats}"
        if (amount_sats > max_amount_sats):
            return f"Something went wrong: amount_sats is greater than {max_amount_sats}"

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

        quotes_data_store[quote_id] = quote
        return (quote)
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
        logging.info("Received post data to /session - " + ", ".join([f"{key}: {value}" for key, value in vars(body).items()]))

        #logging.info(f"Received post data to /session data: {body}")
        #logging.info(f"app_id: {body.app_id}")
        #logging.info(f"node_pubkey: {body.node_pubkey}")
        #logging.info(f"session_id: {body.session_id}")
        #logging.info(f"signature: {body.signature}")

        expires_on = datetime.utcnow() + timedelta(minutes=60)
        expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        session = InlineResponse2002(session_id=body.session_id, app_id=body.app_id, expires_on=expires_on)
        return (session)
    return 'Something went wrong'

def verify_get():  # noqa: E501
    """Provides token for authentication

    Request a token to be signed by the reciever node as proof of ownership # noqa: E501

    :rtype: InlineResponse2001
    """

    expires_on = datetime.utcnow() + timedelta(minutes=60)
    expires_on_formatted = expires_on.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

    #todo: generate a random session_id and token
    session_id = "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
    token = "yyq6qpj2a"

    challenge = InlineResponse2001(session_id=session_id, token=token, expires_on=expires_on)
    return (challenge)


def withdrawal_post(body):  # noqa: E501
    #todo: lnurlw could maybe be deterministic based on the order id.

    """Initiate a withdrawal

    Request lnurlw from the provider. User can provide optional fallback onchain address which will be used if the withdrawal is not claimed before the expiration date # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2005
    """
    if connexion.request.is_json:
        body = WithdrawalBody.from_dict(connexion.request.get_json())  # noqa: E501
        logging.info("Received post data to /session - " + ", ".join([f"{key}: {value}" for key, value in vars(body).items()]))
        #logging.info(f"Received post data to /withdrawal data: {body}")
        #logging.info(f"failback_onchain: {body.failback_onchain}")
        #logging.info(f"order_id: {body.order_id}")
        #logging.info(f"session_id: {body.session_id}")

        if body.order_id not in  orders_data_store:
            return (f"order {body.order_id} does not exist")

        if body.order_id in finished_data_store:
            return (f"a payout already exists for order {body.order_id}")

        assert filled_data_store[body.order_id] is not None
        logging.warning(f"Order {body.order_id} was marked as filled (paid) at {filled_data_store[body.order_id]}.")

        order = orders_data_store[body.order_id]

        withdrawal_expiration = datetime.utcnow() + timedelta(minutes=30)
        withdrawal_expiration_date_formatted = withdrawal_expiration.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        #todo: "failback_onchain": "bc1qcmu7kcwrndyke09zzyl0wv3dqxwlzqkma248kj" #optional

        #Check order balance remaining to be paid out > 0
        previous_payouts_for_this_order = 0
        remaining_balance = order.amount_sats - previous_payouts_for_this_order

        if (remaining_balance <= 0):
            #todo: assert that order status is finished or somethings is very wrong
            return (f"{previous_payouts} has already been paid out")
            assert finished_data_store[body.order_id] is not None

        #todo: check that the order is not in the process of being paid out

        #todo: should you be allowed to make multiple withdrawals for an order? if not, how should a case where only a partial withdraw is made by the lnurlw?
        #todo: and if so, should it use the same lnurlw or a new one? A new one, or else the wallet can withdraw more. lnurlw should be single use

        #todo: consider if the user does not register an onchain fallback, then a new withdraw request should be allowed for the same order?

        #UPDATE THE ORDER STATUS
        logging.warning(f"Marking the order {body.order_id} as paid. This is a dummy call that should be done from its own API endpoint after the payout is done")
        new_order_status='finished'
        finished_data_store[body.order_id] = datetime.utcnow()
        orders_data_store[body.order_id].order_status = new_order_status

        #todo: generate a valid LNURLw
        logging.info(f"todo: generate a valid LNURLw for {remaining_balance}")
        lnurlw=f"LNURL... which will let you withdraw {remaining_balance}"

        response = InlineResponse2005( order_id=body.order_id, lnurlw=lnurlw, withdrawal_expiration_date=withdrawal_expiration_date_formatted)
        return (response)
    return 'Something went wrong'
