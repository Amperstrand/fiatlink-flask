# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2002(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, session_id: str=None, app_id: str=None, expires_on: datetime=None):  # noqa: E501
        """InlineResponse2002 - a model defined in Swagger

        :param session_id: The session_id of this InlineResponse2002.  # noqa: E501
        :type session_id: str
        :param app_id: The app_id of this InlineResponse2002.  # noqa: E501
        :type app_id: str
        :param expires_on: The expires_on of this InlineResponse2002.  # noqa: E501
        :type expires_on: datetime
        """
        self.swagger_types = {
            'session_id': str,
            'app_id': str,
            'expires_on': datetime
        }

        self.attribute_map = {
            'session_id': 'session_id',
            'app_id': 'app_id',
            'expires_on': 'expires_on'
        }
        self._session_id = session_id
        self._app_id = app_id
        self._expires_on = expires_on

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2002':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_2 of this InlineResponse2002.  # noqa: E501
        :rtype: InlineResponse2002
        """
        return util.deserialize_model(dikt, cls)

    @property
    def session_id(self) -> str:
        """Gets the session_id of this InlineResponse2002.


        :return: The session_id of this InlineResponse2002.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """Sets the session_id of this InlineResponse2002.


        :param session_id: The session_id of this InlineResponse2002.
        :type session_id: str
        """
        if session_id is None:
            raise ValueError("Invalid value for `session_id`, must not be `None`")  # noqa: E501

        self._session_id = session_id

    @property
    def app_id(self) -> str:
        """Gets the app_id of this InlineResponse2002.


        :return: The app_id of this InlineResponse2002.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id: str):
        """Sets the app_id of this InlineResponse2002.


        :param app_id: The app_id of this InlineResponse2002.
        :type app_id: str
        """

        self._app_id = app_id

    @property
    def expires_on(self) -> datetime:
        """Gets the expires_on of this InlineResponse2002.


        :return: The expires_on of this InlineResponse2002.
        :rtype: datetime
        """
        return self._expires_on

    @expires_on.setter
    def expires_on(self, expires_on: datetime):
        """Sets the expires_on of this InlineResponse2002.


        :param expires_on: The expires_on of this InlineResponse2002.
        :type expires_on: datetime
        """
        if expires_on is None:
            raise ValueError("Invalid value for `expires_on`, must not be `None`")  # noqa: E501

        self._expires_on = expires_on
