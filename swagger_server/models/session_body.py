# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SessionBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, session_id: str=None, app_id: str=None, signature: str=None, node_pubkey: str=None):  # noqa: E501
        """SessionBody - a model defined in Swagger

        :param session_id: The session_id of this SessionBody.  # noqa: E501
        :type session_id: str
        :param app_id: The app_id of this SessionBody.  # noqa: E501
        :type app_id: str
        :param signature: The signature of this SessionBody.  # noqa: E501
        :type signature: str
        :param node_pubkey: The node_pubkey of this SessionBody.  # noqa: E501
        :type node_pubkey: str
        """
        self.swagger_types = {
            'session_id': str,
            'app_id': str,
            'signature': str,
            'node_pubkey': str
        }

        self.attribute_map = {
            'session_id': 'session_id',
            'app_id': 'app_id',
            'signature': 'signature',
            'node_pubkey': 'node_pubkey'
        }
        self._session_id = session_id
        self._app_id = app_id
        self._signature = signature
        self._node_pubkey = node_pubkey

    @classmethod
    def from_dict(cls, dikt) -> 'SessionBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The session_body of this SessionBody.  # noqa: E501
        :rtype: SessionBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def session_id(self) -> str:
        """Gets the session_id of this SessionBody.


        :return: The session_id of this SessionBody.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """Sets the session_id of this SessionBody.


        :param session_id: The session_id of this SessionBody.
        :type session_id: str
        """
        if session_id is None:
            raise ValueError("Invalid value for `session_id`, must not be `None`")  # noqa: E501

        self._session_id = session_id

    @property
    def app_id(self) -> str:
        """Gets the app_id of this SessionBody.

        serves as identifier of the application  # noqa: E501

        :return: The app_id of this SessionBody.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id: str):
        """Sets the app_id of this SessionBody.

        serves as identifier of the application  # noqa: E501

        :param app_id: The app_id of this SessionBody.
        :type app_id: str
        """

        self._app_id = app_id

    @property
    def signature(self) -> str:
        """Gets the signature of this SessionBody.

        token signed with the node's private key, in zbase32 format  # noqa: E501

        :return: The signature of this SessionBody.
        :rtype: str
        """
        return self._signature

    @signature.setter
    def signature(self, signature: str):
        """Sets the signature of this SessionBody.

        token signed with the node's private key, in zbase32 format  # noqa: E501

        :param signature: The signature of this SessionBody.
        :type signature: str
        """
        if signature is None:
            raise ValueError("Invalid value for `signature`, must not be `None`")  # noqa: E501

        self._signature = signature

    @property
    def node_pubkey(self) -> str:
        """Gets the node_pubkey of this SessionBody.


        :return: The node_pubkey of this SessionBody.
        :rtype: str
        """
        return self._node_pubkey

    @node_pubkey.setter
    def node_pubkey(self, node_pubkey: str):
        """Sets the node_pubkey of this SessionBody.


        :param node_pubkey: The node_pubkey of this SessionBody.
        :type node_pubkey: str
        """

        self._node_pubkey = node_pubkey
