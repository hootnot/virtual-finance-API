# -*- coding: utf-8 -*-
import pytest

# from .unittestsetup import environment as environment
from ..unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
from ..unittestsetup import API_URL, client
import requests_mock
import json
import logging
import pandas as pd
import numpy as np


from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)

from virtual_finance_api.compat.yfinance.endpoints.bundle import responses
import virtual_finance_api.endpoints.business_insider as bi
import virtual_finance_api.compat.yfinance as yf


def test__Ticker_init():
    """Ticker instance init."""
    # raw data IN, dict (JSON) out
    ticker = yf.Ticker("IBM")
    assert ticker._r["profile"] is None


def test__Ticker_isin(requests_mock):
    """Ticker instance isin."""
    # setup a mock for the ISIN request in a way that it can be called
    # from the Ticker instance
    tid = "_get_isin"
    resp, data, params = fetchTestData(bi.responses.isin.responses, tid)
    # now hack the class, not the instance!
    setattr(bi.ISIN, "DOMAIN", API_URL)
    r = bi.ISIN(params={"query": "IBM"})
    rawdata = fetchRawData("business_insider_get_isin.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    ticker = yf.Ticker("IBM")
    assert ticker.isin == resp


def test__Ticker_history(requests_mock):
    """Ticker instance history."""
    COLUMNS = ["Open", "High", "Low", "Close", "Volume"]
    tid = "_yf_history_IBM"
    resp, data, params = fetchTestData(yf.endpoints.responses.bundle.responses, tid)
    # params = {'period': 'max', 'auto_adjust': True, 'back_adjust': False}
    params = {
        "period": "max",
        "auto_adjust": False,
        "back_adjust": True,
        "actions": True,
    }
    tid = "_je_history_backadjust"
    resp = fetchFullResponse(tid)
    # now hack the class, not the instance!
    setattr(yf.endpoints.History, "DOMAIN", API_URL)
    r = yf.endpoints.History("IBM", params=params)
    rawdata = fetchRawData("yahoo_history.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)

    ticker = yf.Ticker("IBM")

    respDF = pd.DataFrame(resp["ohlcdata"]).set_index("timestamp")
    respDF.drop(columns=["adjclose"], inplace=True)
    respDF.index = pd.to_datetime(respDF.index, unit="s")
    # rename open->Open etc, fabricate the columns dict
    respDF = respDF.rename(columns=dict(zip([c.lower() for c in COLUMNS], COLUMNS)))
    respDF = respDF[COLUMNS]

    TH = ticker.history(**params)
    TH = TH[COLUMNS]

    assert TH.equals(respDF)

    tid = "_je_history_backadjust"
    resp = fetchFullResponse(tid)
    assert (
        sorted(list(ticker.splits.values))
        == sorted([s["numerator"] / s["denominator"] for s in resp["splits"]])
        and sorted(list(ticker.dividends.values))
        == sorted([d["amount"] for d in resp["dividends"]])
        and ticker.actions.to_json()
        == pd.DataFrame(pd.concat([ticker.dividends, ticker.splits], axis=1))
        .replace(np.NaN, 0.0)
        .to_json()
    )


@pytest.mark.parametrize(
    "tid,cls,attrname,_resp,_fullResp,toJSON,rawFile",
    [
        (
            "_yf_holders_major",
            yf.endpoints.Holders,
            "major_holders",
            yf.endpoints.responses.bundle.responses,
            None,
            (),
            "yahoo_holders.raw",
        ),
        (
            "_yf_holders_institutional",
            yf.endpoints.Holders,
            "institutional_holders",
            yf.endpoints.responses.bundle.responses,
            None,
            (),
            "yahoo_holders.raw",
        ),
        (
            "_yf_holders_mutualfund",
            yf.endpoints.Holders,
            "mutualfund_holders",
            yf.endpoints.responses.bundle.responses,
            None,
            (),
            "yahoo_holders.raw",
        ),
        (
            "_yf_profile_info",
            yf.endpoints.Profile,
            "info",
            yf.endpoints.responses.bundle.responses,
            None,
            None,
            "yahoo_profile.raw",
        ),
        (
            "_yf_profile_sustainability",
            yf.endpoints.Profile,
            "sustainability",
            yf.endpoints.responses.bundle.responses,
            None,
            (),
            "yahoo_profile.raw",
        ),
        (
            "_yf_profile_recommendations",
            yf.endpoints.Profile,
            "recommendations",
            yf.endpoints.responses.bundle.responses,
            "_yf_profile_recommendations",
            (),
            "yahoo_profile.raw",
        ),
        (
            "_yf_profile_calendar",
            yf.endpoints.Profile,
            "calendar",
            yf.endpoints.responses.bundle.responses,
            None,
            (),
            "yahoo_profile.raw",
        ),
        (
            "_yf_options_options",
            yf.endpoints.Options,
            "options",
            yf.endpoints.responses.bundle.responses,
            "_yf_options_options",
            None,
            "yahoo_options.raw",
        ),
        (
            "_yf_financials_balancesheet",
            yf.endpoints.Financials,
            "balancesheet",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_balancesheet",
            ("yearly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_balancesheet",
            yf.endpoints.Financials,
            "balance_sheet",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_balancesheet",
            ("yearly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_balancesheet",
            yf.endpoints.Financials,
            "quarterly_balancesheet",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_balancesheet",
            ("quarterly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_balancesheet",
            yf.endpoints.Financials,
            "quarterly_balance_sheet",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_balancesheet",
            ("quarterly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_cashflow",
            yf.endpoints.Financials,
            "cashflow",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_cashflow",
            ("yearly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_cashflow",
            yf.endpoints.Financials,
            "quarterly_cashflow",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_cashflow",
            ("quarterly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_earnings",
            yf.endpoints.Financials,
            "earnings",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_earnings",
            ("yearly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_earnings",
            yf.endpoints.Financials,
            "quarterly_earnings",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_earnings",
            ("quarterly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_financials",
            yf.endpoints.Financials,
            "financials",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_financials",
            ("yearly",),
            "yahoo_financials.raw",
        ),
        (
            "_yf_financials_financials",
            yf.endpoints.Financials,
            "quarterly_financials",
            yf.endpoints.responses.bundle.responses,
            "_yf_financials_financials",
            ("quarterly",),
            "yahoo_financials.raw",
        ),
    ],
)
def test__Ticker_attrs(
    requests_mock, tid, cls, attrname, _resp, _fullResp, toJSON, rawFile, **kwargs
):
    """Ticker instance."""
    # toJSON must have a value
    #   - None or,
    #   - () or,
    #   - ('<indexname>')
    # components = ['yearly', 'quarterly'] if cls is yf.endpoints.Financials else []
    # tid = "_yf_profile_info"
    resp, data, params = None, None, None
    try:
        resp, data, params = fetchTestData(_resp, tid)

    except Exception as err:  # noqa F841
        resp, data = fetchTestData(_resp, tid)

    try:
        dresp = fetchFullResponse(tid)

    except Exception as err:  # noqa F841
        pass

    else:
        resp = dresp
    setattr(cls, "DOMAIN", API_URL)
    r = cls("IBM")
    rawdata = fetchRawData(rawFile)
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    ticker = yf.Ticker("IBM")
    instancedata = (
        getattr(ticker, attrname)
        if isinstance(attrname, str)
        else getattr(ticker, attrname[0])(attrname[1])
    )
    if isinstance(instancedata, tuple):
        instancedata = list(instancedata)
    if toJSON is not None:
        instancedata = json.loads(instancedata.to_json())
        if len(toJSON):
            _tframe = toJSON[0]
            resp = resp[_tframe]

    #        print("+++++++++++++++++++++++++++++++++++++++++\n", instancedata)
    #        print("=========================================\n", resp)
    assert instancedata == resp


# class TestCompatYfinance(unittest.TestCase):
#    """Tests regarding the business_insider endpoints."""
#
#            logging.basicConfig(
#                filename="/tmp/TST.log",
#                level=logging.INFO,
#                format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
#            )
#
#    @parameterized.expand(
#        [
#        ],
#        skip_on_empty=True,
#    )
