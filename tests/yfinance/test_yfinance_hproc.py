# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
import virtual_finance_api.endpoints.yahoo.util as hp
from ..unittestsetup import API_URL, client


@pytest.mark.parametrize(
    "params,expected",
    [
        ({"period": "3mo"}, {"range": "3mo"}),
        ({"period": "max"}, {"period1": -2208988800}),
        ({"start": "2000-01-01"}, {"period1": 946684800}),
        ({"end": "2000-01-01"}, {"period2": 946684800}),
        ({"end": datetime(2000, 1, 1)}, {"period2": 946684800}),
        (
            {"start": "2000-01-01", "auto_adjust": True},
            {"period1": 946684800, "adjust": "auto"},
        ),
        (
            {"start": "2000-01-01", "auto_adjust": False, "back_adjust": True},
            {"period1": 946684800, "adjust": "backadjust"},
        ),
        (
            {"start": "2000-01-01", "prepost": True},
            {"period1": 946684800, "prepost": True},
        ),
    ],
)
def test_hprocopt_periods(params, expected):
    res = hp.hprocopt(**params)
    F = True
    for k, v in expected.items():
        F = F and v == res[k]

    assert F is True
