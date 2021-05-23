# -*- coding: utf-8 -*-

import pytest

# from .unittestsetup import environment as environment
from ..unittestsetup import fetchTestData, fetchRawData
from ..unittestsetup import API_URL, client
import requests_mock


from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.yahoo.screener_bundle import responses
import virtual_finance_api.endpoints.yahoo as yhe


def test__predefined_screener001(requests_mock, client):
    """get the screener output."""
    tid = "_screener"
    resp, data = fetchTestData(responses, tid)
    r = yhe.Screener("MOST_SHORTED_STOCKS")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("screener.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    result = client.request(r)
    assert str(result) == str(resp)


def test__predefined_screener002(requests_mock, client):
    """get the screener output."""
    tid = "_screener"
    resp, data = fetchTestData(responses, tid)
    r = yhe.Screener("MOST_SHORTED_STOCKS")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("screener.raw")

    requests_mock.register_uri(
        "GET", "{}/{}".format(API_URL, r), text=rawdata.replace("store", "erots")
    )
    with pytest.raises(VirtualFinanceAPIError) as cErr:
        client.request(r)
    assert 422 == cErr.value.code


def test__predefined_screeners001(requests_mock, client):
    """get the screeners output 001."""
    # raw data IN, dict (JSON) out
    tid = "_screeners"
    resp, data = fetchTestData(responses, tid)
    r = yhe.Screeners()
    r.DOMAIN = API_URL
    rawdata = fetchRawData("screeners.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    result = None
    result = client.request(r)
    assert result == resp


def test__predefined_screeners002(requests_mock, client):
    """get the screeners output."""
    # raw data IN, dict (JSON) out
    tid = "_screeners"
    resp, data = fetchTestData(responses, tid)
    r = yhe.Screeners()
    r.DOMAIN = API_URL
    rawdata = fetchRawData("screeners.raw")
    requests_mock.register_uri(
        "GET", "{}/{}".format(API_URL, r), text=rawdata.replace("Store", "WTF")
    )
    cErr = None
    with pytest.raises(VirtualFinanceAPIError) as cErr:
        client.request(r)
    assert 422 == cErr.value.code
