""" initialization of unittests and data for unittests """

import time
import zipfile
import json
import pytest
import virtual_finance_api as fa

# calculate expiryDate as an offset from today
# now + 5 days
days = 5
expiryDate = time.strftime(
    "%Y-%m-%dT%H:%M:%S", time.localtime(int(time.time() + 86400 * days))
)

API_URL = "https://test.com"


@pytest.fixture
def client():
    return fa.Client()


def fetchTestData(responses, k):
    resp = responses[k]["response"]
    params, data = None, None
    if "body" in responses[k]:
        data = responses[k]["body"]

    if "params" in responses[k]:
        params = responses[k]["params"]

    if params is not None:
        return (resp, data, params)

    return (resp, data)


def fetchFullResponse(entry, isJSON=True):
    with zipfile.ZipFile("./tests/full_responses/full_responses.zip") as ZIPIN:
        _entry = f"{entry}.json"
        with ZIPIN.open(_entry) as TSTDATA:
            rawdata = TSTDATA.read().decode("utf-8")
            if isJSON:
                return json.loads(rawdata)
            else:
                return rawdata


def fetchRawData(entry):
    with zipfile.ZipFile("./tests/raw_html_data/raw_html.zip") as ZIPIN:
        with ZIPIN.open(entry) as TSTDATA:
            rawdata = TSTDATA.read().decode("utf-8")
            return rawdata

    return None


class TestData(object):
    def __init__(self, responses, tid):
        self._responses = responses[tid]

    @property
    def resp(self):
        return self._responses["response"]

    @property
    def body(self):
        return self._responses["body"]

    @property
    def params(self):
        return self._responses["params"]
