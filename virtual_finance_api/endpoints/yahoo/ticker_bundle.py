# -*- coding: utf-8 -*-
"""All Yahoo requests that require ticker as route parameter in the request."""

from ..decorators import endpoint, dyndoc_insert
from .util import response2json
import logging
import pandas as pd
import json

from ..apirequest import APIRequest, VirtualAPIRequest
from abc import abstractmethod
from virtual_finance_api.exceptions import ConversionHookError
from .responses.ticker_bundle import responses


logger = logging.getLogger(__name__)


class Yhoo(APIRequest):
    """Yhoo - base class to handle the Yhoo endpoints that require a ticker."""

    @abstractmethod
    def __init__(self, ticker):
        """Instantiate a Yhoo APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.
        """
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(Yhoo, self).__init__(endpoint, method=self.METHOD)
        self._ticker = ticker

    @property
    def ticker(self):
        return self._ticker


@endpoint('quote/{ticker}/financials', domain='https://finance.yahoo.com')
class Financials(VirtualAPIRequest, Yhoo):
    """Financials - class to handle the financials endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Financials APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        Example
        -------

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.Financials('IBM')
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))

        ::

            {_yh_financials_resp}

        """
        super(Financials, self).__init__(ticker)

    def _conversion_hook(self, s):
        rv = None
        try:
            rv = response2json(s)

        except Exception as err:  # noqa F841
            # let the client deal with the error
            raise ConversionHookError(422, '')

        else:
            logger.info("conversion_hook: %s OK", self.ticker)
            return rv


# @endpoint('v7/finance/download/{ticker}')   # 7 or 8 ?
@endpoint('v8/finance/chart/{ticker}', response_type='json',
          domain='https://query1.finance.yahoo.com')
class History(Yhoo):
    """History - class to handle the history endpoint."""

    # @dyndoc_insert(responses)
    def __init__(self, ticker, params):
        """Instantiate a History APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        params : dict (optional)
            dictionary with optional parameters to perform the request
            parameters default to 1 month of daily (1d) historical data.
        """
        super(History, self).__init__(ticker)
        self.params = params


@endpoint('quote/{ticker}/holders', domain='https://finance.yahoo.com')
class Holders(VirtualAPIRequest, Yhoo):
    """Holders - class to handle the holders endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Holders APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        Example
        -------

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.Holders('IBM')
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))

        ::

            {_yh_holders_resp}


        """
        super(Holders, self).__init__(ticker)

    def _conversion_hook(self, s):
        # build the JSON response from the HTML
        response = {}

        try:
            data = pd.read_html(s)
            for i, k in enumerate(['major', 'institutional', 'mutualfund']):
                logger.debug("conversion_hook: %s", k)
                try:
                    response.update({k: json.loads(data[i].to_json())})

                except IndexError as iErr:  # noqa F841
                    # not always all are available
                    logger.debug("conversion_hook: %s failed, no data", k)

        except Exception as err:  # noqa F841
            # let the client deal with a 'fatal' error
            raise ConversionHookError(422, '')

        else:
            logger.info("conversion_hook: %s OK", self.ticker)
            return response


@endpoint('v7/finance/options/{ticker}',
          domain='https://query1.finance.yahoo.com',
          response_type='json')
class Options(Yhoo):
    """Options - class to handle the options endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker, params=None):
        """Instantiate a Options APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        params :
            dict with optional 'date' parameter.

        Example
        -------

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.Options('IBM')
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))

        ::

            {_yh_options_resp}

        """
        super(Options, self).__init__(ticker)
        self.params = {'p': ticker}

        if params is not None:
            self.params.update(**params)


@endpoint('quote/{ticker}', domain='https://finance.yahoo.com')
class Profile(VirtualAPIRequest, Yhoo):
    """Profile - class to handle the profile endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Profile APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        Example
        -------

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.Profile('IBM')
        >>> rv = client.request(r)
        >>> print(json.dumps(rv, indent=2))

        ::

            {_yh_profile_resp}

        """
        super(Profile, self).__init__(ticker)

    def _conversion_hook(self, s):
        rv = None
        try:
            rv = response2json(s)

        except Exception as err:  # noqa F841
            # let the client deal with the error
            raise ConversionHookError(422, '')

        else:
            logger.info("conversion_hook: %s OK", self.ticker)
            return rv
