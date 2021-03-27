import unittest
# from .unittestsetup import environment as environment
from .unittestsetup import fetchTestData, fetchRawData, fetchFullResponse
import requests_mock
import json
import logging


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
# from virtual_finance_api.compat.yfinance.ticker import responses
from virtual_finance_api.compat.yfinance.endpoints.bundle import responses
import virtual_finance_api.endpoints.business_insider as bi
import virtual_finance_api.compat.yfinance as yf

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

            logging.basicConfig(
                filename="/tmp/TST.log",
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
            )

        except Exception as e:
            print("%s" % e)
            exit(0)

    @requests_mock.Mocker()
    def test__Ticker_init(self, mock_req):
        """Ticker instance init."""
        # raw data IN, dict (JSON) out
        ticker = yf.Ticker('IBM')
        self.assertTrue(ticker._r['profile'] is None)

    @requests_mock.Mocker()
    def test__Ticker_isin(self, mock_req):
        """Ticker instance isin."""
        tid = "_get_isin"
        resp, data, params = fetchTestData(bi.responses.isin.responses, tid)
        setattr(bi.ISIN, 'DOMAIN', API_URL)
        r = bi.ISIN(params={'query': 'IBM'})
        rawdata = fetchRawData('business_insider_get_isin.raw')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=rawdata)
        ticker = yf.Ticker('IBM')
        self.assertTrue(ticker.isin == {'ticker': 'IBM',
                                        'ISIN': 'US4592001014'})

    @parameterized.expand([
        ('_yf_holders_major', yf.endpoints.Holders, 'major_holders', yf.endpoints.responses.bundle.responses, None, 'to_json', 'yahoo_holders.raw'),
        ('_yf_holders_institutional', yf.endpoints.Holders, 'institutional_holders', yf.endpoints.responses.bundle.responses, None, 'to_json', 'yahoo_holders.raw'),
        ('_yf_holders_mutualfund', yf.endpoints.Holders, 'mutualfund_holders', yf.endpoints.responses.bundle.responses, None, 'to_json', 'yahoo_holders.raw'),
        ('_yf_profile_info', yf.endpoints.Profile, 'info', yf.endpoints.responses.bundle.responses, None, None, 'yahoo_profile.raw'),
        ('_yf_profile_sustainability', yf.endpoints.Profile, 'sustainability', yf.endpoints.responses.bundle.responses, None, 'to_json', 'yahoo_profile.raw'),
        ('_yf_profile_recommendations', yf.endpoints.Profile, 'recommendations', yf.endpoints.responses.bundle.responses, '_yf_profile_recommendations', 'to_json', 'yahoo_profile.raw'),
        ('_yf_profile_calendar', yf.endpoints.Profile, 'calendar', yf.endpoints.responses.bundle.responses, None, 'to_json', 'yahoo_profile.raw'),
        ('_yf_options_options', yf.endpoints.Options, 'options', yf.endpoints.responses.bundle.responses, '_yf_options_options', None, 'yahoo_options.raw'),
        ])
    @requests_mock.Mocker(kw='mock')
    def test__Ticker_attrs(self, tid, cls, attrname, _resp, _fullResp, toJSON, rawFile, **kwargs):
        """Ticker instance profile-info."""
        # components = ['yearly', 'quarterly'] if cls is yf.endpoints.Financials else []
        # tid = "_yf_profile_info"
        resp, data, params = None, None, None
        try:
            resp, data, params = fetchTestData(_resp, tid)
        except Exception as err:  # noqa F841
            resp, data = fetchTestData(_resp, tid)

        try:
            dresp = fetchFullResponse(tid)
        except Exception as err:  # noqa F841
            pass
        else:
            resp = dresp
        setattr(cls, 'DOMAIN', API_URL)
        r = cls('IBM')
        rawdata = fetchRawData(rawFile)
        kwargs['mock'].register_uri('GET',
                                    "{}/{}".format(API_URL, r),
                                    text=rawdata)
        ticker = yf.Ticker('IBM')
        instancedata = getattr(ticker, attrname) if isinstance(attrname, str) else getattr(ticker, attrname[0])(attrname[1])
        if isinstance(instancedata, tuple):
            instancedata = list(instancedata)
        if toJSON == 'to_json':
            instancedata = json.loads(instancedata.to_json())
        self.assertTrue(instancedata == resp)
