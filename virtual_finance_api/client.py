# -*- coding: utf-8 -*-

import requests
import logging

try:
    import rapidjson as json
except ImportError as err:  # noqa F841
    import json

from .exceptions import (
    VirtualFinanceAPIError,
    ConversionHookError
)
from .endpoints.apirequest import VirtualAPIRequest

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "Accept-Encoding": "gzip, deflate"
}


class Client:

    def __init__(self, headers=None, request_params=None):
        """Instantiate a Client instance.

        Parameters
        ----------

        headers : dict (optional)
            optional headers to set to requests

        request_params : dict (optional)
            optional parameters to set to requests


        for details pls. check requests.readthedocs.io


        Example
        -------

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> import json
        >>> client = fa.Client()
        >>> r = yh.Profile('IBM')
        >>> try:
        ...    rv = client.request(r)
        ... except VirtualFinanceAPIError as err:
        ...    print(err)
        ... else:
        ...    print(json.dumps(rv['pageViews'], indent=2))
        {
          "shortTermTrend": "NEUTRAL",
          "midTermTrend": "UP",
          "longTermTrend": "UP",
          "maxAge": 1
        }

        """
        self._client = requests.Session()
        self._request_params = request_params if request_params else {}

        self._client.headers.update(DEFAULT_HEADERS)
        if headers:
            self._client.headers.update(headers)
            logger.info("applying headers %s", ",".join(headers.keys()))

    @property
    def request_params(self):
        """request_params property."""
        return self._request_params

    def request(self, endpoint):
        """Perform a request for the APIRequest instance 'endpoint'.

        Parameters
        ----------

        endpoint : APIRequest (required)
            The endpoint parameter contains an instance of an APIRequest
            containing the endpoint, method and optionally other parameters
            or body data.

        Raises
        ------

        VirtualFinanceAPIError
            in case of HTTP response code >= 400

        requests-lib exceptions
            Possible exceptions from the requests library, those are
            re-raised.

        """
        method = endpoint.method.lower()
        params = None
        try:
            params = getattr(endpoint, "params")
        except AttributeError:
            # request does not have params
            params = {}

        headers = {}
        if hasattr(endpoint, "HEADERS"):
            headers = getattr(endpoint, "HEADERS")

        request_args = {}
        if method == 'get':
            request_args['params'] = params
        elif hasattr(endpoint, "data") and endpoint.data:
            request_args['json'] = endpoint.data

        # if any parameter for request then merge them
        request_args.update(self._request_params)

        url = "{}/{}".format(endpoint.DOMAIN, endpoint)

        # perform the actual request
        func = getattr(self._client, method)
        headers = headers if headers else {}
        response = None
        content = None
        try:
            logger.info("performing request %s", url)
            response = func(url, headers=headers, **request_args)

            # in case of a virtual request:
            # process the primary response into the desired response
            # by calling the _conversion_hook
            if hasattr(endpoint, '_conversion_hook'):
                # only allow _conversion_hook for VirtualAPIRequest instances
                assert isinstance(endpoint, VirtualAPIRequest)
                try:
                    content = endpoint._conversion_hook(
                            response.content.decode('utf-8'))

                except ConversionHookError as err:
                    logger.error("%s: conversion error: %s", endpoint, err)
                    endpoint.status_code = err.code

                    # raise exception just as if the server returned a 4xx code
                    raise VirtualFinanceAPIError(endpoint.status_code, err)

                # to prevent back and forth conversion to keep the flow correct
                # lets hack a bit and keep track of the already converted
                # content in the content variable

                # else:
                #     # response content is read-only
                #     setattr(response, '_content',
                #             json.dumps(content).encode('utf-8'))

        except requests.RequestException as err:
            logger.error("request %s failed [%s]", url, err)
            raise err

        # Handle error responses
        if response.status_code >= 400:
            logger.error("request %s failed [%d,%s]",
                         url,
                         response.status_code,
                         response.content.decode('utf-8'))
            raise VirtualFinanceAPIError(response.status_code,
                                         response.content.decode('utf-8'))

        if content is None:
            content = response.content.decode('utf-8')
        endpoint.status_code = response.status_code

        if endpoint.RESPONSE_TYPE == 'json':
            try:
                if isinstance(content, str):
                    content = json.loads(content)

            except Exception as err:
                logger.error("Error loading JSON response ... %s", err)
                raise ValueError(f"request: {endpoint}, "
                                 "response could not be loaded as JSON")

            # else:
            #   if not isinstance(content, (list, dict)):
            #       raise ValueError("request: %s, expected response: 'json', "
            #                        "got: %s", endpoint, type(content))

        # update endpoint
        endpoint.response = content

        return content
