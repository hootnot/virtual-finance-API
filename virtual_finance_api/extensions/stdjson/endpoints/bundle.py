# -*- coding: utf-8 -*-

"""This module provides the request classes that provide a 'normalized' JSON
response. The responses from the base request classes can have an inconveniant
format. The request classes from this module provide JSON data in standardized
way.
"""
from virtual_finance_api.compat.yfinance.endpoints.util import extract_domain
import virtual_finance_api.endpoints.yahoo as yhe
from virtual_finance_api.compat.yfinance.endpoints.bundle import hprocopt
from virtual_finance_api.exceptions import ConversionHookError
from .responses.bundle import responses
from virtual_finance_api.endpoints.decorators import dyndoc_insert
import logging


logger = logging.getLogger(__name__)


class Financials(yhe.Financials):
    """Financials - class to handle the financials endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Financials APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> # import the standardized JSON endpoints
        >>> import virtual_finance_api.extensions.json.endpoints as je
        >>> client = fa.Client()
        >>> r = je.Financials('IBM')
        >>> rv = client.request(r)
        >>> print(json.dumps(rv['earnings'], indent=2))


        ::

            {_je_financials_resp}

        """
        super(Financials, self).__init__(ticker)
        self.base = False

    def _conversion_hook(self, s):
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            { 'balancesheet': {
                 'yearly': {},
                 'quarterly': {},
              },
              ...
            }

        for all groups.
        """
        data = super(Financials, self)._conversion_hook(s)
        _resp = {}

        try:

            for repgroup in (
                ('cashflow', 'cashflowStatement', 'cashflowStatements'),
                ('balancesheet', 'balanceSheet', 'balanceSheetStatements'),
                ('financials', 'incomeStatement', 'incomeStatementHistory')
            ):
                attr, subject, details = repgroup
                for itemDetail, key in [('', 'yearly'), ('Quarterly', 'quarterly')]:  # noqa E501
                    item = f'{subject}History{itemDetail}'
                    if isinstance(data.get(item), dict):
                        if attr not in _resp:
                            _resp.update({attr: {}})
                        _resp[attr].update({key: data[item][details]})

            # earnings
            if data.get('earnings', None):
                _resp.update({'earnings': data['earnings']['financialsChart']})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, '')

        else:
            return _resp


class Holders(yhe.Holders):
    """Holders - class to handle the holders endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Holders APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.extensions.json.endpoints as je
        >>> client = fa.Client()
        >>> r = je.Holders('IBM')
        >>> rv = client.request(r)

        ::

            {_je_holders_resp}

        """
        super(Holders, self).__init__(ticker)
        self.base = False
        self._holders = {}

    def _conversion_hook(self, s):
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            { 'holders': {
                 'major': {},
                 'institutional': {},
                 'mutualfund': {},
              }
            }

        """
        def normalize(data, K):
            _record = {}
            _legend = {}
            for k, v in data[K].items():
                _k = k.lower().replace(' ', '_').replace('%', 'pch')
                if _k not in _legend:
                    _legend.update({_k: k})
                for i, (kk, vv) in enumerate(v.items()):
                    if i not in _record:
                        _record.update({i: {}})
                    if isinstance(vv, (str,)) and '%' in vv:
                        vv = float(vv.replace('%', ''))
                    _record[i].update({_k: vv})

            return {
                    'legend': _legend,
                    'holders': list(_record.values())
            }

        data = super(Holders, self)._conversion_hook(s)
        _resp = {}

        try:
            _resp.update({
                'major':
                [list(l) for l in zip(data['major']['0'].values(), data['major']['1'].values())]  # noqa E501
            })
            for k in ['institutional', 'mutualfund']:
                try:
                    ndd = normalize(data, k)

                except KeyError as err:
                    # allow that error
                    logger.warning(err)

                else:
                    if ndd:
                        _resp.update({k: ndd})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, '')

        else:
            return _resp


class Profile(yhe.Profile):

    """Profile - class to handle the profile endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate a Profile APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> # import the yfinance compatible endpoints
        >>> import virtual_finance_api.extensions.json.endpoints as je
        >>> client = fa.Client()
        >>> r = je.Profile('IBM')
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.calendar)
        >>> # ... the calendar as a Pandas Dataframe

        >>> # the JSON representation of the dataframe
        >>> print(r.calendar.to_json())

        ::

            {_je_profile_resp}


        """
        super(Profile, self).__init__(ticker)

    def _conversion_hook(self, s):
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            {
               'profile': {
                   'recommendations': {},
                   'calendar': {},
                   'info': {},
               }
            }

        """
        data = super(Profile, self)._conversion_hook(s)
        resp = {}

        def info(response):
            rv = {}
            SECTIONS = [
                    'summaryProfile', 'summaryDetail', 'quoteType',
                    'defaultKeyStatistics', 'assetProfile', 'summaryDetail']
            for section in SECTIONS:
                if section in response:
                    rv.update(response[section])

            rv['regularMarketPrice'] = rv['regularMarketOpen']
            rv['logo_url'] = ""
            domain = extract_domain(rv['website'])
            if domain:
                rv['logo_url'] = f'https://logo.clearbit.com/{domain}'

            return rv

        def recommendations(response):
            return response['upgradeDowngradeHistory']['history']

        def calendar(response):
            return response['calendarEvents']

        def sustainability(response):
            return response['esgScores']

        try:
            resp.update({'info': info(data)})
            resp.update({'recommendations': recommendations(data)})
            resp.update({'calendar': calendar(data)})
            resp.update({'sustainability': sustainability(data)})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, '')

        else:
            return resp


class Options(yhe.Options):

    """Options - class to handle the options endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker):
        """Instantiate an Options APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.


        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.extensionse.stdjson.endpoints as je
        >>> client = fa.Client()
        >>> r = je.Options('IBM')
        >>> rv = client.request(r)

        >>> # now we can use the request properties to fetch data
        >>> print(r.options)
        >>> # ... the calendar as a Pandas Dataframe

        ::

            {_je_options_resp}

        """
        super(Options, self).__init__(ticker)

    def _conversion_hook(self, s):
        data = super(Options, self)._conversion_hook(s)

        resp = {}
        try:
            for attr in ['underlyingSymbol', 'expirationDates', 'strikes',
                         'hasMiniOptions', 'options']:
                resp.update({attr: data['optionChain']['result'][0][attr]})

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, '')

        else:
            return resp


class History(yhe.History):
    """History - class to handle the history endpoint."""

    @dyndoc_insert(responses)
    def __init__(self, ticker, params):
        """Instantiate a History APIRequest instance.

        Parameters
        ----------
        ticker : string (required)
            the ticker to perform the request for.

        params : dict (optional)
            dictionary with optional parameters to perform the request
            parameters default to 1 month of daily (1d) historical data.


        ::
            {_je_history_params}

        >>> import virtual_finance_api as fa
        >>> import virtual_finance_api.extensions.json.endpoints as je
        >>> client = fa.Client()
        >>> r = je.History('IBM', params=params)
        >>> rv = client.request(r)

        >>> print(r.response)

        ::

            {_je_history_resp}


        """
        super(History, self).__init__(ticker, params=hprocopt(**params))
        logger.info("%s instantiated, ticker: %s, params: %s",
                    self.__class__.__name__, self.ticker, self.params)

    def _conversion_hook(self, resp):
        """call the conversionhook of the parent class to get our data
        then standardize the JSON data here to get:

            {
               'ohlcdata': {...},
               'dividends': {...},
               'spits': {...},
            }

        """

        def _ordered_timeitems(d, cat):
            """
            dividends / splits
            yahoo has dicts with items like:
                "878826600": {
                   "amount": 0.1,
                   "date": 878826600
                },
            string type epoch as key, numeric value in the value dict
            this function transforms these dicts in a list of (epoch)
            ordered value dicts:
                [ {...},
                  {
                   "amount": 0.1,
                   "date": 878826600
                },
                ...
               ]
            """
            try:
                res = [d[cat][str(k)] for k in sorted(int(dt) for dt in d[cat].keys())]  # noqa E501

            except Exception as err:  # noqa F841
                logger.info("no data for: cat %s", cat)
                return []

            else:
                return res

        def adjust(ohlcdata, adjustType=None):
            """price adjustments for the historical data.

            for yfinance compatibility there are 2 adjustment types:
            - auto adjust
            - back adjust

            ohlcdata is: { 'timestamp': [...],
                           'open': [...],
                           'high': [...],
                           'low': [...],
                           'close': [...],
                           'volume': [...]}
            """
            if adjustType == 'auto':
                num, denom = 'close', 'adjclose'

            elif adjustType == 'backadjust':
                num, denom = 'adjclose', 'close'

            else:
                logger.warning('adjust: None')
                return ohlcdata

            ratio = [ohlcdata[num][i] / ohlcdata[denom][i] for i in range(len(ohlcdata['close']))]  # noqa E501

            ohlcdata['close'] = ohlcdata['adjclose']
            for qc in ['open', 'high', 'low']:
                ohlcdata[qc] = [ohlcdata[qc][i] / ratio[i] for i in range(len(ohlcdata['close']))]  # noqa E501

            return ohlcdata

        # transform the yahoo data
        data = super(History, self)._conversion_hook(resp)
        tdata = {}

        try:
            _data = data['chart']['result'][0]
            tdata.update({'meta': _data['meta']})
            tdata.update({'ohlcdata': {}})
            tdata['ohlcdata'].update({'timestamp': _data['timestamp']})
            tdata['ohlcdata'].update(_data['indicators']['quote'][0])
            tdata['ohlcdata'].update(_data['indicators']['adjclose'][0])
            if 'events' in _data:
                for cat in ['dividends', 'splits']:
                    try:
                        tdata.update({cat: _ordered_timeitems(_data['events'], cat)})  # noqa E501

                    except Exception as err:
                        logger.warning("no events for %s cat: %s [%s]",
                                       self.ticker, cat, err)

                    else:
                        logger.info("added: %s cat: %s, #%s",
                                    self.ticker, cat, len(tdata[cat]))

            # adjust data ?
            _pAdjust = self.params.get('adjust', None)
            if _pAdjust:
                logger.info('adjust: %s %s', self.ticker, _pAdjust)
                tdata['ohlcdata'] = adjust(tdata['ohlcdata'], adjustType=_pAdjust)  # noqa E501

        except Exception as err:
            logger.error(err)
            raise ConversionHookError(422, '')

        else:
            return tdata
