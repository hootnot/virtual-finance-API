# -*- coding: utf-8 -*-

import re


def camel2title(o):
    return [re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", i).title() for i in o]


def extract_domain(url):
    m = re.match("^.*://(?:www.|)(.*)", url)
    try:
        return m.group(1)

    except IndexError:
        return ""


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
