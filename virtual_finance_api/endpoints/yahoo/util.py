# -*- coding: utf-8 -*-

try:
    import rapidjson as json
except ImportError as err:  # noqa F841
    import json

import re


def get_store(resp, store):
    jsontxt = resp.split('root.App.main =')[1].split(
                '(this)')[0].split(';\n}')[0].strip()
    return json.loads(jsontxt)['context']['dispatcher']['stores'][store]


def response2json(resp):
    _resp = get_store(resp, 'QuoteSummaryStore')
    _resp = json.dumps(_resp).replace('{}', 'null')
    _resp = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', _resp)
    return json.loads(_resp)
