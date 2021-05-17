# -*- coding: utf-8 -*-

from ..decorators import endpoint, dyndoc_insert
from ..apirequest import VirtualAPIRequest
from ...exceptions import ConversionHookError
from .responses.isin import responses
from virtual_finance_api.generic.isin import ISINCode


@endpoint("ajax/SearchController_Suggest", domain="https://markets.businessinsider.com")
class ISIN(VirtualAPIRequest):
    """ISIN - class to handle the ISIN endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, params: dict):
        """Instantiate a ISIN equest instance.

        Parameters
        ----------
        params : dict (required)
            max_results: 25   (default),
            query: <ticker>

        Raises
        ------

        ValueError
            in case of a missing *query* parameter.


        Example:

        params::

            {_get_isin_params}


        >>> print(client.request(ISIN(params=params)))

        ::

            {_get_isin_resp}

        """
        endpoint = self.ENDPOINT
        super(ISIN, self).__init__(endpoint, method=self.METHOD)
        self.params = {"max_results": 25}
        if "query" not in params:
            raise ValueError("Missing in 'params': 'query'")

        self.params.update(**params)

    def _conversion_hook(self, response: str):
        ticker = self.params.get("query")
        lookup = "{}|".format(ticker)

        rv = {"ticker": self.params["query"]}

        if lookup not in response:
            lookup = '"|'
            if ticker.lower() not in response.lower() or lookup not in response:
                # raise a NOT FOUND status
                raise ConversionHookError(404, "ISIN not found")

        else:
            v = response.split(lookup)[1].split('"')[0].split("|")[0]
            try:
                _isin = ISINCode(v)

            except ValueError as err:
                raise ConversionHookError(422, "Unprocessable Entity")

            else:
                rv.update({"ISIN": _isin.code})

        return rv
