# -*- coding: UTF-8 -*-
"""decorators."""


def dyndoc_insert(src):
    """docstring_insert - a decorator to insert API-docparts dynamically."""
    # manipulating docstrings this way is tricky due to indentation
    # the JSON needs leading whitespace to be interpreted correctly
    import json
    import re

    def mkblock(d, flag=0):
        # response, pretty formatted
        v = json.dumps(d, indent=2)
        if flag == 1:
            # strip the '[' and ']' in case of a list holding items
            # that stand on their own (example: tick records from a stream)
            nw = re.findall('.*?[(.*)]', v, flags=re.S)
            v = nw[0]
        # add leading whitespace for each line and start with a newline
        return "\n{}".format("".join(["{0:>16}{1}\n".format("", L)
                             for L in v.split('\n')]))

    def dec(obj):
        allSlots = re.findall("{(_.*?)}", obj.__doc__)
        docsub = {}
        sub = {}
        for k in allSlots:
            p = re.findall("^(_.*)_(.*)", k)
            p = list(*p)
            sub.update({p[1]: p[0]})

        for v in sub.values():
            for k in sub.keys():
                docsub["{}_url".format(v)] = "{}".format(src[v]["url"])
                if "resp" == k:
                    docsub.update({"{}_resp".format(v):
                                   mkblock(src[v]["response"])})
                if "body" == k:
                    docsub.update({"{}_body".format(v):
                                   mkblock(src[v]["body"])})

                if "params" == k:
                    docsub.update({"{}_params".format(v):
                                   mkblock(src[v]["params"])})
                if "ciresp" == k:
                    docsub.update({"{}_ciresp".format(v):
                                   mkblock(src[v]["response"], 1)})

        obj.__doc__ = obj.__doc__.format(**docsub)

        return obj

    return dec


def endpoint(url, domain=None, method="GET", response_type="txt", expected_status=200):  # noqa E501
    """endpoint - decorator to manipulate the REST-service endpoint.
    The endpoint decorator sets the endpoint and the method for the class
    to access the REST-service.
    """
    def dec(obj):
        obj.ENDPOINT = url
        obj.DOMAIN = domain
        obj.METHOD = method
        obj.EXPECTED_STATUS = expected_status
        obj.RESPONSE_TYPE = response_type
        return obj

    return dec
