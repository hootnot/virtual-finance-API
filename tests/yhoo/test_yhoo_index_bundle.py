# -*- coding: utf-8 -*-

import pytest

# from .unittestsetup import environment as environment
from ..unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
from ..unittestsetup import API_URL, client
import requests_mock

# import json

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.yahoo.index_bundle import responses
import virtual_finance_api.endpoints.yahoo as yh


def test__yhoo_index001(requests_mock, client):
    """yahoo index ."""
    tid = "_yh_yahooindex"
    resp, data = fetchTestData(responses, tid)
    resp = fetchFullResponse(tid)
    r = yh.YhooIndex("%5EIXIC")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("yahoo_index.raw")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    client.request(r)
    assert r.response == resp


def test__yhoo_index002(requests_mock, client):
    """yahoo index ."""
    tid = "_yh_yahooindex"
    resp, data = fetchTestData(responses, tid)
    r = yh.YhooIndex("%5EIXIC")
    r.DOMAIN = API_URL
    rawdata = fetchRawData("yahoo_index.raw")[10000:50000]
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    with pytest.raises(VirtualFinanceAPIError) as cErr:
        client.request(r)
    assert 422 == cErr.value.code
