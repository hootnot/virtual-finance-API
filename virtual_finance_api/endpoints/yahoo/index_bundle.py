# -*- coding: utf-8 -*-

from ..decorators import endpoint, dyndoc_insert
from ..apirequest import VirtualAPIRequest
import pandas as pd
import json
import logging
from .responses.index_bundle import responses
from ...exceptions import ConversionHookError


logger = logging.getLogger(__name__)


@endpoint('quote/{index}/components', domain='https://finance.yahoo.com')
class YhooIndex(VirtualAPIRequest):
    """YhooIndex - request class to handle the index overview endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, index):
        """Instantiate a YhooIndex APIRequest instance.

        Parameters
        ----------
        index : string (required)
            the ticker of the index to perform the request for.

        Example
        -------

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.YhooIndex('^IXIC')
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))


        ::

            {_endpoints_yh_yahooindex_resp}

        """
        endpoint = self.ENDPOINT.format(index=index)
        super(YhooIndex, self).__init__(endpoint, method=self.METHOD)

        # this url takes index as a route parameter, but also as a query param
        # normally params get passed via the constructor, but since this one
        # is redundant, we create it here
        self.params = {'p': index}
        self._index = index

    @property
    def index(self):
        return self._index

    def _conversion_hook(self, s):
        rv = None
        try:
            data = pd.read_html(s)
            rv = json.loads(data[0].to_json())

        except Exception as err:  # noqa F841
            # let the client deal with the error
            raise ConversionHookError(422, '')

        else:
            logger.info("%s conversion_hook: %s OK",
                        self.__class__.__name__, self.index)
            return rv
