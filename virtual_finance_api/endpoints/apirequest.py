# -*- coding: utf-8 -*-

"""Handling of API requests."""
from abc import ABC, abstractmethod


class APIRequest(ABC):
    """Base Class for API-request classes."""

    @abstractmethod
    def __init__(self, endpoint, method="GET", expected_status=200):
        """Instantiate an API request.

        Parameters
        ----------
        endpoint : string
            the URL format string
        method : string
            the method for the request. Default: GET.
        """
        self._expected_status = expected_status
        self._status_code = None
        self._response = None

        self._endpoint = endpoint
        self.method = method

    @property
    def expected_status(self):
        return self._expected_status

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value):
        # if value != self._expected_status:
        #    raise ValueError("{} {} {:d}".format(self, self.method, value))
        self._status_code = value

    @property
    def response(self):
        """response - get the response of the request."""
        return self._response

    @response.setter
    def response(self, value):
        """response - set the response of the request."""
        self._response = value

    def __str__(self):
        """return the endpoint."""
        return self._endpoint


class VirtualAPIRequest(APIRequest):
    """Base Class for Virtual API-request classes.

    A VirtualAPI request is a regular (Non-REST) HTTP request that returns
    a HTML page. The _conversion_hook() method parses the html into the
    wanted (JSON) response.
    """

    @abstractmethod
    def _conversion_hook(self, s):
        return s
