# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

import virtual_finance_api.endpoints.yahoo.util as yu
import virtual_finance_api.endpoints.yahoo.types as types


@pytest.mark.parametrize(
    "params,expected",
    [
        ({"period": types.Period.p_3mo}, {"range": "3mo"}),
        ({"period": types.Period.p_max}, {"period1": -2208988800}),
        ({"start": "2000-01-01"}, {"period1": 946684800}),
        ({"end": "2000-01-01"}, {"period2": 946684800}),
        ({"end": datetime(2000, 1, 1)}, {"period2": 946684800}),
        (
            {"start": "2000-01-01", "adjust": types.AdjustType.auto},
            {"period1": 946684800, "adjust": types.AdjustType.auto},
        ),
        (
            {"start": "2000-01-01", "adjust": types.AdjustType.back},
            {"period1": 946684800, "adjust": types.AdjustType.back},
        ),
        (
            {"start": "2000-01-01", "prepost": True},
            {"period1": 946684800, "prepost": True},
        ),
    ],
)
def test_procopt_options(params, expected):
    res = yu.procopt(**params)
    F = True
    for k, v in expected.items():
        F = F and v == res[k]

    assert F is True
