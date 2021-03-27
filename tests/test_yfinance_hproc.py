import unittest
from datetime import datetime
# from .unittestsetup import environment as environment
# from .unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
# import requests_mock
# import json


try:
    from parameterized import parameterized  # noqa F401

except Exception as err:  # noqa F841
    print("*** Please install 'parameterized' to run these tests ***")
    exit(0)

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError
)
import virtual_finance_api.compat.yfinance.endpoints.bundle as hp

client = None
API_URL = 'https://test.com'


class TestCompatYfinance(unittest.TestCase):
    """Tests regarding the business_insider endpoints."""

    def setUp(self):
        """setup for all tests."""
        global client
        # self.maxDiff = None
        try:
            client = Client(headers={"Content-Type": "application/json"})
            # api.api_url = 'https://test.com'
        except Exception as e:
            print("%s" % e)
            exit(0)

    @parameterized.expand([
        ({"period": "3mo"},
         {"range": "3mo"}),
        ({"period": "max"},
         {"period1": -2208988800}),
        ({"start": "2000-01-01"},
         {"period1": 946684800}),
        ({"end": "2000-01-01"},
         {"period2": 946684800}),
        ({"end": datetime(2000, 1, 1)},
         {"period2": 946684800}),
        ({"start": "2000-01-01", "auto_adjust": True},
         {"period1": 946684800, "adjust": "auto"}),
        ({"start": "2000-01-01", "auto_adjust": False, "back_adjust": True},
         {"period1": 946684800, "adjust": "backadjust"}),
        ({"start": "2000-01-01", "prepost": True},
         {"period1": 946684800, "prepost": True}),
    ])
    def test_hprocopt_periods(self, params, expected):
        res = hp.hprocopt(**params)
        F = True
        for k, v in expected.items():
            F = (F and v == res[k])

        self.assertTrue(F)
