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
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.yahoo.screener_bundle import responses
import virtual_finance_api.endpoints.yahoo as yhe

client = None
API_URL = "https://test.com"


class TestScreener_bundle(unittest.TestCase):
    """Tests regarding the accounts endpoints."""

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

    @requests_mock.Mocker()
    def test__predefined_screener001(self, mock_req):
        """get the screener output."""
        tid = "_predefined_screener"
        resp, data = fetchTestData(responses, tid)
        r = yhe.Screener("MOST_SHORTED_STOCKS")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("screener.raw")
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        result = client.request(r)
        self.assertTrue(str(result) == str(resp))

    @requests_mock.Mocker()
    def test__predefined_screener002(self, mock_req):
        """get the screener output."""
        tid = "_predefined_screener"
        resp, data = fetchTestData(responses, tid)
        r = yhe.Screener("MOST_SHORTED_STOCKS")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("screener.raw")

        mock_req.register_uri(
            "GET", "{}/{}".format(API_URL, r), text=rawdata.replace("store", "erots")
        )
        with self.assertRaises(VirtualFinanceAPIError) as cErr:
            client.request(r)
        self.assertTrue(422, cErr.exception.code)

    @requests_mock.Mocker()
    def test__predefined_screeners001(self, mock_req):
        """get the screeners output 001."""
        # raw data IN, dict (JSON) out
        tid = "_predefined_screeners"
        resp, data = fetchTestData(responses, tid)
        r = yhe.Screeners()
        r.DOMAIN = API_URL
        rawdata = fetchRawData("screeners.raw")
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        result = None
        result = client.request(r)
        self.assertTrue(result == resp)

    @requests_mock.Mocker()
    def test__predefined_screeners002(self, mock_req):
        """get the screeners output."""
        # raw data IN, dict (JSON) out
        tid = "_predefined_screeners"
        resp, data = fetchTestData(responses, tid)
        r = yhe.Screeners()
        r.DOMAIN = API_URL
        rawdata = fetchRawData("screeners.raw")
        mock_req.register_uri(
            "GET", "{}/{}".format(API_URL, r), text=rawdata.replace("Store", "WTF")
        )
        cErr = None
        with self.assertRaises(VirtualFinanceAPIError) as cErr:
            client.request(r)
        self.assertTrue(422, cErr.exception.code)
