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

class Prop(object):
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
        'league_id': 'str',
        'name': 'str',
        'prop_type': 'str',
        'created': 'datetime',
        'updated': 'datetime',
        'sport_event_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'league_id': 'leagueId',
        'name': 'name',
        'prop_type': 'propType',
        'created': 'created',
        'updated': 'updated',
        'sport_event_id': 'sportEventId'
    }

    def __init__(self, id=None, league_id=None, name=None, prop_type=None, created=None, updated=None, sport_event_id=None):  # noqa: E501
        """Prop - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._league_id = None
        self._name = None
        self._prop_type = None
        self._created = None
        self._updated = None
        self._sport_event_id = None
        self.discriminator = None
        self.id = id
        if league_id is not None:
            self.league_id = league_id
        self.name = name
        if prop_type is not None:
            self.prop_type = prop_type
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        if sport_event_id is not None:
            self.sport_event_id = sport_event_id

    @property
    def id(self):
        """Gets the id of this Prop.  # noqa: E501


        :return: The id of this Prop.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Prop.


        :param id: The id of this Prop.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def league_id(self):
        """Gets the league_id of this Prop.  # noqa: E501


        :return: The league_id of this Prop.  # noqa: E501
        :rtype: str
        """
        return self._league_id

    @league_id.setter
    def league_id(self, league_id):
        """Sets the league_id of this Prop.


        :param league_id: The league_id of this Prop.  # noqa: E501
        :type: str
        """

        self._league_id = league_id

    @property
    def name(self):
        """Gets the name of this Prop.  # noqa: E501


        :return: The name of this Prop.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Prop.


        :param name: The name of this Prop.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def prop_type(self):
        """Gets the prop_type of this Prop.  # noqa: E501


        :return: The prop_type of this Prop.  # noqa: E501
        :rtype: str
        """
        return self._prop_type

    @prop_type.setter
    def prop_type(self, prop_type):
        """Sets the prop_type of this Prop.


        :param prop_type: The prop_type of this Prop.  # noqa: E501
        :type: str
        """
        allowed_values = ["winner", "team_prop", "player_prop", "other"]  # noqa: E501
        if prop_type not in allowed_values:
            raise ValueError(
                "Invalid value for `prop_type` ({0}), must be one of {1}"  # noqa: E501
                .format(prop_type, allowed_values)
            )

        self._prop_type = prop_type

    @property
    def created(self):
        """Gets the created of this Prop.  # noqa: E501


        :return: The created of this Prop.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Prop.


        :param created: The created of this Prop.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this Prop.  # noqa: E501


        :return: The updated of this Prop.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this Prop.


        :param updated: The updated of this Prop.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    @property
    def sport_event_id(self):
        """Gets the sport_event_id of this Prop.  # noqa: E501


        :return: The sport_event_id of this Prop.  # noqa: E501
        :rtype: str
        """
        return self._sport_event_id

    @sport_event_id.setter
    def sport_event_id(self, sport_event_id):
        """Sets the sport_event_id of this Prop.


        :param sport_event_id: The sport_event_id of this Prop.  # noqa: E501
        :type: str
        """

        self._sport_event_id = sport_event_id

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
        if issubclass(Prop, dict):
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
        if not isinstance(other, Prop):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
