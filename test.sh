#!/bin/bash

base_url=http://localhost:8080


# get to /features

curl -X 'GET' \
  "$base_url/ALJAZ/fiatlink/1.0.0/features" \
  -H 'accept: application/json'

# get to /verify

curl -X 'GET' \
  "$base_url/ALJAZ/fiatlink/1.0.0/verify" \
  -H 'accept: application/json'

# post to /session

curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/session" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "app_id": "8ed13c2a-a8c6-4f0e-b43e-3fdbf1f094a6",
  "node_pubkey": "0288037d3f0bdcfb240402b43b80cdc32e41528b3e2ebe05884aff507d71fca71a",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5",
  "signature": "rdfe8mi98o7am51jpocda1zp5d8scdu7rg65nn73fs6mb69t4byer9xned1hntkeq1pqdct9z5owx6bg58w5fmny6p5q783dce8ittjh"
}'


# post to /payment-options
curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/payment-options" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "currency_code": "EUR",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}'

curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/payment-options" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "currency_code": "eur",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}'

curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/payment-options" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "currency_code": "invalid",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}'

curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/payment-options" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}'

# post to /quote

quote_response=$(curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/quote" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount_fiat": 100,
  "currency_id": 1,
  "payment_option_id": 1,
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}')
echo $quote_response
quote_id=$(echo $quote_response | jq -r .quote_id)

sleep 1

#post to /order
curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "quote_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5",
  "webhook_url": "https://webhook.example.com/"
}'

#post to /order-status
curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order-status" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}' | grep status

#post to /order-status again after 15 seconds. order should be paid now
sleep 15
curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order-status" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}' | grep status

#post to /withdrawal

curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/withdrawal" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "failback_onchain": "bc1qcmu7kcwrndyke09zzyl0wv3dqxwlzqkma248kj",
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}'


#post to /order-status again after 15 seconds. order should be finished
sleep 1
curl -X 'POST' \
  "$base_url/ALJAZ/fiatlink/1.0.0/order-status" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "order_id": "'$quote_id'",
  "session_id": "d7ef9a88-1ca1-4ac8-bc9e-da3d9824cdc5"
}' |grep status
