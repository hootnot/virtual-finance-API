# -*- coding: utf-8 -*-

import time
from datetime import datetime
import re

try:
    import rapidjson as json

except ImportError as err:
    import json


def get_store(resp, store):
    jsontxt = (
        resp.split("root.App.main =")[1].split("(this)")[0].split(";\n}")[0].strip()
    )
    return json.loads(jsontxt)["context"]["dispatcher"]["stores"][store]


def response2json(resp):
    _resp = get_store(resp, "QuoteSummaryStore")
    _resp = json.dumps(_resp).replace("{}", "null")
    _resp = re.sub(r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", _resp)
    return json.loads(_resp)


def extract_domain(url):
    m = re.match("^.*://(?:www.|)(.*)", url)
    try:
        return m.group(1)

    except IndexError:
        return ""


def hprocopt(
    period="1mo",
    interval="1d",
    start=None,
    end=None,
    prepost=False,
    actions=True,
    auto_adjust=True,
    back_adjust=False,
    proxy=None,
    rounding=False,
    tz=None,
    **kwargs,
):
    def convtime(t):
        if isinstance(t, datetime):
            return int(time.mktime(t.timetuple()))
        else:
            return int(time.mktime(time.strptime(str(t), "%Y-%m-%d")))

    if auto_adjust and back_adjust:
        raise ValueError("auto/back adjust are mutually exclusive")

    if proxy:
        logger.warning("proxy is ignored: configure proxy via the Client")

    params = {
        "events": "div,splits",
        "interval": interval.lower(),
        "includePrePost": prepost,
        "includeAdjustedClose": True,
        "prepost": prepost,
        "actions": actions,
        "tz": tz,
        "rounding": rounding,
    }

    if auto_adjust:
        params.update({"adjust": "auto"})
    elif back_adjust:
        params.update({"adjust": "backadjust"})

    if end is None:
        params.update({"period2": int(time.time())})

    else:
        params.update({"period2": convtime(end)})

    if start:
        params.update({"period1": convtime(start)})

    else:
        if period.lower() == "max":
            params.update({"period1": -2208988800})

        else:
            params.update({"range": period.lower()})

    return params
