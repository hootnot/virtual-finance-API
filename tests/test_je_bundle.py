import unittest
# from .unittestsetup import environment as environment
from .unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
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
from virtual_finance_api.extensions.stdjson.endpoints.bundle import responses
import virtual_finance_api.extensions.stdjson.endpoints as je
import json

client = None
API_URL = 'https://test.com'
TEST_ENDPOINT = 'my/{ticker}/test'


class TestExtensionsStdJSONBundle(unittest.TestCase):
    """Tests regarding the extensions stdjson endpoints."""

    def setUp(self):
        """setup for all tests."""
        global client
        # self.maxDiff = None
        try:
            client = Client(headers={"Content-Type": "application/json"})
        except Exception as e:
            print("%s" % e)
            exit(0)

    @parameterized.expand([
        (je.Holders, 'IBM', '_je_holders', True, 'yahoo_holders.raw'),
        (je.Profile, 'IBM', '_je_profile', True, 'yahoo_profile.raw'),
        (je.Financials, 'IBM', '_je_financials', True, 'yahoo_financials.raw'),
        (je.Options, 'IBM', '_je_options', True, 'yahoo_options.raw'),
        (je.History, 'IBM', '_je_history', True, 'yahoo_history.raw'),
        (je.History, 'IBM', ('_je_history', '_backadjust'), True, 'yahoo_history.raw', {'back_adjust': True, 'auto_adjust': False})
    ])
    @requests_mock.Mocker(kw='mock')
    def test__requests(self, cls, ticker, _tid, useFullResponse, rawFile, mrg=None, **kwargs):  # noqa E501
        tid = _tid
        subtid = None
        if isinstance(_tid, (tuple,)):
            tid = _tid[0]
            subtid = _tid[1]

        try:
            # try to get with params first
            resp, data, params = fetchTestData(responses, tid)
            if mrg:
                for k, v in mrg.items():
                    params.update({k: v})
                # print("******* PARAMS *********", params)

        except ValueError as err:  # noqa F841
            # ... else get without params
            resp, data = fetchTestData(responses, tid)

        if useFullResponse:
            respID = tid if subtid is None else (tid + subtid)
            resp = fetchFullResponse(respID)

        r = cls(ticker) if cls is not je.History else cls(ticker, params=params)  # noqa E501

        r.DOMAIN = API_URL
        rawdata = fetchRawData(rawFile)
        kwargs['mock'].register_uri('GET',
                                    "{}/{}".format(API_URL, r),
                                    text=rawdata)
        client.request(r)
        with open(f"/tmp/DB_{tid}.json", "w") as OUT:
            OUT.write(json.dumps(r.response, indent=2))
        self.assertTrue(r.response == resp)

    @parameterized.expand([
        (je.Holders, 'IBM', '_je_holders', True, 'yahoo_holders.raw'),
        (je.Profile, 'IBM', '_je_profile', True, 'yahoo_profile.raw'),
        (je.Financials, 'IBM', '_je_financials', True, 'yahoo_financials.raw'),
    ])
    @requests_mock.Mocker(kw='mock')
    def test__excep(self, cls, ticker, tid, useFullResponse, rawFile, **kwargs):  # noqa E501
        """the exception will be raised in the parent class already, so we need to let
        that one pass, but the one in the derived class raise
        """
        r = cls(ticker)
        r.DOMAIN = API_URL
        rawdata = ""   # fetchRawData(rawFile)
        kwargs['mock'].register_uri('GET',
                                    "{}/{}".format(API_URL, r),
                                    text=rawdata)
        with self.assertRaises(VirtualFinanceAPIError) as cErr:
            client.request(r)
        self.assertTrue(422 == cErr.exception.code)
