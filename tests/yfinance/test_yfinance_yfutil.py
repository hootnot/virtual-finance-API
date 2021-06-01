# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
import virtual_finance_api.compat.yfinance.endpoints.util as yp
import virtual_finance_api.endpoints.yahoo.types as types
from ..unittestsetup import API_URL, client


@pytest.mark.parametrize(
    "params,expected",
    [
        ({"period": "3mo"}, {"period": types.Period.p_3mo}),
        ({"period": "max"}, {"period": types.Period.p_max}),
        ({"start": "2000-01-01"}, {"start": "2000-01-01"}),
        ({"end": "2000-01-01"}, {"end": "2000-01-01"}),
        ({"end": datetime(2000, 1, 1)}, {"end": datetime(2000, 1, 1)}),
        ({"auto_adjust": True}, {"adjust": types.AdjustType.auto}),
        (
            {"auto_adjust": False, "back_adjust": True},
            {"adjust": types.AdjustType.back},
        ),
    ],
)
def test_yfprocopt_options(params, expected):
    res = yp.yfprocopt(**params)
    F = True
    for k, v in expected.items():
        F = F and v == res[k]

    assert F is True
