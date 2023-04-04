# flake8: noqa
# isort: skip_file
# coding: utf-8

"""
    Frontrunner Market Maker

    This is a first draft of the FR External Market Maker API  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Market(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'injective_id': 'str',
        'created': 'datetime',
        'updated': 'datetime',
        'long_entity_id': 'str',
        'short_entity_id': 'str',
        'status': 'MarketStatus',
        'prop_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'injective_id': 'injectiveId',
        'created': 'created',
        'updated': 'updated',
        'long_entity_id': 'longEntityId',
        'short_entity_id': 'shortEntityId',
        'status': 'status',
        'prop_id': 'propId'
    }

    def __init__(self, id=None, injective_id=None, created=None, updated=None, long_entity_id=None, short_entity_id=None, status=None, prop_id=None):  # noqa: E501
        """Market - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._injective_id = None
        self._created = None
        self._updated = None
        self._long_entity_id = None
        self._short_entity_id = None
        self._status = None
        self._prop_id = None
        self.discriminator = None
        self.id = id
        self.injective_id = injective_id
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        if long_entity_id is not None:
            self.long_entity_id = long_entity_id
        if short_entity_id is not None:
            self.short_entity_id = short_entity_id
        self.status = status
        if prop_id is not None:
            self.prop_id = prop_id

    @property
    def id(self):
        """Gets the id of this Market.  # noqa: E501


        :return: The id of this Market.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Market.


        :param id: The id of this Market.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def injective_id(self):
        """Gets the injective_id of this Market.  # noqa: E501

        The marketId on Injective  # noqa: E501

        :return: The injective_id of this Market.  # noqa: E501
        :rtype: str
        """
        return self._injective_id

    @injective_id.setter
    def injective_id(self, injective_id):
        """Sets the injective_id of this Market.

        The marketId on Injective  # noqa: E501

        :param injective_id: The injective_id of this Market.  # noqa: E501
        :type: str
        """
        if injective_id is None:
            raise ValueError("Invalid value for `injective_id`, must not be `None`")  # noqa: E501

        self._injective_id = injective_id

    @property
    def created(self):
        """Gets the created of this Market.  # noqa: E501


        :return: The created of this Market.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Market.


        :param created: The created of this Market.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this Market.  # noqa: E501


        :return: The updated of this Market.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this Market.


        :param updated: The updated of this Market.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    @property
    def long_entity_id(self):
        """Gets the long_entity_id of this Market.  # noqa: E501

        The ID of the SportEntity on the long side of the market; if this side wins the market will go to 1  # noqa: E501

        :return: The long_entity_id of this Market.  # noqa: E501
        :rtype: str
        """
        return self._long_entity_id

    @long_entity_id.setter
    def long_entity_id(self, long_entity_id):
        """Sets the long_entity_id of this Market.

        The ID of the SportEntity on the long side of the market; if this side wins the market will go to 1  # noqa: E501

        :param long_entity_id: The long_entity_id of this Market.  # noqa: E501
        :type: str
        """

        self._long_entity_id = long_entity_id

    @property
    def short_entity_id(self):
        """Gets the short_entity_id of this Market.  # noqa: E501

        The ID of the SportEntity, if it exists, on the short side of the market; if this side wins the market will go to 0. If this is null, then the short side of the market is the \\'not\\' of the `longEntity`  # noqa: E501

        :return: The short_entity_id of this Market.  # noqa: E501
        :rtype: str
        """
        return self._short_entity_id

    @short_entity_id.setter
    def short_entity_id(self, short_entity_id):
        """Sets the short_entity_id of this Market.

        The ID of the SportEntity, if it exists, on the short side of the market; if this side wins the market will go to 0. If this is null, then the short side of the market is the \\'not\\' of the `longEntity`  # noqa: E501

        :param short_entity_id: The short_entity_id of this Market.  # noqa: E501
        :type: str
        """

        self._short_entity_id = short_entity_id

    @property
    def status(self):
        """Gets the status of this Market.  # noqa: E501


        :return: The status of this Market.  # noqa: E501
        :rtype: MarketStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Market.


        :param status: The status of this Market.  # noqa: E501
        :type: MarketStatus
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def prop_id(self):
        """Gets the prop_id of this Market.  # noqa: E501


        :return: The prop_id of this Market.  # noqa: E501
        :rtype: str
        """
        return self._prop_id

    @prop_id.setter
    def prop_id(self, prop_id):
        """Sets the prop_id of this Market.


        :param prop_id: The prop_id of this Market.  # noqa: E501
        :type: str
        """

        self._prop_id = prop_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Market, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Market):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
