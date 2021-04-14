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
    VirtualFinanceAPIError,
)
from virtual_finance_api.endpoints.yahoo.ticker_bundle import responses

# from virtual_finance_api.extensions.stdjson.endpoints.bundle import (
#    responses as je_responses,
# )
import virtual_finance_api.endpoints.yahoo as yh
from virtual_finance_api.endpoints.decorators import endpoint

client = None
API_URL = "https://test.com"
TEST_ENDPOINT = "my/{ticker}/test"


@endpoint(TEST_ENDPOINT)
class MyYhoo(yh.ticker_bundle.Yhoo):
    def __init__(self, ticker):
        super(MyYhoo, self).__init__(ticker)


class TestYahooTickerBundle(unittest.TestCase):
    """Tests regarding the yahoo tickerbundle endpoints."""

    def setUp(self):
        """setup for all tests."""
        global client
        # self.maxDiff = None
        try:
            client = Client(headers={"Content-Type": "application/json"})
        except Exception as e:
            print("%s" % e)
            exit(0)

    def test__MyYhoo(self):
        """derived Yhoo request."""
        ticker = "IBM"
        r = MyYhoo(ticker)
        self.assertTrue(
            str(r) == TEST_ENDPOINT.format(ticker=ticker) and r.ticker == ticker
        )

    @parameterized.expand(
        [
            (yh.Holders, "IBM", "_yh_holders", True, "yahoo_holders.raw"),
            (yh.Profile, "IBM", "_yh_profile", True, "yahoo_profile.raw"),
            (yh.Financials, "IBM", "_yh_financials", True, "yahoo_financials.raw"),
            (yh.Options, "IBM", "_yh_options", True, "yahoo_options.raw"),
        ]
    )
    @requests_mock.Mocker(kw="mock")
    def test__requests(
        self, cls, ticker, tid, useFullResponse, rawFile, **kwargs
    ):  # noqa E501
        resp, data = fetchTestData(responses, tid)
        if useFullResponse:
            # refactor:
            tid = tid.replace("_yh", "_je")
            resp = fetchFullResponse(tid)
        r = cls(ticker)
        r.DOMAIN = API_URL
        rawdata = fetchRawData(rawFile)
        kwargs["mock"].register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        self.assertTrue(r.response == resp)

    @parameterized.expand(
        [
            (yh.Holders, "IBM", "_yh_holders", True, "yahoo_holders.raw"),
            (yh.Profile, "IBM", "_yh_profile", True, "yahoo_profile.raw"),
            (yh.Financials, "IBM", "_yh_financials", True, "yahoo_financials.raw"),
        ],
        skip_on_empty=True,
    )
    @requests_mock.Mocker(kw="mock")
    def test__excep(
        self, cls, ticker, tid, useFullResponse, rawFile, **kwargs
    ):  # noqa E501
        r = cls(ticker)
        r.DOMAIN = API_URL
        rawdata = ""  # fetchRawData(rawFile)
        kwargs["mock"].register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        with self.assertRaises(VirtualFinanceAPIError) as cErr:
            client.request(r)
        self.assertTrue(422, cErr.exception.code)
