# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2001(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, session_id: str=None, token: str=None, expires_on: datetime=None):  # noqa: E501
        """InlineResponse2001 - a model defined in Swagger

        :param session_id: The session_id of this InlineResponse2001.  # noqa: E501
        :type session_id: str
        :param token: The token of this InlineResponse2001.  # noqa: E501
        :type token: str
        :param expires_on: The expires_on of this InlineResponse2001.  # noqa: E501
        :type expires_on: datetime
        """
        self.swagger_types = {
            'session_id': str,
            'token': str,
            'expires_on': datetime
        }

        self.attribute_map = {
            'session_id': 'session_id',
            'token': 'token',
            'expires_on': 'expires_on'
        }
        self._session_id = session_id
        self._token = token
        self._expires_on = expires_on

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2001':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_1 of this InlineResponse2001.  # noqa: E501
        :rtype: InlineResponse2001
        """
        return util.deserialize_model(dikt, cls)

    @property
    def session_id(self) -> str:
        """Gets the session_id of this InlineResponse2001.


        :return: The session_id of this InlineResponse2001.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """Sets the session_id of this InlineResponse2001.


        :param session_id: The session_id of this InlineResponse2001.
        :type session_id: str
        """
        if session_id is None:
            raise ValueError("Invalid value for `session_id`, must not be `None`")  # noqa: E501

        self._session_id = session_id

    @property
    def token(self) -> str:
        """Gets the token of this InlineResponse2001.


        :return: The token of this InlineResponse2001.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token: str):
        """Sets the token of this InlineResponse2001.


        :param token: The token of this InlineResponse2001.
        :type token: str
        """

        self._token = token

    @property
    def expires_on(self) -> datetime:
        """Gets the expires_on of this InlineResponse2001.


        :return: The expires_on of this InlineResponse2001.
        :rtype: datetime
        """
        return self._expires_on

    @expires_on.setter
    def expires_on(self, expires_on: datetime):
        """Sets the expires_on of this InlineResponse2001.


        :param expires_on: The expires_on of this InlineResponse2001.
        :type expires_on: datetime
        """
        if expires_on is None:
            raise ValueError("Invalid value for `expires_on`, must not be `None`")  # noqa: E501

        self._expires_on = expires_on
