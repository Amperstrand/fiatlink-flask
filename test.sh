#!/bin/bash
delay=1
set -e

base_url=http://localhost:8080

# get to /features
features_response=$(curl -sS -X 'GET' \
  "$base_url/ALJAZ/fiatlink/1.0.0/features" \
  -H 'accept: application/json')
echo $features_response | jq -r .

# get to /verify
verify_response=$(curl -sS -X 'GET' \
  "$base_url/ALJAZ/fiatlink/1.0.0/verify" \
  -H 'accept: application/json')
echo $verify_response | jq -r .

# post to /session
session_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/session" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "app_id": "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",
  "node_pubkey": "0288037d3f0bdcfb240402b43b80cdc32e41528b3e2ebe05884aff507d71fca71a",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5",
  "signature": "rdfe8mi98o7am51jpocda1zp5d8scdu7rg65nn73fs6mb69t4byer9xned1hntkeq1pqdct9z5owx6bg58w5fmny6p5q783dce8ittjh"
}')

echo $session_response | jq -r .
session_id=$(echo $session_response | jq -r .session_id)
echo session_id $session_id

# post to /payment-options
payment_options_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/payment-options" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "currency_code": "EUR",
  "session_id": "'$session_id'"
}')
echo $payment_options_response | jq -r .

# post to /quote

quote_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/quote" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount_fiat": 100,
  "currency_id": 1,
  "payment_option_id": 1,
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}')
echo $quote_response | jq -r .
quote_id=$(echo $quote_response | jq -r .quote_id)
echo quote_id $quote_id

sleep ${delay}

#post to /order
order_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "quote_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5",
  "webhook_url": "https://webhook.example.com/"
}')
echo $order_response | jq -r .
echo $order_response | jq -r .order_status


#mark the order as settled

api_key=215b9e349fa918023654d6982a68e05d26beb851
store_id=6WGmyJNq1AvQD9n5JZipn1wSt4Nh86wwUv6xYSzEdtui

#invoice_id=$(python3 -c "import uuid; import base64; print(base64.urlsafe_b64encode(uuid.UUID('"${quote_id}"').bytes).decode('utf-8').rstrip('='))")
invoice_id=$(python3 -c "import uuid; import base64; quote_id='"${quote_id}"'; print(base64.urlsafe_b64encode(uuid.UUID(quote_id).bytes).decode('utf-8').rstrip('='))")
echo $invoice_id
python3 -c "from swagger_server.controllers.invoice_helper import convert_id_to_uuid; id='"$invoice_id"'; uuid = convert_id_to_uuid(id); print(uuid)"
 

echo invoice_id $invoice_id
echo invoice_id $invoice_id


curl  -X POST https://signet.demo.btcpayserver.org/api/v1/stores/${store_id}/invoices/${invoice_id}/status -H 'Authorization: token 7275e951ef1e37d36e612fa28963602546155fab' -H 'Content-Type: application/json' -d '{"status": "Settled"}'

sleep 5
exit


# {"missingPermission":"btcpay.store.canmodifyinvoices","code":"missing-permission","message":"Insufficient API Permissions. Please use an API key with permission \"btcpay.store.canmodifyinvoices\". You can create an API key in your account's settings / Api Keys."}%                      


#post to /order-status after a few seconds seconds. order should be marked as paid now
sleep ${delay}
order_status_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order-status" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}')

echo $order_status_response | jq
echo $order_status_response | jq -r '."'$quote_id'".order_status'

#post to /withdrawal

withdrawal_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/withdrawal" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "failback_onchain": "bc1qcmu7kcwrndyke09zzyl0wv3dqxwlzqkma248kj",
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}')

echo $withdrawal_response | jq -r .


#post to /order-status after withdraw. should be finished
order_status_response=$(curl -sS -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order-status" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}')

echo $order_status_response | jq
echo $order_status_response | jq -r '."'$quote_id'".order_status'
