# -*- coding: utf-8 -*-

import pytest

# from .unittestsetup import environment as environment
from ..unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
from ..unittestsetup import API_URL, client
import requests_mock
import json


from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
from virtual_finance_api.compat.yfinance.endpoints.bundle import responses
import virtual_finance_api.compat.yfinance.endpoints as yfe


#    # ------------------------
#    # history     V
#    # dividends   V
#    # splits      V
#    # value     ?
def test__yf_history001(requests_mock):
    """History-history ."""
    tid = "_yf_history_IBM"
    client = Client()
    resp, data, params = fetchTestData(responses, tid)

    tid = "_je_history_backadjust"
    resp = fetchFullResponse(tid)
    rawdata = fetchRawData("yahoo_history.raw")
    params = {"period": "max", "interval": "1d", "actions": True, "auto_adjust": False}
    r = yfe.History("IBM", params=params)
    r.DOMAIN = API_URL
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    assert (
        (r.response["ohlcdata"]["adjclose"] == resp["ohlcdata"]["adjclose"])
        and (r.response["ohlcdata"]["timestamp"] == resp["ohlcdata"]["timestamp"])
        and (r.response["ohlcdata"]["volume"] == resp["ohlcdata"]["volume"])
        and sorted(list(r.dividends.values))
        == sorted([d["amount"] for d in resp["dividends"]])
        and sorted(list(r.splits.values))
        == sorted([s["numerator"] / s["denominator"] for s in resp["splits"]])
    )


@pytest.mark.parametrize(
    "cls,attr,tid,rawfile,comp",
    [
        (
            yfe.Profile,
            "calendar",
            "_yf_profile_calendar",
            "yahoo_profile.raw",
            ["calendar", "upgradeDowngradeHistory", "esgScores"],
        ),
        (
            yfe.Profile,
            "recommendations",
            "_yf_profile_recommendations",
            "yahoo_profile.raw",
            [],
        ),
        (
            yfe.Profile,
            "sustainability",
            "_yf_profile_sustainability",
            "yahoo_profile.raw",
            [],
        ),
        (yfe.Profile, ("info", None), "_yf_profile_info", "yahoo_profile.raw", []),
        (yfe.Holders, "major", "_yf_holders_major", "yahoo_holders.raw", []),
        (yfe.Holders, "mutualfund", "_yf_holders_mutualfund", "yahoo_holders.raw", []),
        (
            yfe.Holders,
            "institutional",
            "_yf_holders_institutional",
            "yahoo_holders.raw",
            [],
        ),
    ],
)
def test__yf_None(requests_mock, client, cls, attr, tid, rawfile, comp, **kwargs):
    import pandas as pd

    resp, data = fetchTestData(responses, tid)
    try:
        _resp = fetchFullResponse(tid)
    except Exception as err:  # noqa F841
        pass
    else:
        resp = _resp
    r = cls("IBM")
    r.DOMAIN = API_URL
    rawdata = fetchRawData(rawfile)
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    if isinstance(attr, str):
        assert json.loads(getattr(r, attr).to_json()) == resp

    else:
        assert getattr(r, attr[0]) == resp

    F = True
    for C in comp:
        r.response[C] = None
        F = F and getattr(r, attr) is None

    assert F is True


def test__yf_profile_info002(requests_mock, client):
    """Profile-info ."""
    tid = "_yf_profile_info"
    resp, data = fetchTestData(responses, tid)
    r = yfe.Profile("IBM")
    r.DOMAIN = API_URL
    # force an error by corrupting the input data
    rawdata = fetchRawData("yahoo_profile.raw")[100:1000]
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    with pytest.raises(VirtualFinanceAPIError) as cErr:
        client.request(r)
    assert 422 == cErr.value.code


def test__yf_holders_004(requests_mock, client):
    """Holders-wrong ."""
    # tid = "_yf_holders_institutional"
    # resp, data = fetchTestData(responses, tid)
    # resp = fetchFullResponse(tid)
    r = yfe.Holders("IBM")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("yahoo_holders.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    with pytest.raises(KeyError) as cErr:
        client.request(r)
        r.major.to_json()
        del r._holders["major"]
        r.major.to_json()

    assert "major" in str(cErr.value)


@pytest.mark.parametrize(
    "cls,attr,tid",
    [
        (yfe.Financials, "earnings", "_yf_financials_earnings"),
        (yfe.Financials, "balancesheet", "_yf_financials_balancesheet"),
        (yfe.Financials, "cashflow", "_yf_financials_cashflow"),
        (yfe.Financials, "financials", "_yf_financials_financials"),
    ],
)
def test__yf_financials(requests_mock, client, cls, attr, tid, **kwargs):
    resp, data = fetchTestData(responses, tid)
    try:
        _resp = fetchFullResponse(tid)

    except Exception as err:  # noqa F841
        pass

    else:
        resp = _resp

    r = cls("IBM")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("yahoo_financials.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    assert {
        "yearly": json.loads(getattr(r, attr)["yearly"].to_json()),
        "quarterly": json.loads(getattr(r, attr)["quarterly"].to_json()),
    } == resp


def test__yf_options001(requests_mock, client):
    """Options-options ."""
    tid = "_yf_options_options"
    resp, data = fetchTestData(responses, tid)
    resp = fetchFullResponse(tid)
    resp = tuple(resp)
    r = yfe.Options("IBM")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("yahoo_options.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    assert r.options == resp


def test__yf_options002(requests_mock, client):
    """Options-options ."""
    tid = "_yf_options_optionchain"
    resp, data = fetchTestData(responses, tid)
    resp = fetchFullResponse(tid)
    r = yfe.Options("IBM")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("yahoo_options.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    assert {
        "calls": json.loads(r.option_chain()[0].to_json()),
        "puts": json.loads(r.option_chain()[1].to_json()),
    } == resp
