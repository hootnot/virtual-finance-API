# -*- coding: utf-8 -*-

import re
from virtual_finance_api.endpoints.yahoo.types import AdjustType, Period, Interval


def camel2title(o):
    return [re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", i).title() for i in o]


class YFHolders:
    def __init__(self, std):
        self._std = std

    def major(self):
        L = []
        R = []

        for i in self._std["major"]:
            L.append(i[0])
            R.append(i[1])

        return {"major": {"0": L, "1": R}}

    def _conv(self, subject):

        yf = {}
        legend = self._std[subject]["legend"]

        for i, holder in enumerate(self._std[subject]["holders"]):
            for s in ["holder", "shares", "date_reported", "pch_out", "value"]:
                key = legend[s]
                if key not in yf:
                    yf.update({key: {}})
                yf[key].update({str(i): holder[s]})

        return {subject: yf}

    def institutional(self):
        return self._conv("institutional")

    def mutualfund(self):
        return self._conv("mutualfund")

    def convert(self):
        r = {}
        r.update(self.major())
        r.update(self.institutional())
        r.update(self.mutualfund())

        return r


def yfprocopt(
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
) -> dict:
    """yfprocopt - parse parameters in an yfinance compatible way.

    manipulate them to be used by procopt.
    """

    if auto_adjust and back_adjust:
        raise ValueError("auto/back adjust are mutually exclusive")

    if proxy:
        logger.warning("proxy is ignored: configure proxy via the Client")

    params = {}

    params.update({"period": getattr(Period, f"p_{period}")})
    params.update({"interval": getattr(Interval, f"i_{interval}")})
    params.update({"start": start})
    params.update({"end": end})
    params.update({"prepost": prepost})
    params.update({"actions": actions})
    params.update({"rounding": rounding})
    params.update({"tz": tz})

    if auto_adjust:
        params.update({"adjust": AdjustType.auto})

    elif back_adjust:
        params.update({"adjust": AdjustType.back})

    return params
