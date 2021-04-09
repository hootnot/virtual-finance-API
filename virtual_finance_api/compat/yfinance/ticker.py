# -*- coding: utf-8 -*-

"""The Ticker-class aims to be the compatible counterpart of yfinance.Ticker.
The Ticker class basically wraps all the requests needed to represent all the
properties like yfinance.Ticker.

This class is provided for compatibility reasons. If you only need certain
data, the advise is to use the request providing that data.

If you still want the yfinance compatible output you can use one of the
*compat.yfinance.endpoints* request classes.

The other option is to use one tof the *extensions.stdjson* request classes.
These classes provide a standardized JSON response.
"""

from .endpoints.bundle import (
    Financials,
    Profile,
    Holders,
    History,
    Options
)
from virtual_finance_api.endpoints.decorators import dyndoc_insert
from virtual_finance_api.endpoints.business_insider import ISIN
from virtual_finance_api.client import Client
from .endpoints.responses.bundle import responses
import logging


logger = logging.getLogger(__name__)

# To enable communcation we need a Client instance
# The Ticker class will create a Client if there is no Client instance
client = None


class Ticker:

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Ticker instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        The constructor will instantiate all the requests needed to fetch data for certain
        properties. But the requests will only be executed when the data is asked for.


        >>> import json
        >>> import virtual_finance_api.compat.yfinance as yf
        >>> t = yf.Ticker('IBM')

        >>> # now we can use the request properties to fetch data
        >>> print(t.earnings)
        >>> print(t.quarterly_earnings)
        >>> # ... earnings as a dict with Pandas Dataframes equal to yfinance

        >>> # the dataframes combined as JSON
        >>> yq = dict([(k, json.loads(getattr(t, k).to_json())) for k in ('earnings', 'quarterly_earnings')])  # noqa E501
        >>> print(json.dumps(yq, indent=2))


        ::

            {_yf_financials_earnings_resp}

        """
        self._hparams = {
            'period': '1mo',
            'interval': '1d',
            'actions': 'True',
        }
        self._ticker = ticker

        # dict to hold request instances that only will we instantiated
        # in case the property is asked for
        self._r = {
            'profile': None,
            'financials': None,
            'holders': None,
            'options': None,
            'history': None,
            'isin': None
        }
        global client
        if client is None:
            client = Client()

    def _init(self, key, cls, attr, kwargs):
        global client

        if self._r[key] is None:
            self._r[key] = cls(**kwargs)
            try:
                client.request(self._r[key])

            except Exception as err:
                logger.error(err)
                return None

        return getattr(self._r[key], attr)

    def history(self, **kwargs):
        params = kwargs if kwargs else {}
        for k, v in self._hparams.items():
            if k not in params:
                params.update({k: self._hparams[k]})

        return self._init('history', History, 'history', kwargs={'ticker': self._ticker, 'params': params})  # noqa E501

    @property
    def isin(self):
        return self._init('isin', ISIN, 'response', kwargs={'params': {'query': self._ticker}})  # noqa E501

    @property
    def major_holders(self):
        return self._init('holders', Holders, 'major', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def institutional_holders(self):
        return self._init('holders', Holders, 'institutional', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def mutualfund_holders(self):
        return self._init('holders', Holders, 'mutualfund', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def dividends(self):
        return self._init('history', History, 'dividends', kwargs={'ticker': self._ticker, 'period': 'max'})  # noqa E501

    @property
    def splits(self):
        return self._init('history', History, 'splits', kwargs={'ticker': self._ticker, 'period': 'max'})  # noqa E501

    @property
    def actions(self):
        return self._init('history', History, 'actions', kwargs={'ticker': self._ticker, 'period': 'max'})  # noqa E501

    @property
    def info(self):
        return self._init('profile', Profile, 'info', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def calendar(self):
        return self._init('profile', Profile, 'calendar', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def recommendations(self):
        return self._init('profile', Profile, 'recommendations', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def earnings(self):
        return self._init('financials', Financials, 'earnings', kwargs={'ticker': self._ticker})['yearly']  # noqa E501

    @property
    def quarterly_earnings(self):
        return self._init('financials', Financials, 'earnings', kwargs={'ticker': self._ticker})['quarterly']  # noqa E501

    @property
    def financials(self):
        return self._init('financials', Financials, 'financials', kwargs={'ticker': self._ticker})['yearly']  # noqa E501

    @property
    def quarterly_financials(self):
        return self._init('financials', Financials, 'financials', kwargs={'ticker': self._ticker})['quarterly']  # noqa E501

    @property
    def balance_sheet(self):
        return self._init('financials', Financials, 'balancesheet', kwargs={'ticker': self._ticker})['yearly']  # noqa E501

    @property
    def quarterly_balance_sheet(self):
        return self._init('financials', Financials, 'balancesheet', kwargs={'ticker': self._ticker})['quarterly']  # noqa E501

    @property
    def balancesheet(self):
        # ... just like balance_sheeet
        return self.balance_sheet

    @property
    def quarterly_balancesheet(self):
        # ... just like quarterly_balance_sheeet
        return self.quarterly_balance_sheet

    @property
    def cashflow(self):
        return self._init('financials', Financials, 'cashflow', kwargs={'ticker': self._ticker})['yearly']  # noqa E501

    @property
    def quarterly_cashflow(self):
        return self._init('financials', Financials, 'cashflow', kwargs={'ticker': self._ticker})['quarterly']  # noqa E501

    @property
    def sustainability(self):
        return self._init('profile', Profile, 'sustainability', kwargs={'ticker': self._ticker})  # noqa E501

    @property
    def options(self):
        return self._init('options', Options, 'options', kwargs={'ticker': self._ticker})  # noqa E501

    def option_chain(self, date):
        self._init('options', Options, 'options', kwargs={'ticker': self._ticker})  # noqa E501
        return self._r['options'].option_chain(date)
