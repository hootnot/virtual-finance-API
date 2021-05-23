# -*- coding: utf-8 -*-

import pytest
from ..unittestsetup import fetchTestData, fetchRawData
from ..unittestsetup import API_URL, client

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.business_insider.isin import responses
import virtual_finance_api.endpoints.business_insider as bi


@pytest.mark.parametrize(
    "tid, raises, inParams, func, exceptionParams",
    [
        ("_get_isin", None, None, None, None),
        ("_get_isin", VirtualFinanceAPIError, None, lambda q: q[10000:40000], (404,)),
        ("_get_isin", VirtualFinanceAPIError, None, lambda q: "IBM|", (422,)),
    ],
)
def test_isin001(requests_mock, client, tid, raises, inParams, func, exceptionParams):
    tid = "_get_isin"
    resp, data, params = fetchTestData(responses, tid)
    if inParams is not None:
        params = inParams
    r = bi.ISIN(params=params)
    r.DOMAIN = API_URL
    rawdata = fetchRawData("business_insider_get_isin.raw")
    if func:
        rawdata = func(rawdata)
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
    if raises is not None:
        with pytest.raises(raises) as cErr:
            client.request(r)
            if exceptionParams and exceptionParams[0]:
                assert exceptionParams[0] == cErr.value.code
            elif exceptionParams and exceptionParams[1]:
                assert exceptionParams[1] in str(cErr.value)

    else:
        result = client.request(r)
        assert result == resp


def test__isin002():
    """get the ISIN, make instantiation fail"""
    cErr = None
    with pytest.raises(ValueError) as cErr:
        bi.ISIN(params={})
    assert "Missing in 'params': 'query'" in str(cErr.value)
