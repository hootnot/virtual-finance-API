# -*- coding: utf-8 -*-

import pytest

# from .unittestsetup import environment as environment
from ..unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
from ..unittestsetup import API_URL, client
import requests_mock

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.yahoo.ticker_bundle import responses
import virtual_finance_api.endpoints.yahoo as yh
from virtual_finance_api.endpoints.decorators import endpoint

TEST_ENDPOINT = "my/{ticker}/test"


@endpoint(TEST_ENDPOINT)
class MyYhoo(yh.ticker_bundle.Yhoo):
    def __init__(self, ticker):
        super(MyYhoo, self).__init__(ticker)


def test__MyYhoo():
    """derived Yhoo request."""
    ticker = "IBM"
    r = MyYhoo(ticker)
    assert str(r) == TEST_ENDPOINT.format(ticker=ticker) and r.ticker == ticker


@pytest.mark.parametrize(
    "cls,ticker,tid,useFullResponse,rawFile",
    [
        (yh.Holders, "IBM", "_yh_holders", True, "yahoo_holders.raw"),
        (yh.Profile, "IBM", "_yh_profile", True, "yahoo_profile.raw"),
        (yh.Financials, "IBM", "_yh_financials", True, "yahoo_financials.raw"),
        (yh.Options, "IBM", "_yh_options", True, "yahoo_options.raw"),
    ],
)
def test__requests(
    requests_mock, client, cls, ticker, tid, useFullResponse, rawFile, **kwargs
):  # noqa E501
    resp, data = fetchTestData(responses, tid)
    if useFullResponse:
        # refactor:
        tid = tid.replace("_yh", "_je")
        resp = fetchFullResponse(tid)
    r = cls(ticker)
    r.DOMAIN = API_URL
    rawdata = fetchRawData(rawFile)
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    assert r.response == resp


@pytest.mark.parametrize(
    "cls,ticker,tid,useFullResponse,rawFile",
    [
        (yh.Holders, "IBM", "_yh_holders", True, "yahoo_holders.raw"),
        (yh.Profile, "IBM", "_yh_profile", True, "yahoo_profile.raw"),
        (yh.Financials, "IBM", "_yh_financials", True, "yahoo_financials.raw"),
    ],
)
def test__excep(
    requests_mock, client, cls, ticker, tid, useFullResponse, rawFile, **kwargs
):  # noqa E501
    r = cls(ticker)
    r.DOMAIN = API_URL
    rawdata = ""  # fetchRawData(rawFile)
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    with pytest.raises(VirtualFinanceAPIError) as cErr:
        client.request(r)
    assert 422 == cErr.value.code
