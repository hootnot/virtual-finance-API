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
        # just to have some silly operation: reverse s 
        return s[::-1]


@endpoint("some/{ticker}/thing", method="PUT", domain="https://test.com")
class SimulatePUT(APIRequest):

    def __init__(self, ticker, data):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(SimulatePUT, self).__init__(endpoint, method=self.METHOD)
        self.data = data


@endpoint("some/{ticker}/thing", response_type='json', domain="https://test.com")
class SimulateJSON(VirtualAPIRequest):

    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(SimulateJSON, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        return s

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

    def test__request_status(self):
        """expected status."""
        r = FakeVirtualRequest('IBM')
        self.assertTrue(r.expected_status == 200)

    def test__request_chook(self):
        """conversion_hook."""
        r = FakeVirtualRequest('IBM')
        self.assertTrue(r._conversion_hook('abc') == 'abc')

    @requests_mock.Mocker()
    def test__data(self, mock_req):
        """sending data."""
        data = {'a': 10, 'b': 20}
        r = SimulatePUT('IBM', data=data)
        mock_req.register_uri('PUT',
                              "{}/{}".format(API_URL, r),
                              text="")
        client.request(r)
        self.assertTrue(r.expected_status == r.status_code and r.data == data)

    @requests_mock.Mocker()
    def test__404(self, mock_req):
        """simulate a 404."""
        data = {'a': 10, 'b': 20}
        r = SimulatePUT('IBM', data=data)
        mock_req.register_uri('PUT',
                              "{}/{}".format(API_URL, r),
                              status_code=404,
                              text="")
        with self.assertRaises(VirtualFinanceAPIError) as err:
            client.request(r)
        self.assertTrue(err.exception.code == 404)

    @requests_mock.Mocker()
    def test__json(self, mock_req):
        """simulate a JSON endpoint."""
        data = {'a': 10, 'b': 20}
        r = SimulateJSON('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=json.dumps(data))
        client.request(r)
        self.assertTrue(r.response == data)

    @requests_mock.Mocker()
    def test__json_err(self, mock_req):
        """simulate a JSON endpoint error."""
        data = '{"a": 10, "b: 20}'  # error on purpose
        r = SimulateJSON('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=data)
        with self.assertRaises(ValueError) as err:
            client.request(r)
        self.assertTrue("response could not be loaded as JSON" in str(err.exception))

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
        """test__conversion."""
        indata = json.dumps({'tickerlist': ['IBM', 'CSCO']})

        r = SimulateStCh('IBM')
        mock_req.register_uri('GET',
                              "{}/{}".format(API_URL, r),
                              text=indata)
        result = client.request(r)
        self.assertTrue(result == {'data': 'OCSC'} and
                        r.status_code == 200)
