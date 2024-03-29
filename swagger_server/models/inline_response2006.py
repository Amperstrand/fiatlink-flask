# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2006(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, currencies: List[Dict[str, object]]=None):  # noqa: E501
        """InlineResponse2006 - a model defined in Swagger

        :param currencies: The currencies of this InlineResponse2006.  # noqa: E501
        :type currencies: List[Dict[str, object]]
        """
        self.swagger_types = {
            'currencies': List[Dict[str, object]]
        }

        self.attribute_map = {
            'currencies': 'currencies'
        }
        self._currencies = currencies

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2006':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_6 of this InlineResponse2006.  # noqa: E501
        :rtype: InlineResponse2006
        """
        return util.deserialize_model(dikt, cls)

    @property
    def currencies(self) -> List[Dict[str, object]]:
        """Gets the currencies of this InlineResponse2006.


        :return: The currencies of this InlineResponse2006.
        :rtype: List[Dict[str, object]]
        """
        return self._currencies

    @currencies.setter
    def currencies(self, currencies: List[Dict[str, object]]):
        """Sets the currencies of this InlineResponse2006.


        :param currencies: The currencies of this InlineResponse2006.
        :type currencies: List[Dict[str, object]]
        """

        self._currencies = currencies
