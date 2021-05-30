# -*- coding: utf-8 -*-
"""All Yahoo requests that require ticker as route parameter in the request."""

from ..decorators import endpoint, dyndoc_insert
from .util import response2json, extract_domain, hprocopt

import logging
import pandas as pd

try:
    import rapidjson as json

except ImportError as err:
    import json

from ..apirequest import APIRequest, VirtualAPIRequest
from abc import abstractmethod
from virtual_finance_api.exceptions import ConversionHookError
from .responses.ticker_bundle import responses
from .types import AdjustType


logger = logging.getLogger(__name__)


class Yhoo(APIRequest):
    """Yhoo - base class to handle the Yhoo endpoints that require a ticker."""

    @abstractmethod
    def __init__(self, ticker: str) -> None:
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
    def ticker(self) -> str:
        return self._ticker


@endpoint("quote/{ticker}/financials", domain="https://finance.yahoo.com")
class Financials(VirtualAPIRequest, Yhoo):
    """Financials - class to handle the financials endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker: str) -> None:
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

    def _conversion_hook(self, s: str) -> dict:
        """transform the response into a 'standardized' JSON response

        for all groups we want to have yearly and quarterly, like:

        {'cashflow': {
            'yearly': { ...},
            'quarterly': { ...},
          },
          ...
        }
        """
        data = None
        _resp = {}

        try:
            data = response2json(s)

            for repgroup in (
                ("cashflow", "cashflowStatement", "cashflowStatements"),
                ("balancesheet", "balanceSheet", "balanceSheetStatements"),
                ("financials", "incomeStatement", "incomeStatementHistory"),
            ):
                attr, subject, details = repgroup
                for itemDetail, key in [("", "yearly"), ("Quarterly", "quarterly")]:
                    item = f"{subject}History{itemDetail}"
                    if isinstance(data.get(item), dict):
                        if attr not in _resp:
                            _resp.update({attr: {}})
                        _resp[attr].update({key: data[item][details]})

            # earnings
            if data.get("earnings", None):
                _resp.update({"earnings": {}})
                earnings = data["earnings"]["financialsChart"]
                _resp.update({"earnings": data["earnings"]["financialsChart"]})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, "")

        else:
            logger.info("conversion_hook: %s OK", self.ticker)
            return _resp


@endpoint(
    "v8/finance/chart/{ticker}",
    response_type="json",
    domain="https://query1.finance.yahoo.com",
)
class History(VirtualAPIRequest, Yhoo):
    """History - class to handle the history endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker: str, params: dict) -> None:
        """Instantiate a History APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        params : dict (optional)
            dictionary with optional parameters to perform the request,
            parameters default to 1 month of daily (1d) historical data.


        ::
            {_yh_history_params}


        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.endpoints.yahoo as yh
        >>> client = fa.Client()
        >>> r = yh.History('IBM', params=params)
        >>> rv = client.request(r)

        >>> print(r.response)

        ::

            {_yh_history_resp}


        """
        super(History, self).__init__(ticker)
        self.params = hprocopt(**params)

        logger.info(
            "%s instantiated, ticker: %s, params: %s",
            self.__class__.__name__,
            self.ticker,
            self.params,
        )

    def _conversion_hook(self, s: str) -> dict:
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            {
               'ohlcdata': {...},
               'dividends': {...},
               'spits': {...},
            }

        """

        def _ordered_timeitems(d: dict, cat: str) -> list:
            """
            dividends / splits
            yahoo has dicts with items like:
                "878826600": {
                   "amount": 0.1,
                   "date": 878826600
                },
            string type epoch as key, numeric value in the value dict
            this function transforms these dicts in a list of (epoch)
            ordered value dicts:
                [ {...},
                  {
                   "amount": 0.1,
                   "date": 878826600
                },
                ...
               ]
            """
            try:
                res = [d[cat][str(k)] for k in sorted(int(dt) for dt in d[cat].keys())]

            except Exception as err:
                logger.info("no data for: cat %s", cat)
                return []

            else:
                return res

        def adjust(ohlcdata, adjustType: AdjustType = None) -> dict:
            """price adjustments for the historical data.

            for yfinance compatibility there are 2 adjustment types:
            - auto adjust
            - back adjust

            ohlcdata is: { 'timestamp': [...],
                           'open': [...],
                           'high': [...],
                           'low': [...],
                           'close': [...],
                           'volume': [...]}
            """
            if adjustType.value == AdjustType.auto:
                num, denom = "close", "adjclose"

            elif adjustType.value == AdjustType.backadjust:
                num, denom = "adjclose", "close"

            else:
                logger.warning("adjust: not set, returning plain data")
                return ohlcdata

            ratio = [
                ohlcdata[num][i] / ohlcdata[denom][i]
                for i in range(len(ohlcdata["close"]))
            ]

            ohlcdata["close"] = ohlcdata["adjclose"]
            for qc in ["open", "high", "low"]:
                ohlcdata[qc] = [
                    ohlcdata[qc][i] / ratio[i] for i in range(len(ohlcdata["close"]))
                ]

            return ohlcdata

        # transform the yahoo data
        tdata = {}

        try:
            resp = json.loads(s)
            _data = resp["chart"]["result"][0]
            tdata.update({"meta": _data["meta"]})
            tdata.update({"ohlcdata": {}})
            tdata["ohlcdata"].update({"timestamp": _data["timestamp"]})
            tdata["ohlcdata"].update(_data["indicators"]["quote"][0])
            tdata["ohlcdata"].update(_data["indicators"]["adjclose"][0])
            if "events" in _data:
                for cat in ["dividends", "splits"]:
                    try:
                        tdata.update({cat: _ordered_timeitems(_data["events"], cat)})

                    except Exception as err:
                        logger.warning(
                            "no events for %s cat: %s [%s]", self.ticker, cat, err
                        )

                    else:
                        logger.info(
                            "added: %s cat: %s, #%s", self.ticker, cat, len(tdata[cat])
                        )

            # adjust data ?
            _pAdjust = self.params.get("adjust", None)
            if _pAdjust:
                logger.info("adjust: %s %s", self.ticker, _pAdjust)
                tdata["ohlcdata"] = adjust(
                    tdata["ohlcdata"], adjustType=getattr(AdjustType, _pAdjust)
                )

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, "")

        else:
            return tdata


@endpoint("quote/{ticker}/holders", domain="https://finance.yahoo.com")
class Holders(VirtualAPIRequest, Yhoo):
    """Holders - class to handle the holders endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker: str) -> None:
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

    def _conversion_hook(self, s: str) -> dict:
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            {
               "major": [ .. ],
               "institutional": {
                  "legend": { .. },
                  "holders": [ .. ],
               },
               "mutualfund": {
                  "legend": { .. },
                  "holders": [ .. ],
               },
            }
        """

        def normalize(data: dict, K: str) -> dict:
            _record = {}
            _legend = {}
            for k, v in data[K].items():
                _k = k.lower().replace(" ", "_").replace("%", "pch")
                if _k not in _legend:
                    _legend.update({_k: k})
                for i, (kk, vv) in enumerate(v.items()):
                    if i not in _record:
                        _record.update({i: {}})
                    if isinstance(vv, (str,)) and "%" in vv:
                        vv = float(vv.replace("%", ""))
                    _record[i].update({_k: vv})

            return {"legend": _legend, "holders": list(_record.values())}

        _resp = {}

        data = {}
        try:
            _data = pd.read_html(s)
            for i, k in enumerate(["major", "institutional", "mutualfund"]):
                logger.debug("conversion_hook: %s", k)
                try:
                    data.update({k: json.loads(_data[i].to_json())})

                except IndexError as iErr:
                    # not always all are available
                    logger.debug("conversion_hook: %s failed, no data", k)

            _resp.update(
                {
                    "major": [
                        list(l)
                        for l in zip(
                            data["major"]["0"].values(), data["major"]["1"].values()
                        )
                    ]
                }
            )
            for k in ["institutional", "mutualfund"]:
                try:
                    ndd = normalize(data, k)

                except KeyError as err:
                    # allow that error
                    logger.warning(err)

                else:
                    if ndd:
                        _resp.update({k: ndd})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, "")

        else:
            return _resp


@endpoint(
    "v7/finance/options/{ticker}",
    domain="https://query1.finance.yahoo.com",
    response_type="json",
)
class Options(VirtualAPIRequest, Yhoo):
    """Options - class to handle the options endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker: str, params: dict = None) -> None:
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
        self.params = params

    def _conversion_hook(self, s: str) -> dict:

        resp = {}
        try:
            data = json.loads(s)
            for attr in [
                "underlyingSymbol",
                "expirationDates",
                "strikes",
                "hasMiniOptions",
                "options",
            ]:
                resp.update({attr: data["optionChain"]["result"][0][attr]})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, "")

        else:
            logger.info("conversion_hook: %s OK", self.ticker)
            return resp


@endpoint("quote/{ticker}", domain="https://finance.yahoo.com")
class Profile(VirtualAPIRequest, Yhoo):
    """Profile - class to handle the profile endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker: str) -> None:
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

    def _conversion_hook(self, s: str) -> dict:
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            {
               'profile': {
                   'recommendations': {},
                   'calendar': {},
                   'info': {},
               }
            }

        """
        resp = {}

        def info(response: dict) -> dict:
            rv = {}
            SECTIONS = [
                "summaryProfile",
                "summaryDetail",
                "quoteType",
                "defaultKeyStatistics",
                "assetProfile",
                "summaryDetail",
            ]
            for section in SECTIONS:
                if section in response:
                    rv.update(response[section])

            rv["regularMarketPrice"] = rv["regularMarketOpen"]
            rv["logo_url"] = ""
            domain = extract_domain(rv["website"])
            if domain:
                rv["logo_url"] = f"https://logo.clearbit.com/{domain}"

            return rv

        def recommendations(response: dict) -> dict:
            return response["upgradeDowngradeHistory"]["history"]

        def calendar(response: dict) -> dict:
            return response["calendarEvents"]

        def sustainability(response: dict) -> dict:
            return response["esgScores"]

        try:
            data = response2json(s)

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, "")

        else:
            logger.info("conversion_hook: %s OK", self.ticker)

        try:
            resp.update({"info": info(data)})
            resp.update({"recommendations": recommendations(data)})
            resp.update({"calendar": calendar(data)})
            resp.update({"sustainability": sustainability(data)})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(404, "Profile not found")

        return resp
