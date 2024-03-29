# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class OrderBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, session_id: str=None, quote_id: str=None, webhook_url: str=None):  # noqa: E501
        """OrderBody - a model defined in Swagger

        :param session_id: The session_id of this OrderBody.  # noqa: E501
        :type session_id: str
        :param quote_id: The quote_id of this OrderBody.  # noqa: E501
        :type quote_id: str
        :param webhook_url: The webhook_url of this OrderBody.  # noqa: E501
        :type webhook_url: str
        """
        self.swagger_types = {
            'session_id': str,
            'quote_id': str,
            'webhook_url': str
        }

        self.attribute_map = {
            'session_id': 'session_id',
            'quote_id': 'quote_id',
            'webhook_url': 'webhook_url'
        }
        self._session_id = session_id
        self._quote_id = quote_id
        self._webhook_url = webhook_url

    @classmethod
    def from_dict(cls, dikt) -> 'OrderBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The order_body of this OrderBody.  # noqa: E501
        :rtype: OrderBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def session_id(self) -> str:
        """Gets the session_id of this OrderBody.


        :return: The session_id of this OrderBody.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """Sets the session_id of this OrderBody.


        :param session_id: The session_id of this OrderBody.
        :type session_id: str
        """
        if session_id is None:
            raise ValueError("Invalid value for `session_id`, must not be `None`")  # noqa: E501

        self._session_id = session_id

    @property
    def quote_id(self) -> str:
        """Gets the quote_id of this OrderBody.


        :return: The quote_id of this OrderBody.
        :rtype: str
        """
        return self._quote_id

    @quote_id.setter
    def quote_id(self, quote_id: str):
        """Sets the quote_id of this OrderBody.


        :param quote_id: The quote_id of this OrderBody.
        :type quote_id: str
        """
        if quote_id is None:
            raise ValueError("Invalid value for `quote_id`, must not be `None`")  # noqa: E501

        self._quote_id = quote_id

    @property
    def webhook_url(self) -> str:
        """Gets the webhook_url of this OrderBody.

        optional webhook for notifications  # noqa: E501

        :return: The webhook_url of this OrderBody.
        :rtype: str
        """
        return self._webhook_url

    @webhook_url.setter
    def webhook_url(self, webhook_url: str):
        """Sets the webhook_url of this OrderBody.

        optional webhook for notifications  # noqa: E501

        :param webhook_url: The webhook_url of this OrderBody.
        :type webhook_url: str
        """

        self._webhook_url = webhook_url
