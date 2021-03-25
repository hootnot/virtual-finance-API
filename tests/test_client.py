# -*- coding: utf-8 -*-

import unittest
import json
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError
)
import virtual_finance_api as fa
from requests.exceptions import RequestException
from virtual_finance_api.endpoints.decorators import endpoint
from virtual_finance_api.endpoints.apirequest import (
    APIRequest,
    VirtualAPIRequest
)
import requests_mock

try:
    from parameterized import parameterized  # noqa F401

except Exception as err:  # noqa F841
    print("*** Please install 'parameterized' to run these tests ***")
    exit(0)


@endpoint("some/{ticker}/thing", domain="ttps://test.com")  # force error
class FakeRequest(APIRequest):
    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(FakeRequest, self).__init__(endpoint, method=self.METHOD)


@endpoint("some/{ticker}/thing", domain="ttps://test.com")  # force error
class FakeVirtualRequest(VirtualAPIRequest):
    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(FakeVirtualRequest, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        return s


@endpoint("some/{ticker}/thing", domain="https://test.com")
class Simulate(VirtualAPIRequest):

    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(Simulate, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        return s[::-1]


@endpoint("some/{ticker}/thing", domain="https://test.com",
          response_type="json")
class SimulateStCh(VirtualAPIRequest):

    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(SimulateStCh, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        try:
            _s = json.loads(s)

        except Exception as err:  # noqa F841
            raise ConversionHookError(422, 'Processing error')

        else:
            try:
                t = _s['tickerlist'][1]

            except Exception as err:  # noqa F841
                raise ConversionHookError(404, 'Processing error')

            else:
                return {'data': t[::-1]}


client = None
API_URL = 'https://test.com'


class TestClient(unittest.TestCase):
    """Tests regarding the accounts endpoints."""

    def setUp(self):
        """setup for all tests."""
        global client
        # self.maxDiff = None
        try:
            # client = Client(headers={"Content-Type": "application/json"})
            client = fa.Client()
            # api.api_url = 'https://test.com'
            pass
        except Exception as e:
            print("%s" % e)
            exit(0)

    def test__client_request_params(self):
        """request parameters."""
        request_params = {"timeout": 10}
        client = fa.Client(request_params=request_params)
        self.assertTrue(client.request_params == request_params)

    def test__client_requestexception(self):
        """force a requests exception."""
        client = fa.Client(headers={"Content-Type": "application/json"})
        text = "No connection " \
               "adapters were found for 'ttps://test.com/some/IBM/thing'"
        r = FakeRequest('IBM')
        with self.assertRaises(RequestException) as err:
            client.request(r)

        self.assertEqual("{}".format(err.exception), text)

    def test__requests001(self):
        """expected status fetch."""
        r = FakeVirtualRequest('IBM')
        self.assertTrue(r.expected_status == 200)

    def test__requests002(self):
        """conversion_hook."""
        r = FakeVirtualRequest('IBM')
        self.assertTrue(r._conversion_hook('abc') == 'abc')

    @requests_mock.Mocker()
    def test__expected_status(self, mock_req):
        """expected status."""
        indata = "abcde"
        r = Simulate('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=indata)
        client.request(r)
        self.assertTrue(r.response[::-1] == indata and
                        r.expected_status == r.status_code)

    @requests_mock.Mocker()
    def test__statuschange_422(self, mock_req):
        """status change due to conversionhook error."""
        indata = ""

        r = SimulateStCh('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=indata)
        result = None
        with self.assertRaises(VirtualFinanceAPIError) as err:
            result = client.request(r)
        self.assertTrue(result is None and
                        r.status_code == 422 and
                        err.exception.code == 422)

    @requests_mock.Mocker()
    def test__statuschange_404(self, mock_req):
        """status change due to conversionhook error."""
        # force a conversion_hook error by 1 elem. list
        indata = json.dumps({'tickerlist': ['IBM']})

        r = SimulateStCh('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=indata)
        result = None
        with self.assertRaises(VirtualFinanceAPIError) as err:
            result = client.request(r)
        self.assertTrue(result is None and
                        r.status_code == 404 and
                        err.exception.code == 404)

    @requests_mock.Mocker()
    def test__conversion(self, mock_req):
        """status change due to conversionhook error."""
        indata = json.dumps({'tickerlist': ['IBM', 'CSCO']})

        r = SimulateStCh('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=indata)
        result = client.request(r)
        self.assertTrue(result == {'data': 'OCSC'} and
                        r.status_code == 200)
