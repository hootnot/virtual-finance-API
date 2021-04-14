import unittest

# from .unittestsetup import environment as environment
from .unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
import requests_mock
import json


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
from virtual_finance_api.compat.yfinance.endpoints.bundle import responses

# from virtual_finance_api.extensions.stdjson.endpoints.bundle import (
#    responses as je_responses,
# )
import virtual_finance_api.compat.yfinance.endpoints as yfe

# import virtual_finance_api.compat.yfinance as yf

client = None
API_URL = "https://test.com"


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

    @parameterized.expand(
        [
            (
                yfe.Profile,
                "calendar",
                "_yf_profile_calendar",
                "yahoo_profile.raw",
                ["calendar", "upgradeDowngradeHistory", "esgScores"],
            ),
            (
                yfe.Profile,
                "recommendations",
                "_yf_profile_recommendations",
                "yahoo_profile.raw",
                [],
            ),
            (
                yfe.Profile,
                "sustainability",
                "_yf_profile_sustainability",
                "yahoo_profile.raw",
                [],
            ),
            (yfe.Profile, ("info", None), "_yf_profile_info", "yahoo_profile.raw", []),
            (yfe.Holders, "major", "_yf_holders_major", "yahoo_holders.raw", []),
            (
                yfe.Holders,
                "mutualfund",
                "_yf_holders_mutualfund",
                "yahoo_holders.raw",
                [],
            ),
            (
                yfe.Holders,
                "institutional",
                "_yf_holders_institutional",
                "yahoo_holders.raw",
                [],
            ),
        ],
        skip_on_empty=True,
    )
    @requests_mock.Mocker(kw="mock")
    def test__yf_None(self, cls, attr, tid, rawfile, comp, **kwargs):
        import pandas as pd

        resp, data = fetchTestData(responses, tid)
        try:
            _resp = fetchFullResponse(tid)
        except Exception as err:  # noqa F841
            pass
        else:
            resp = _resp
        r = cls("IBM")
        r.DOMAIN = API_URL
        rawdata = fetchRawData(rawfile)
        kwargs["mock"].register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        if isinstance(attr, str):
            self.assertTrue(json.loads(getattr(r, attr).to_json()) == resp)

        else:
            self.assertTrue(getattr(r, attr[0]) == resp)

        F = True
        for C in comp:
            r.response[C] = None
            F = F and getattr(r, attr) is None
        self.assertTrue(F is True)

    @requests_mock.Mocker()
    def test__yf_profile_info002(self, mock_req):
        """Profile-info ."""
        tid = "_yf_profile_info"
        resp, data = fetchTestData(responses, tid)
        r = yfe.Profile("IBM")
        r.DOMAIN = API_URL
        # force an error by corrupting the input data
        rawdata = fetchRawData("yahoo_profile.raw")[100:1000]
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        with self.assertRaises(VirtualFinanceAPIError) as cErr:
            client.request(r)
        self.assertTrue(422, cErr.exception.code)

    # -----------------
    @requests_mock.Mocker()
    def test__yf_holders_004(self, mock_req):
        """Holders-wrong ."""
        # tid = "_yf_holders_institutional"
        # resp, data = fetchTestData(responses, tid)
        # resp = fetchFullResponse(tid)
        r = yfe.Holders("IBM")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("yahoo_holders.raw")
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        with self.assertRaises(KeyError) as cErr:
            client.request(r)
            r.major.to_json()
            del r._holders["major"]
            r.major.to_json()

        # ? print("EXCEP is: ", cErr.exception, "major" == str(cErr.exception))
        self.assertTrue("major" in str(cErr.exception))

    # -----------------
    @parameterized.expand(
        [
            (yfe.Financials, "earnings", "_yf_financials_earnings"),
            (yfe.Financials, "balancesheet", "_yf_financials_balancesheet"),
            (yfe.Financials, "cashflow", "_yf_financials_cashflow"),
            (yfe.Financials, "financials", "_yf_financials_financials"),
        ],
        skip_on_empty=True,
    )
    @requests_mock.Mocker(kw="mock")
    def test__yf_financials(self, cls, attr, tid, **kwargs):
        resp, data = fetchTestData(responses, tid)
        try:
            _resp = fetchFullResponse(tid)
        except Exception as err:  # noqa F841
            pass
        else:
            resp = _resp
        r = cls("IBM")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("yahoo_financials.raw")
        kwargs["mock"].register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        self.assertTrue(
            {
                "yearly": json.loads(getattr(r, attr)["yearly"].to_json()),
                "quarterly": json.loads(getattr(r, attr)["quarterly"].to_json()),
            }
            == resp
        )

    # -----------------
    @requests_mock.Mocker()
    def test__yf_options001(self, mock_req):
        """Options-options ."""
        tid = "_yf_options_options"
        resp, data = fetchTestData(responses, tid)
        resp = fetchFullResponse(tid)
        resp = tuple(resp)
        r = yfe.Options("IBM")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("yahoo_options.raw")
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        self.assertTrue(r.options == resp)

    @requests_mock.Mocker()
    def test__yf_options002(self, mock_req):
        """Options-options ."""
        tid = "_yf_options_optionchain"
        resp, data = fetchTestData(responses, tid)
        resp = fetchFullResponse(tid)
        r = yfe.Options("IBM")
        r.DOMAIN = API_URL
        rawdata = fetchRawData("yahoo_options.raw")
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        self.assertTrue(
            {
                "calls": json.loads(r.option_chain()[0].to_json()),
                "puts": json.loads(r.option_chain()[1].to_json()),
            }
            == resp
        )

    # ------------------------
    # history     V
    # dividends   V
    # splits      V
    # value     ?
    @requests_mock.Mocker()
    def test__yf_history001(self, mock_req):
        """History-history ."""
        tid = "_yf_history_IBM"
        resp, data, params = fetchTestData(responses, tid)

        tid = "_je_history_backadjust"
        resp = fetchFullResponse(tid)
        rawdata = fetchRawData("yahoo_history.raw")
        params = {
            "period": "max",
            "interval": "1d",
            "actions": True,
            "auto_adjust": False,
        }
        r = yfe.History("IBM", params=params)
        r.DOMAIN = API_URL
        mock_req.register_uri("GET", "{}/{}".format(API_URL, r), text=rawdata)
        client.request(r)
        self.assertTrue(
            (r.response["ohlcdata"]["adjclose"] == resp["ohlcdata"]["adjclose"])
            and (r.response["ohlcdata"]["timestamp"] == resp["ohlcdata"]["timestamp"])
            and (r.response["ohlcdata"]["volume"] == resp["ohlcdata"]["volume"])
            and sorted(list(r.dividends.values))
            == sorted([d["amount"] for d in resp["dividends"]])
            and sorted(list(r.splits.values))
            == sorted([s["numerator"] / s["denominator"] for s in resp["splits"]])
        )
