import requests
import json

import base64
import uuid
import logging

#def convert_id_to_uuid(order_response):
    # Extract the ID from the order response
    #order_id = order_response.get('id')
def convert_id_to_uuid(order_id):
    if not order_id:
        logging.error("No ID found in order response")
        return None

    # Add padding to the Base64 string if necessary
    padding_needed = len(order_id) % 4
    if padding_needed:
        order_id_padded = order_id + "=" * (4 - padding_needed)
    else:
        order_id_padded = order_id

    # Try decoding with padding
    try:
        decoded_bytes = base64.b64decode(order_id_padded)
        if len(decoded_bytes) == 16:
            # Convert to UUID
            return str(uuid.UUID(bytes=decoded_bytes))

        else:
            logging.error("Decoded bytes do not form a valid UUID.")
            return None
    except Exception as e:
        logging.error(f"Error in decoding: {e}")
        return None

def convert_uuid_to_orderId(uuid_str):
    try:
        # Convert the string to a UUID object
        uuid_obj = uuid.UUID(uuid_str)

        # Convert UUID to bytes
        uuid_bytes = uuid_obj.bytes

        # Encode bytes to Base64
        encoded_base64 = base64.b64encode(uuid_bytes)

        # Convert to string and remove padding
        order_id = encoded_base64.decode('utf-8').rstrip('=')

        return order_id
    except Exception as e:
        logging.error(f"Error in converting UUID string to order ID: {e}")
        return None



def get_invoice_data(api_key, crypto_code, store_id, invoiceId):
    """
    Retrieves invoice data from a specified endpoint.

    Parameters:
    api_key (str): API key for authentication.
    crypto_code (str): Cryptocurrency code.
    store_id (str): Store ID.
    invoiceId (str): Invoice ID.

    Returns:
    dict: Parsed JSON data of the invoice or an empty dict if the request fails.
    """
    # Construct the URL
    url = f"https://signet.demo.btcpayserver.org/api/v1/stores/{store_id}/invoices/{invoiceId}"

    # Headers with API Key for Authentication
    headers = {
        "Authorization": f"token {api_key}"
    }

    # Making the GET request with authentication
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        data = {}

    return data

def is_invoice_paid(api_key, crypto_code, store_id, invoiceId):
    """
    Checks if the invoice is paid.

    Parameters:
    api_key (str): API key for authentication.
    crypto_code (str): Cryptocurrency code.
    store_id (str): Store ID.
    invoiceId (str): Invoice ID.

    Returns:
    bool: True if the invoice is paid, False otherwise.
    """
    # Retrieve the invoice data
    invoice_data = get_invoice_data(api_key, crypto_code, store_id, invoiceId)

    # Check if the invoice data is retrieved successfully and check its status
    if invoice_data and 'status' in invoice_data:
        logging.info(invoice_data['status'])
        #return invoice_data['status'].lower() == 'settled'

        #invoice has status processing until n confirmations. for signet, we don't care about this and accept 0conf
        return invoice_data['status'].lower() in ['settled', 'processing']
    return False


def create_invoice(api_key, store_id, amount, currency, metadata, checkout):
    """
    Creates an order (invoice) on BTCPay Server.

    Parameters:
    api_key (str): API key for authentication.
    store_id (str): Store ID.
    amount (float): Amount for the invoice.
    currency (str): Currency code (e.g., 'BTC').
    metadata (dict): Metadata associated with the invoice.
    checkout (dict): Checkout options.

    Returns:
    dict: Response data from the server or an error message.
    """
    url = f"https://signet.demo.btcpayserver.org/api/v1/stores/{store_id}/invoices"

    headers = {
        "Authorization": f"token {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "amount": amount,
        "currency": currency,
        "metadata": metadata,
        "checkout": checkout
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to create order. Status code: {response.status_code}"}

import requests

def mark_invoice_status(api_key, store_id, invoiceId, new_status):
    """
    Marks an invoice as settled or invalid.

    Parameters:
    api_key (str): API key for authentication.
    store_id (str): Store ID.
    invoiceId (str): Invoice ID to be updated.
    new_status (str): New status of the invoice ("Settled" or "Invalid").

    Returns:
    dict: Response data from the server or an error message.
    """
    url = f"https://signet.demo.btcpayserver.org/api/v1/stores/{store_id}/invoices/{invoiceId}/status"

    headers = {
        "Authorization": f"token {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "status": new_status
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to mark invoice status. Status code: {response.status_code}"}

def find_invoiceId_that_starts_with(api_key, store_id, partial_id):
    """
    Searches through invoices and returns the full ID of an invoice that starts with the provided partial ID.

    Parameters:
    api_key (str): API key for authentication.
    store_id (str): Store ID.
    partial_id (str): The partial ID to search for.

    Returns:
    str: The full invoice ID if found, None otherwise.
    """
    url = f"https://signet.demo.btcpayserver.org/api/v1/stores/{store_id}/invoices"

    headers = {
        "Authorization": f"token {api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        invoices = response.json()

        for invoice in invoices:
            invoiceId = invoice.get("id")
            if invoiceId and invoiceId.startswith(partial_id):
                return invoiceId

        return None  # No matching invoice ID found
    else:
        print(f"Failed to retrieve invoices. Status code: {response.status_code}")
        return None

import requests
import json

def create_pull_payment(api_key, store_id, name, description, amount, currency, period, BOLT11Expiration, autoApproveClaims, startsAt, expiresAt, paymentMethods):
    """
    Creates a pull payment on BTCPay Server.

    Parameters:
    api_key (str): API key for authentication.
    store_id (str): Store ID.
    name (str): Name of the pull payment.
    description (str): Description of the pull payment.
    amount (str): Amount for the pull payment.
    currency (str): Currency code (e.g., 'BTC').
    period (int): Period in seconds.
    BOLT11Expiration (int): BOLT11 invoice expiration time in minutes.
    autoApproveClaims (bool): Whether to auto-approve claims or not.
    startsAt (int): Start time in Unix timestamp.
    expiresAt (int): Expiration time in Unix timestamp.
    paymentMethods (list): List of payment methods (e.g., ['BTC']).

    Returns:
    dict: Response data from the server or an error message.
    """
    url = f"https://signet.demo.btcpayserver.org/api/v1/stores/{store_id}/pull-payments"

    headers = {
        "Authorization": f"token {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "name": name,
        "description": description,
        "amount": amount,
        "currency": currency,
        "period": period,
        "BOLT11Expiration": BOLT11Expiration,
        "autoApproveClaims": autoApproveClaims,
        "startsAt": startsAt,
        "expiresAt": expiresAt,
        "paymentMethods": paymentMethods
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to create pull payment. Status code: {response.status_code}"}

# Example usage
# api_key = 'your_api_key_here'
# store_id = 'your_store_id_here'
# response = create_pull_payment(api_key, store_id, "Test payout", "Description", "0.1", "BTC", 604800, 30, False, 1592312018, 1593129600, ["BTC"])
# print(response)

