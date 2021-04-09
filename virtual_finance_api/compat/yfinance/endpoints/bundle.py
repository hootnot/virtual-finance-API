# -*- coding: utf-8 -*-
"""This module provides the *yfinance* compatible requests.

These requests are derived from the Yahoo base classes, but all classes provide
*yfinance.Ticker* compatible properties. So, some return a dict, some return
Pandas series and some return a Pandas dataframe, just like *yfinance* does.
"""

from .util import camel2title, extract_domain

import pandas as pd
import numpy as np
import virtual_finance_api.endpoints.yahoo as yhe
from .responses.bundle import responses
from virtual_finance_api.endpoints.decorators import dyndoc_insert

import logging
from datetime import datetime
from collections import namedtuple
import time


logger = logging.getLogger(__name__)


class Financials(yhe.Financials):
    """Financials - class to handle the financials endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Financials APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> # import the yfinance compatible endpoints
        >>> import virtual_finance_api.compat.yfinance.endpoints as yf
        >>> client = fa.Client()
        >>> r = yf.Financials('IBM')
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.earnings)
        >>> # ... earnings as a dict with Pandas Dataframes equal to yfinance

        .. note::
           The full response of the parent request is still available in the
           return value and the response property


        >>> # the dataframes combined as JSON
        >>> yq = dict([(k, json.loads(r.earnings[k].to_json())) for k in ('yearly', 'quarterly')])  # noqa E501
        >>> print(json.dumps(yq, indent=2))


        ::

            {_yf_financials_earnings_resp}

        """
        super(Financials, self).__init__(ticker)
        self.base = False
        self._earnings = {"yearly": None, "quarterly": None}
        self._cashflow = {"yearly": None, "quarterly": None}
        self._balancesheet = {"yearly": None, "quarterly": None}
        self._financials = {"yearly": None, "quarterly": None}

    def _processed(self, attr):
        return attr['yearly'] is not None and attr['quarterly'] is not None

    @property
    def earnings(self):
        if not self._processed(self._earnings):
            self._extract()
        return self._earnings

    @property
    def cashflow(self):
        if not self._processed(self._cashflow):
            self._extract()
        return self._cashflow

    @property
    def balancesheet(self):
        if not self._processed(self._balancesheet):
            self._extract()
        return self._balancesheet

    @property
    def financials(self):
        if not self._processed(self._financials):
            self._extract()
        return self._financials

    def _extract(self):

        def mk_dataframe(data):
            df = pd.DataFrame(data).drop(columns=['maxAge'])
            for col in df.columns:
                df[col] = np.where(df[col].astype(str) == '-', np.nan, df[col])

            df.set_index('endDate', inplace=True)
            try:
                df.index = pd.to_datetime(df.index, unit='s')

            except ValueError:
                df.index = pd.to_datetime(df.index)
            df = df.T
            df.columns.name = ''
            df.index.name = 'Breakdown'

            df.index = camel2title(df.index)
            return df

        for repgroup in (
            ('_cashflow', 'cashflowStatement', 'cashflowStatements'),
            ('_balancesheet', 'balanceSheet', 'balanceSheetStatements'),
            ('_financials', 'incomeStatement', 'incomeStatementHistory')
        ):
            attr, subject, details = repgroup
            for itemDetail, key in [('', 'yearly'), ('Quarterly', 'quarterly')]:  # noqa E501
                item = f'{subject}History{itemDetail}'
                if isinstance(self.response.get(item), dict):
                    getattr(self, attr)[key] = mk_dataframe(self.response[item][details])  # noqa E501

        # earnings
        if isinstance(self.response.get('earnings'), dict):
            earnings = self.response['earnings']['financialsChart']
            for key, title in [('yearly', 'Year'), ('quarterly', 'Quarter')]:
                df = pd.DataFrame(earnings[key]).set_index('date')
                df.columns = camel2title(df.columns)
                df.index.name = title
                self._earnings[key] = df


class Holders(yhe.Holders):
    """Holders - class to handle the holders endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Holders APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.compat.yfinance.endpoints as yf
        >>> client = fa.Client()
        >>> r = yf.Holders('IBM')
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.majors)
        >>> # ... the majors as a Pandas Dataframe equal to yfinance

        >>> # the JSON representation of the dataframe
        >>> print(r.majors.to_json())

        ::

            {_yf_holders_major_resp}

        """
        super(Holders, self).__init__(ticker)
        self.base = False
        self._holders = {}

    def _holders_by_type(self, htype):
        if not self._holders:
            self._extract()

        try:
            return self._holders[htype]

        except Exception as err:
            logger.warning("Holders: not found: %s", err)
            raise err

    @property
    def institutional(self):
        return self._holders_by_type('institutional')

    @property
    def mutualfund(self):
        return self._holders_by_type('mutualfund')

    @property
    def major(self):
        return self._holders_by_type('major')

    def _extract(self):
        self._holders = {}
        for k, v in self.response.items():
            self._holders.update({k: pd.DataFrame(v)})

        for k, df in self._holders.items():
            if 'Date Reported' in df:
                self._holders[k]['Date Reported'] = pd.to_datetime(df['Date Reported'])  # noqa E501
            if '% Out' in df:
                self._holders[k]['% Out'] = df['% Out'].str.replace('%', '').astype(float) / 100  # noqa E501


class Profile(yhe.Profile):

    """Profile - class to handle the profile endpoint."""

    COMPONENTS = ['defaultKeyStatistics', 'details', 'summaryProfile',
                  'recommendationTrend', 'financialsTemplate',
                  'earnings', 'price', 'financialData', 'quoteType',
                  'calendarEvents', 'summaryDetail', 'symbol',
                  'esgScores', 'upgradeDowngradeHistory', 'pageViews']

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Profile APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> # import the yfinance compatible endpoints
        >>> import virtual_finance_api.compat.yfinance.endpoints as yf
        >>> client = fa.Client()
        >>> r = yf.Profile('IBM')
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.calendar)
        >>> # ... the calendar as a Pandas Dataframe

        >>> # the JSON representation of the dataframe
        >>> print(r.calendar.to_json())

        ::

            {_yf_profile_calendar_resp}


        """
        super(Profile, self).__init__(ticker)

    @property
    def calendar(self):
        return self.Calendar(self)

    @property
    def recommendations(self):
        return self.Recommendations(self)

    @property
    def sustainability(self):
        return self.Sustainability(self)

    @property
    def info(self):
        return self.Info(self)

    def Sustainability(self, r):
        d = {}
        try:
            for item in r.response['esgScores']:
                if not isinstance(r.response['esgScores'][item], (dict, list)):
                    d[item] = r.response['esgScores'][item]

            s = pd.DataFrame(index=[0], data=d)[-1:].T
            s.columns = ['Value']
            s.index.name = '{:.0f}-{:.0f}'.format(
                s[s.index == 'ratingYear']['Value'].values[0],
                s[s.index == 'ratingMonth']['Value'].values[0])

        except Exception as err:
            logger.warning(err)
            return None

        else:
            return s[~s.index.isin(['maxAge', 'ratingYear', 'ratingMonth'])]

    def Calendar(self, r):
        try:
            df = pd.DataFrame(r.response['calendarEvents']['earnings'])
            df['earningsDate'] = pd.to_datetime(df['earningsDate'], unit='s')
            df = df.T
            df.index = camel2title(df.index)
            df.columns = ['Value' for c in range(len(df.columns))]

        except Exception as err:
            logger.warning(err)
            return None

        return df

    def Recommendations(self, r):
        try:
            df = pd.DataFrame(r.response['upgradeDowngradeHistory']['history'])
            df['Date'] = pd.to_datetime(df['epochGradeDate'], unit='s')
            df.set_index('Date', inplace=True)
            df.columns = camel2title(df.columns)
            df = df[['Firm', 'To Grade', 'From Grade', 'Action']].sort_index()

        except Exception as err:
            logger.warning("Recommendations: %s", err)
            return None

        return df

    def Info(self, r):
        rv = {}
        SECTIONS = ['summaryProfile', 'summaryDetail', 'quoteType',
                    'defaultKeyStatistics', 'assetProfile', 'summaryDetail']
        for section in SECTIONS:
            if isinstance(r.response.get(section), dict):
                rv.update(r.response[section])

        rv['regularMarketPrice'] = rv['regularMarketOpen']
        rv['logo_url'] = ""
        domain = extract_domain(rv['website'])
        if domain:
            rv['logo_url'] = f'https://logo.clearbit.com/{domain}'

        return rv


class Options(yhe.Options):

    """Options - class to handle the options endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker, params=None):
        """Instantiate a Profile APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> # import the yfinance compatible endpoints
        >>> import virtual_finance_api.compat.yfinance.endpoints as yf
        >>> client = fa.Client()
        >>> r = yf.Options('IBM')
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.options)
        >>> # ... the calendar as a Pandas Dataframe

        ::

            {_yf_options_options_resp}


        >>> # and, just like yfinance: the dataframes with calls and puts
        >>> print(r.option_chain('2021-03-26')[0]  # all calls
        >>> print(r.option_chain('2021-03-26')[1]  # all puts


        """
        super(Options, self).__init__(ticker, params=params)
        self._expirations = {}

    def _prep(self):
        if self.response['optionChain']['result']:
            for exp in self.response['optionChain']['result'][0]['expirationDates']:  # noqa E501
                self._expirations[datetime.utcfromtimestamp(
                    exp).strftime('%Y-%m-%d')] = exp
            return self.response['optionChain']['result'][0]['options'][0]

        return {}

    @property
    def options(self):
        if not self._expirations:
            self._option_series = self._prep()
        return tuple(sorted(self._expirations.keys()))

    def _options2df(self, opt, tz):
        COLUMNS = [
            'contractSymbol',
            'lastTradeDate',
            'strike',
            'lastPrice',
            'bid',
            'ask',
            'change',
            'percentChange',
            'volume',
            'openInterest',
            'impliedVolatility',
            'inTheMoney',
            'contractSize',
            'currency']
        df = pd.DataFrame(opt).reindex(columns=COLUMNS)
        df['lastTradeDate'] = pd.to_datetime(df['lastTradeDate'], unit='s')

        if tz is not None:
            df['lastTradeDate'] = df['lastTradeDate'].tz_localize(tz)

        return df

    def option_chain(self, date=None, proxy=None, tz=None):
        if not self._expirations:
            _ = self.options

        if date not in self._expirations:
            raise ValueError(
                    "Expiration '{}' cannot be found. "
                    "Available expiration are: [{}]".format(
                        date, ', '.join(self._expirations)))

        date = self._expirations[date]

        return namedtuple('Options', ['calls', 'puts'])(**{
            "calls": self._options2df(self._option_series['calls'], tz=tz),
            "puts": self._options2df(self._option_series['puts'], tz=tz)
        })


# =================

def parse_actions(data, atype, tz):
    df = None
    if "events" in data and atype in data["events"]:
        df = pd.DataFrame(data=list(data["events"][atype].values()))
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index, unit="s")
        df.sort_index(inplace=True)
        if tz is not None:
            df.index = df.index.tz_localize(tz)

    return df


def hprocopt(period="1mo", interval="1d", start=None, end=None, prepost=False,
             actions=True, auto_adjust=True, back_adjust=False, proxy=None,
             rounding=False, tz=None, **kwargs):

    def convtime(t):
        if isinstance(t, datetime):
            return int(time.mktime(t.timetuple()))
        else:
            return int(time.mktime(time.strptime(str(t), '%Y-%m-%d')))

    if auto_adjust and back_adjust:
        raise ValueError("auto/back adjust are mutually exclusive")

    if proxy:
        logger.warning("proxy is ignored: configure proxy via the Client")

    params = {
        "events": "div,splits",
        "interval": interval.lower(),
        "includePrePost": prepost,
        "includeAdjustedClose": True,
        "prepost": prepost,
        "actions": actions,
        "tz": tz,
        "rounding": rounding,
    }

    if auto_adjust:
        params.update({"adjust": "auto"})
    elif back_adjust:
        params.update({"adjust": "backadjust"})

    if end is None:
        params.update({"period2": int(time.time())})

    else:
        params.update({"period2": convtime(end)})

    if start:
        params.update({"period1": convtime(start)})

    else:
        if period.lower() == "max":
            params.update({"period1": -2208988800})

        else:
            params.update({"range": period.lower()})

    # 1) fix weird bug with Yahoo! - returning 60m for 30m bars
    # if params["interval"] == "30m":
    #    params["interval"] = "15m"
    return params


class History(yhe.History):
    """History - class to handle the history endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker, params):
        """Instantiate a History APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        params : dict (optional)
            dictionary with optional parameters to perform the request
            parameters default to 1 month of daily (1d) historical data.


        ::
            {_yf_history_IBM_params}

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.compat.yfinance.endpoints as yf
        >>> client = fa.Client()
        >>> r = yf.History('IBM', params=params)
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.history)
        >>> # ... the history as a Pandas Dataframe

        ::

            {_yf_history_IBM_resp}


        """
        super(History, self).__init__(ticker, params=hprocopt(**params))
        logger.info("%s instantiated, ticker: %s, params: %s",
                    self.__class__.__name__, self.ticker, self.params)
        self._history = None
        self._dividends = None
        self._splits = None

    @staticmethod
    def data_adjust(data, adjustType='auto'):
        """price adjustments for the historical data.

        for yfinance compatibility there are 2 adjustment types:
        - auto adjust
        - back adjust

        """
        df = data.copy()
        if adjustType == 'auto':
            ratio = df["Close"] / df["Adj Close"]

        elif adjustType == 'backadjust':
            ratio = df["Adj Close"] / df["Close"]

        elif adjustType is None:
            # just pass it
            logger.info('data_adjust: None')
            return data

        else:
            logger.error('data_adjust: %s invalid', adjustType)
            raise ValueError(f"Invalid parameter: {adjustType}")

        logger.info('data_adjust: %s', adjustType)

        df["Close"] = df["Adj Close"]
        df["Open"] /= ratio
        df["High"] /= ratio
        df["Low"] /= ratio

        return df[["Open", "High", "Low", "Close", "Volume"]]

    def _parse_quotes(self):
        data = self.response['chart']['result'][0]
        timestamps = data["timestamp"]
        ohlc = data["indicators"]["quote"][0]
        closes = ohlc["close"]

        adjclose = closes
        if "adjclose" in data["indicators"]:
            adjclose = data["indicators"]["adjclose"][0]["adjclose"]

        quotes = pd.DataFrame({"Open": ohlc["open"],
                               "High": ohlc["high"],
                               "Low": ohlc["low"],
                               "Close": closes,
                               "Adj Close": adjclose,
                               "Volume": ohlc['volume']})

        quotes.index = pd.to_datetime(timestamps, unit="s")
        quotes.sort_index(inplace=True)

        tz = self.params.get('tz', None)
        if tz:
            quotes.index = quotes.index.tz_localize(tz)

        if self.params.get('adjust', None):
            self._history = self.data_adjust(quotes, adjustType=self.params.get('adjust', None))  # noqa E501

        else:
            self._history = quotes

    def _parse_splits(self):
        df = pd.DataFrame(columns=["Stock Splits"])
        data = self.response['chart']['result'][0]
        _df = parse_actions(data, "splits", self.params.get('tz', None))
        if _df is not None and not _df.empty:
            _df["Stock Splits"] = _df["numerator"] / _df["denominator"]
            df = pd.concat([df, _df[['Stock Splits']]])
        self._splits = df

    def _parse_dividends(self):
        df = pd.DataFrame(columns=["Dividends"])
        data = self.response['chart']['result'][0]
        _df = parse_actions(data, "dividends", self.params.get('tz', None))
        if _df is not None and not _df.empty:
            _df.columns = ["Dividends"]
            df = pd.concat([df, _df])

        # index: date only, drop time component
        df.index = df.index.normalize()
        self._dividends = df

    @property
    def value(self):
        if self._history is not None and not self._history.empty:
            self._value = pd.concat([self.history, self.dividends, self.splits], axis=1)  # noqa E501
            for C in ['Dividends', 'Stock Splits']:
                self._value[C].fillna(0, inplace=True)
        return self._value

    @property
    def history(self):
        if self._history is None:
            try:
                self._parse_quotes()

            except Exception as err:  # noqa F841
                logger.error("No data for ticker: %s", self._ticker)

        return self._history

    @property
    def dividends(self):
        if self._dividends is None:
            try:
                self._parse_dividends()

            except Exception as err:  # noqa F841
                logger.info("No dividend data for ticker: %s "
                            "for the requested range", self._ticker)

            else:
                return self._dividends[(self._dividends.Dividends > 0)]['Dividends']  # noqa E501

        return None

    @property
    def splits(self):
        if self._splits is None:
            try:
                self._parse_splits()

            except Exception as err:  # noqa F841
                logger.info("No split data for ticker: %s "
                            "for the requested range", self._ticker)

        return self._splits
