import unittest

# from .unittestsetup import environment as environment
from .unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
import requests_mock

# import json


try:
    from parameterized import parameterized  # noqa F401

except Exception as err:  # noqa F841
    print("*** Please install 'parameterized' to run these tests ***")
    exit(0)

from virtual_finance_api.client import Client
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.yahoo.index_bundle import responses
import virtual_finance_api.endpoints.yahoo as yh

client = None
API_URL = "https://test.com"


class TestYahooIndexBundle(unittest.TestCase):
    """Tests regarding the yahoo indexbundle endpoints."""

    def setUp(self):
        """setup for all tests."""
        global client
        # self.maxDiff = None
        try:
            client = Client(headers={"Content-Type": "application/json"})
        except Exception as e:
            print("%s" % e)
            exit(0)

    @requests_mock.Mocker()
    def test__yhoo_index001(self, mock_req):
        """yahoo index ."""
        tid = "_endpoints_yh_yahooindex"
        resp, data = fetchTestData(responses, tid)
        resp = fetchFullResponse(tid)
        r = yh.YhooIndex("%5EIXIC")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("yahoo_index.raw")
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        self.assertTrue(r.response == resp)

    @requests_mock.Mocker()
    def test__yhoo_index002(self, mock_req):
        """yahoo index ."""
        tid = "_endpoints_yh_yahooindex"
        resp, data = fetchTestData(responses, tid)
        r = yh.YhooIndex("%5EIXIC")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("yahoo_index.raw")[10000:50000]
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        with self.assertRaises(VirtualFinanceAPIError) as cErr:
            client.request(r)
        self.assertTrue(422, cErr.exception.code)
