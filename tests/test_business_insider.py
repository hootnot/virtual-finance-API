import unittest
# from .unittestsetup import environment as environment
from .unittestsetup import fetchTestData, fetchRawData
import requests_mock


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
from virtual_finance_api.endpoints.business_insider.isin import responses
import virtual_finance_api.endpoints.business_insider as bi

client = None
API_URL = 'https://test.com'


class TestBusinessInsider(unittest.TestCase):
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
        ('_get_isin', None, None, None, None),
        ('_get_isin', VirtualFinanceAPIError, None, lambda q: q[10000:40000], (404,)),  # noqa E501
        ('_get_isin', VirtualFinanceAPIError, None, lambda q: "IBM|", (422,)),
    ])
    @requests_mock.Mocker(kw='mock')
    def test__isin001(self, tid, raises, inParams, func, exceptionParams, **kwargs):  # noqa E501
        tid = "_get_isin"
        resp, data, params = fetchTestData(responses, tid)
        if inParams is not None:
            params = inParams
        r = bi.ISIN(params=params)
        r.DOMAIN = API_URL
        rawdata = fetchRawData('business_insider_get_isin.raw')
        if func:
            rawdata = func(rawdata)
        kwargs['mock'].register_uri('GET',
                                    "{}/{}".format(API_URL, r),
                                    text=rawdata)
        if raises is not None:
            with self.assertRaises(raises) as cErr:
                client.request(r)
                if exceptionParams and exceptionParams[0]:
                    self.assertTrue(exceptionParams[0] == cErr.exception.code)
                elif exceptionParams and exceptionParams[1]:
                    self.assertTrue(exceptionParams[1] in str(cErr.exception))

        else:
            result = client.request(r)
            self.assertTrue(result == resp)

    def test__isin004(self):
        """get the ISIN, make instantiation fail"""
        cErr = None
        with self.assertRaises(ValueError) as cErr:
            bi.ISIN(params={})
        self.assertTrue("Missing in 'params': 'query'" in str(cErr.exception))
