# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class WithdrawalBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, session_id: str=None, order_id: str=None, failback_onchain: str=None):  # noqa: E501
        """WithdrawalBody - a model defined in Swagger

        :param session_id: The session_id of this WithdrawalBody.  # noqa: E501
        :type session_id: str
        :param order_id: The order_id of this WithdrawalBody.  # noqa: E501
        :type order_id: str
        :param failback_onchain: The failback_onchain of this WithdrawalBody.  # noqa: E501
        :type failback_onchain: str
        """
        self.swagger_types = {
            'session_id': str,
            'order_id': str,
            'failback_onchain': str
        }

        self.attribute_map = {
            'session_id': 'session_id',
            'order_id': 'order_id',
            'failback_onchain': 'failback_onchain'
        }
        self._session_id = session_id
        self._order_id = order_id
        self._failback_onchain = failback_onchain

    @classmethod
    def from_dict(cls, dikt) -> 'WithdrawalBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The withdrawal_body of this WithdrawalBody.  # noqa: E501
        :rtype: WithdrawalBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def session_id(self) -> str:
        """Gets the session_id of this WithdrawalBody.


        :return: The session_id of this WithdrawalBody.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """Sets the session_id of this WithdrawalBody.


        :param session_id: The session_id of this WithdrawalBody.
        :type session_id: str
        """
        if session_id is None:
            raise ValueError("Invalid value for `session_id`, must not be `None`")  # noqa: E501

        self._session_id = session_id

    @property
    def order_id(self) -> str:
        """Gets the order_id of this WithdrawalBody.


        :return: The order_id of this WithdrawalBody.
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id: str):
        """Sets the order_id of this WithdrawalBody.


        :param order_id: The order_id of this WithdrawalBody.
        :type order_id: str
        """
        if order_id is None:
            raise ValueError("Invalid value for `order_id`, must not be `None`")  # noqa: E501

        self._order_id = order_id

    @property
    def failback_onchain(self) -> str:
        """Gets the failback_onchain of this WithdrawalBody.


        :return: The failback_onchain of this WithdrawalBody.
        :rtype: str
        """
        return self._failback_onchain

    @failback_onchain.setter
    def failback_onchain(self, failback_onchain: str):
        """Sets the failback_onchain of this WithdrawalBody.


        :param failback_onchain: The failback_onchain of this WithdrawalBody.
        :type failback_onchain: str
        """

        self._failback_onchain = failback_onchain
