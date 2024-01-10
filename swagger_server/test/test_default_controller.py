# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

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
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_features_get(self):
        """Test case for features_get

        Get supported features
        """
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/features',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_order_post(self):
        """Test case for order_post

        Create an order
        """
        body = OrderBody()
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/order',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_order_status_post(self):
        """Test case for order_status_post

        Get order status
        """
        body = OrderstatusBody()
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/order-status',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payment_options_post(self):
        """Test case for payment_options_post

        Get payment options
        """
        body = PaymentoptionsBody()
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/payment-options',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_quote_post(self):
        """Test case for quote_post

        Get a quote or estimate
        """
        body = QuoteBody()
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/quote',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_session_post(self):
        """Test case for session_post

        Start a session
        """
        body = SessionBody()
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/session',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_verify_get(self):
        """Test case for verify_get

        Provides token for authentication
        """
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/verify',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_withdrawal_post(self):
        """Test case for withdrawal_post

        Initiate a withdrawal
        """
        body = WithdrawalBody()
        response = self.client.open(
            '/ALJAZ/fiatlink/1.0.0/withdrawal',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
