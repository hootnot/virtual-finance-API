# -*- coding: utf-8 -*-

from ..decorators import endpoint, dyndoc_insert
from ..apirequest import VirtualAPIRequest
from .responses.screener_bundle import responses
from ...exceptions import ConversionHookError
from .util import get_store
import logging


logger = logging.getLogger(__name__)


@endpoint("screener/predefined/{name}", domain="https://finance.yahoo.com")
class Screener(VirtualAPIRequest):
    """Screener - class to handle the screener endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, name):
        """Instantiate a Screener request instance.

        Parameters
        ----------
        name : string (required)
            the name of the predefined screener to perform the request for.


        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.Screener('MOST_SHORTED_STOCKS')
        >>> rv = client.request(r)

        ::

            {_predefined_screener_resp}

        """
        endpoint = self.ENDPOINT.format(name=name)
        super(Screener, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        rv = None
        try:
            rv = get_store(s, "ScreenerResultsStore")["results"]

        except Exception as err:  # noqa F841
            # let the client deal with the error
            logger.error("ConversionHookError: %s", err)
            raise ConversionHookError(422, "Unprocessable Entity")

        else:
            logger.info("%s conversion_hook: OK", self.__class__.__name__)
            return rv


@endpoint("screener", domain="https://finance.yahoo.com")
class Screeners(VirtualAPIRequest):
    """Screeners - class to handle the screeners endpoint."""

    @dyndoc_insert(responses)
    def __init__(self):
        """Instantiate a Screeners APIRequest instance.

        returns the available prefined screeners.


        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.Screeners()
        >>> rv = client.request(r)
        >>> print(json.dumps(r.response, indent=2))

        ::

            {_predefined_screeners_resp}

        """
        endpoint = self.ENDPOINT
        super(Screeners, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        rv = []
        ATTRS = ["title", "predefinedScr", "description", "canonicalName"]
        try:
            for M in get_store(s, "ScreenerStore")["predefinedList"]:
                d = {}
                for attr in ATTRS:
                    d.update({attr: M[attr]})
                rv.append(d)

        except Exception as err:  # noqa F841
            # let the client deal with the error
            raise ConversionHookError(422, "Unprocessable Entity")

        else:
            logger.info("%s conversion_hook: OK", self.__class__.__name__)
            return {"screeners": rv}
