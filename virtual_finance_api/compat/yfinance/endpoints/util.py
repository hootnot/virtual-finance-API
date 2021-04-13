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
