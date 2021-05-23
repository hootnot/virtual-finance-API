# -*- coding: utf-8 -*-

import pytest
import json
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError,
)
import virtual_finance_api as fa
from requests.exceptions import RequestException
from virtual_finance_api.endpoints.decorators import endpoint
from virtual_finance_api.endpoints.apirequest import APIRequest, VirtualAPIRequest


from .unittestsetup import API_URL, client


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


@endpoint("some/{ticker}/thing", response_type="json", domain="https://test.com")
class SimulateJSON(VirtualAPIRequest):
    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(SimulateJSON, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        return s


@endpoint("some/{ticker}/thing", domain="https://test.com", response_type="json")
class SimulateStCh(VirtualAPIRequest):
    def __init__(self, ticker):
        endpoint = self.ENDPOINT.format(ticker=ticker)
        super(SimulateStCh, self).__init__(endpoint, method=self.METHOD)

    def _conversion_hook(self, s):
        try:
            _s = json.loads(s)

        except Exception as err:  # noqa F841
            raise ConversionHookError(422, "Processing error")

        else:
            try:
                t = _s["tickerlist"][1]

            except Exception as err:  # noqa F841
                raise ConversionHookError(404, "Processing error")

            else:
                return {"data": t[::-1]}


def test_client_request_params():
    """request parameters."""
    request_params = {"timeout": 10}
    client = fa.Client(request_params=request_params)
    assert client.request_params == request_params


def test_client_requestexception():
    """force a requests exception."""
    client = fa.Client(headers={"Content-Type": "application/json"})
    text = "No connection " "adapters were found for 'ttps://test.com/some/IBM/thing'"
    r = FakeRequest("IBM")
    with pytest.raises(RequestException) as err:
        client.request(r)
    assert isinstance(err.value, (RequestException,))


def test_request_status():
    """expected status."""
    r = FakeVirtualRequest("IBM")
    assert r.expected_status == 200


def test_request_chook():
    """conversion_hook."""
    r = FakeVirtualRequest("IBM")
    assert r._conversion_hook("abc") == "abc"


def test__data(requests_mock, client):
    """sending data."""
    data = {"a": 10, "b": 20}
    r = SimulatePUT("IBM", data=data)
    requests_mock.register_uri("PUT", "{}/{}".format(API_URL, r), text="")
    client.request(r)
    assert r.expected_status == r.status_code and r.data == data


def test__404(requests_mock, client):
    """simulate a 404."""
    data = {"a": 10, "b": 20}
    r = SimulatePUT("IBM", data=data)
    requests_mock.register_uri(
        "PUT", "{}/{}".format(API_URL, r), status_code=404, text=""
    )
    with pytest.raises(VirtualFinanceAPIError) as err:
        client.request(r)
    assert err.value.code == 404


def test__json(requests_mock, client):
    """simulate a JSON endpoint."""
    data = {"a": 10, "b": 20}
    r = SimulateJSON("IBM")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=json.dumps(data))
    client.request(r)
    assert r.response == data


def test__json_err(requests_mock, client):
    """simulate a JSON endpoint error."""
    data = '{"a": 10, "b: 20}'  # error on purpose
    r = SimulateJSON("IBM")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=data)
    with pytest.raises(ValueError) as err:
        client.request(r)

    assert "response could not be loaded as JSON" in str(err.value)


def test__expected_status(requests_mock, client):
    """expected status."""
    indata = "abcde"
    r = Simulate("IBM")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=indata)
    client.request(r)
    assert r.response[::-1] == indata and r.expected_status == r.status_code


def test__statuschange_422(requests_mock, client):
    """status change due to conversionhook error."""
    indata = ""

    r = SimulateStCh("IBM")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=indata)
    result = None
    with pytest.raises(VirtualFinanceAPIError) as err:
        result = client.request(r)

    assert result is None and r.status_code == 422 and err.value.code == 422


def test__statuschange_404(requests_mock, client):
    """status change due to conversionhook error."""
    # force a conversion_hook error by 1 elem. list
    indata = json.dumps({"tickerlist": ["IBM"]})

    r = SimulateStCh("IBM")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=indata)
    result = None
    with pytest.raises(VirtualFinanceAPIError) as err:
        result = client.request(r)
    assert result is None and r.status_code == 404 and err.value.code == 404


def test__conversion(requests_mock, client):
    """test__conversion."""
    indata = json.dumps({"tickerlist": ["IBM", "CSCO"]})

    r = SimulateStCh("IBM")
    requests_mock.register_uri("GET", "{}/{}".format(API_URL, r), text=indata)
    result = client.request(r)
    assert result == {"data": "OCSC"} and r.status_code == 200
