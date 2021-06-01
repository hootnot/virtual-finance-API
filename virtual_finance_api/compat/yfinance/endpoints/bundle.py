# -*- coding: utf-8 -*-
"""This module provides the *yfinance* compatible requests.

These requests are derived from the Yahoo base classes, but all classes provide
*yfinance.Ticker* compatible properties. So, some return a dict, some return
Pandas series and some return a Pandas dataframe, just like *yfinance* does.
"""

from .util import camel2title, YFHolders, yfprocopt
from virtual_finance_api.endpoints.yahoo.util import extract_domain

import pandas as pd
import numpy as np
import virtual_finance_api.endpoints.yahoo as yhe
from .responses.bundle import responses
from virtual_finance_api.endpoints.decorators import dyndoc_insert

import logging
from datetime import datetime as dt
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
        >>> yq = dict([(k, json.loads(r.earnings[k].to_json())) for k in ('yearly', 'quarterly')])
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
        return attr["yearly"] is not None and attr["quarterly"] is not None

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
        def mk_dataframe(data, key):

            # earnings uses date, the others endDate
            if "endDate" in data[0]:
                df = pd.DataFrame(data)
                if "maxAge" in df.columns:
                    df = df.drop(columns=["maxAge"])
                for col in df.columns:
                    df[col] = np.where(df[col].astype(str) == "-", np.nan, df[col])

                df.set_index("endDate", inplace=True)
                try:
                    df.index = pd.to_datetime(df.index, unit="s")

                except ValueError:
                    df.index = pd.to_datetime(df.index)

                else:
                    df = df.T
                    df.columns.name = ""
                    df.index.name = "Breakdown"
                    df.index = camel2title(df.index)

            else:  # earnings...
                titles = {"quarterly": "Quarter", "yearly": "Year"}
                df = pd.DataFrame(data)
                df.set_index("date", inplace=True)
                df.columns = camel2title(df.columns)
                df.index.name = titles[key]

            return df

        for k, v in self.response.items():
            for _k, _v in v.items():
                getattr(self, f"_{k}")[_k] = mk_dataframe(_v, key=_k)


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
        return self._holders_by_type("institutional")

    @property
    def mutualfund(self):
        return self._holders_by_type("mutualfund")

    @property
    def major(self):
        return self._holders_by_type("major")

    def _extract(self):
        self._holders = {}
        cnv = YFHolders(self.response)

        for k, v in (cnv.major()).items():
            self._holders.update({k: pd.DataFrame(v)})

        for k in ["mutualfund", "institutional"]:
            df = pd.DataFrame((getattr(cnv, k)())[k])
            self._holders.update({k: df})

        for k, df in self._holders.items():
            if "Date Reported" in df:
                self._holders[k]["Date Reported"] = pd.to_datetime(df["Date Reported"])

            if "% Out" in df:
                logger.warning(
                    "% Out is a % column. yfinance divides it by 100 "
                    "but still presents it as a percentage"
                )
                self._holders[k]["% Out"] = df["% Out"].astype(float) / 100


class Profile(yhe.Profile):

    """Profile - class to handle the profile endpoint."""

    COMPONENTS = [
        "defaultKeyStatistics",
        "details",
        "summaryProfile",
        "recommendationTrend",
        "financialsTemplate",
        "earnings",
        "price",
        "financialData",
        "quoteType",
        "calendarEvents",
        "summaryDetail",
        "symbol",
        "esgScores",
        "upgradeDowngradeHistory",
        "pageViews",
    ]

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
        return self.Calendar()

    @property
    def recommendations(self):
        return self.Recommendations()

    @property
    def sustainability(self):
        return self.Sustainability()

    @property
    def info(self):
        return self.Info()

    def Sustainability(self):
        d = {}
        try:
            for item in self.response["sustainability"]:
                if not isinstance(self.response["sustainability"][item], (dict, list)):
                    d[item] = self.response["sustainability"][item]

            s = pd.DataFrame(index=[0], data=d)[-1:].T
            s.columns = ["Value"]
            s.index.name = "{:.0f}-{:.0f}".format(
                s[s.index == "ratingYear"]["Value"].values[0],
                s[s.index == "ratingMonth"]["Value"].values[0],
            )

        except Exception as err:
            logger.warning(err)
            return None

        else:
            return s[~s.index.isin(["maxAge", "ratingYear", "ratingMonth"])]

    def Calendar(self):
        try:
            df = pd.DataFrame(self.response["calendar"]["earnings"])
            df["earningsDate"] = pd.to_datetime(df["earningsDate"], unit="s")
            df = df.T

            df.index = camel2title(df.index)
            df.columns = ["Value" for C in range(len(df.columns))]

        except Exception as err:
            logger.warning(err)
            return None

        return df

    def Recommendations(self):
        try:
            df = pd.DataFrame(self.response["recommendations"])
            df["Date"] = pd.to_datetime(df["epochGradeDate"], unit="s")
            df.set_index("Date", inplace=True)
            df.columns = camel2title(df.columns)
            df = df[["Firm", "To Grade", "From Grade", "Action"]].sort_index()

        except Exception as err:
            logger.warning("Recommendations: %s", err)
            return None

        return df

    def Info(self):
        return self.response["info"]


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
        >>> # ... all the expiration dates

        ::

            {_yf_options_options_resp}


        >>> # and, just like yfinance: the dataframes with calls and puts
        >>> print(r.option_chain('2021-03-26')[0]  # all calls
        >>> print(r.option_chain('2021-03-26')[1]  # all puts


        """
        super(Options, self).__init__(ticker, params=params)
        self._expirations = {}

    def _prep(self):
        if "expirationDates" in self.response:
            for exp in self.response["expirationDates"]:
                self._expirations[dt.utcfromtimestamp(exp).strftime("%Y-%m-%d")] = exp

    @property
    def options(self):
        if not self._expirations:
            self._prep()
        return tuple(sorted(self._expirations.keys()))

    def _options2df(self, opt, tz):
        COLUMNS = [
            "contractSymbol",
            "lastTradeDate",
            "strike",
            "lastPrice",
            "bid",
            "ask",
            "change",
            "percentChange",
            "volume",
            "openInterest",
            "impliedVolatility",
            "inTheMoney",
            "contractSize",
            "currency",
        ]
        df = pd.DataFrame(opt).reindex(columns=COLUMNS)
        df["lastTradeDate"] = pd.to_datetime(df["lastTradeDate"], unit="s")

        if tz is not None:
            df["lastTradeDate"] = df["lastTradeDate"].tz_localize(tz)

        return df

    def option_chain(self, date=None, proxy=None, tz=None):
        """option_chain - return option chain dataframes for calls/puts."""
        if not self._expirations:
            _ = self.options

        # there is only one date since the optionseries are fetched by date
        # passing an expiration date that does not match with current series
        # raises a ValueError. From the Ticker class this is handled by
        # a request to fetch the series for that date first
        if date is not None and date not in self._expirations:
            raise ValueError(
                "Expiration '{}' cannot be found. "
                "Available expiration are: [{}]".format(
                    date, ", ".join(self._expirations)
                )
            )

            date = self._expirations[date]

        _calls = [
            S
            for S in self.response["options"][0]["calls"]
            if date is None or S["expiration"] == date
        ]
        _puts = [
            S
            for S in self.response["options"][0]["puts"]
            if date is None or S["expiration"] == date
        ]
        return namedtuple("Options", ["calls", "puts"])(
            **{
                "calls": self._options2df(_calls, tz=tz),
                "puts": self._options2df(_puts, tz=tz),
            }
        )


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
        tparams = yfprocopt(**params)
        super(History, self).__init__(ticker, params=tparams)
        logger.info(
            "%s instantiated, ticker: %s, params: %s",
            self.__class__.__name__,
            self.ticker,
            self.params,
        )
        self._history = None
        self._dividends = None
        self._splits = None

    @property
    def history(self):
        if self._history is None:
            try:
                ohlc = self.response["ohlcdata"]
                self._history = pd.DataFrame(
                    {
                        "Date": ohlc["timestamp"],
                        "Open": ohlc["open"],
                        "High": ohlc["high"],
                        "Low": ohlc["low"],
                        "Close": ohlc["close"],
                        "Adj Close": ohlc["adjclose"],
                        "Volume": ohlc["volume"],
                    }
                ).set_index("Date")
                self._history.index = pd.to_datetime(self._history.index, unit="s")

            except Exception as err:
                logger.error(
                    "Error building data frame for ticker: %s [%s]", self._ticker, err
                )

        return self._history

    @property
    def dividends(self):
        df = pd.DataFrame(columns=["Dividends"])
        if len(self.response["dividends"]):
            df = pd.DataFrame(self.response["dividends"])
            df = df.rename(columns={"amount": "Dividends"})
            df.set_index("date", inplace=True)
            df.index = pd.to_datetime(df.index, unit="s").date  # keep only the date
            df.sort_index(inplace=True)

        else:
            logger.info(
                "No dividend data for ticker: %s for the requested range", self._ticker
            )

        return df["Dividends"]

    @property
    def splits(self):
        df = pd.DataFrame(columns=["Stock Splits"])
        if len(self.response["splits"]):
            df = pd.DataFrame(self.response["splits"])
            df.set_index("date", inplace=True)
            df.index = pd.to_datetime(df.index, unit="s").date  # keep only the date
            df.sort_index(inplace=True)
            df["Stock Splits"] = df["numerator"] / df["denominator"]

        else:
            logger.info(
                "No split data for ticker: %s for the requested range", self._ticker
            )

        return df["Stock Splits"]

    @property
    def actions(self):
        return pd.DataFrame(pd.concat([self.dividends, self.splits], axis=1)).replace(
            np.NaN, 0.0
        )
