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

class SportEvent(object):
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
        'name': 'str',
        'event_type': 'str',
        'start_time': 'datetime',
        'created': 'datetime',
        'updated': 'datetime',
        'league_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'event_type': 'eventType',
        'start_time': 'startTime',
        'created': 'created',
        'updated': 'updated',
        'league_id': 'leagueId'
    }

    def __init__(self, id=None, name=None, event_type=None, start_time=None, created=None, updated=None, league_id=None):  # noqa: E501
        """SportEvent - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._event_type = None
        self._start_time = None
        self._created = None
        self._updated = None
        self._league_id = None
        self.discriminator = None
        self.id = id
        self.name = name
        if event_type is not None:
            self.event_type = event_type
        if start_time is not None:
            self.start_time = start_time
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        if league_id is not None:
            self.league_id = league_id

    @property
    def id(self):
        """Gets the id of this SportEvent.  # noqa: E501


        :return: The id of this SportEvent.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SportEvent.


        :param id: The id of this SportEvent.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this SportEvent.  # noqa: E501


        :return: The name of this SportEvent.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SportEvent.


        :param name: The name of this SportEvent.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def event_type(self):
        """Gets the event_type of this SportEvent.  # noqa: E501


        :return: The event_type of this SportEvent.  # noqa: E501
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this SportEvent.


        :param event_type: The event_type of this SportEvent.  # noqa: E501
        :type: str
        """
        allowed_values = ["game", "future"]  # noqa: E501
        if event_type not in allowed_values:
            raise ValueError(
                "Invalid value for `event_type` ({0}), must be one of {1}"  # noqa: E501
                .format(event_type, allowed_values)
            )

        self._event_type = event_type

    @property
    def start_time(self):
        """Gets the start_time of this SportEvent.  # noqa: E501

        The start time, if applicable, of the SportEvent  # noqa: E501

        :return: The start_time of this SportEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this SportEvent.

        The start time, if applicable, of the SportEvent  # noqa: E501

        :param start_time: The start_time of this SportEvent.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def created(self):
        """Gets the created of this SportEvent.  # noqa: E501


        :return: The created of this SportEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this SportEvent.


        :param created: The created of this SportEvent.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this SportEvent.  # noqa: E501


        :return: The updated of this SportEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this SportEvent.


        :param updated: The updated of this SportEvent.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    @property
    def league_id(self):
        """Gets the league_id of this SportEvent.  # noqa: E501


        :return: The league_id of this SportEvent.  # noqa: E501
        :rtype: str
        """
        return self._league_id

    @league_id.setter
    def league_id(self, league_id):
        """Sets the league_id of this SportEvent.


        :param league_id: The league_id of this SportEvent.  # noqa: E501
        :type: str
        """

        self._league_id = league_id

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
        if issubclass(SportEvent, dict):
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
        if not isinstance(other, SportEvent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
