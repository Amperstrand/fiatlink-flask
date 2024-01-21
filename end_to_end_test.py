import requests
import json
import time
import base64
import uuid

from swagger_server.controllers.invoice_helper import find_invoiceId_that_starts_with

simulate_payment=False

# Set up base parameters
base_url = "http://localhost:8080"
headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
delay = 2

# Function to perform GET request
def get_request(url):
    print (f"GET request to {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to perform POST request
def post_request(url, data):
    print (f"POST request to {url}:")
    print (data)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

# GET /features
features_response = get_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/features")
print(json.dumps(features_response, indent=2))

# GET /verify
verify_response = get_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/verify")
print(json.dumps(verify_response, indent=2))

# POST /session
session_data = {
    "app_id": "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",
    "node_pubkey": "0288037d3f0bdcfb240402b43b80cdc32e41528b3e2ebe05884aff507d71fca71a",
    "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5",
    "signature": "rdfe8mi98o7am51jpocda1zp5d8scdu7rg65nn73fs6mb69t4byer9xned1hntkeq1pqdct9z5owx6bg58w5fmny6p5q783dce8ittjh"
}
session_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/session", session_data)
print(json.dumps(session_response, indent=2))
session_id = session_response['session_id']

# POST /payment-options
payment_options_data = {"currency_code": "EUR", "session_id": session_id}
payment_options_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/payment-options", payment_options_data)
print(json.dumps(payment_options_response, indent=2))

# POST /quote
quote_data = {
    "amount_fiat": 1000,
    "currency_id": 0,
    "payment_option_id": 0,
    "session_id": session_id
}

quote_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/quote", quote_data)
print(json.dumps(quote_response, indent=2))

quote_id = quote_response['quote_id']

time.sleep(delay)

# POST /order
order_data = {
    "quote_id": quote_id,
    "session_id": session_id,
    "webhook_url": "https://webhook.example.com/"
}

order_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/order", order_data)
print(json.dumps(order_response, indent=2))

# Mark the order as settled
api_key = "215b9e349fa918023654d6982a68e05d26beb851"
storeId = "6WGmyJNq1AvQD9n5JZipn1wSt4Nh86wwUv6xYSzEdtui"

wrong_invoiceId = base64.urlsafe_b64encode(uuid.UUID(quote_id).bytes).decode('utf-8').rstrip('=')

print('todo: this is inconsistent with the invoiceId that btcpayserver generates')
print("wrong_invoiceId:", wrong_invoiceId)

#strip the last character because the base64 --> uuid conversion process is not quite working
invoiceId=find_invoiceId_that_starts_with(api_key, storeId, wrong_invoiceId[:-1])
print('todo: this is inconsistent with the invoiceId that btcpayserver generates. this is the correct invoiceId')
print (invoiceId)

# POST /order-status to see that the order has not been paid yet
order_status_data = {"order_id": quote_id, "session_id": session_id}
order_status_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/order-status", order_status_data)
print(json.dumps(order_status_response, indent=2))
assert order_status_response[quote_id]['order_status']=='placed'


#mark the invoice invoiceId as settled
if (simulate_payment):
    settle_url = f"https://signet.demo.btcpayserver.org/api/v1/stores/{storeId}/invoices/{invoiceId}/status"
    settle_data = {"status": "Settled"}
    settle_headers = {'Authorization': 'token 7275e951ef1e37d36e612fa28963602546155fab', 'Content-Type': 'application/json'}
    response = requests.post(settle_url, headers=settle_headers, data=json.dumps(settle_data))
    response.raise_for_status()
    time.sleep(delay)
else:
    #pay the order manually
    time.sleep(120)

# POST /order-status again
order_status_data = {"order_id": quote_id, "session_id": session_id}
order_status_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/order-status", order_status_data)
print(json.dumps(order_status_response, indent=2))
assert order_status_response[quote_id]['order_status']=='filled'

# POST /withdrawal
withdrawal_data = {
    "failback_onchain": "bc1qcmu7kcwrndyke09zzyl0wv3dqxwlzqkma248kj",
    "order_id": quote_id,
    "session_id": session_id
}
withdrawal_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/withdrawal", withdrawal_data)
print(json.dumps(withdrawal_response, indent=2))

# Final order status check
final_order_status_response = post_request(f"{base_url}/ALJAZ/fiatlink/1.0.0/order-status", order_status_data)
print(json.dumps(final_order_status_response, indent=2))
