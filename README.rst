Virtual Finance API
===================


.. .. image:: https://img.shields.io/pypi/v/virtual_finance_api.svg
        :target: https://pypi.python.org/pypi/virtual_finance_api

.. image:: https://img.shields.io/travis/hootnot/virtual-finance-API.svg
        :target: https://travis-ci.com/hootnot/virtual-finance-API

.. image:: https://readthedocs.org/projects/virtual-finance-api/badge/?version=latest
        :target: https://virtual-finance-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/hootnot/virtual-finance-API/badge.svg?branch=main
        :target: https://coveralls.io/github/hootnot/virtual-finance-API?branch=main

.. image:: https://img.shields.io/pypi/v/virtual_finance_api.svg
        :target: https://pypi.org/project/virtual_finance_api
        :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/virtual_finance_api.svg
        :target: https://pypi.org/project/virtual_finance_api
        :alt: Python versions

Interactive
-----------

.. image:: https://jupyter.readthedocs.io/en/latest/_static/_images/jupyter.svg
   :target: ./jupyter
   :alt: Jupyter

Using the Jupyter `notebook`_ it is easy to experiment with the
*virtual_finance_api* library.

.. _notebook: ./jupyter/index.ipynb



Install
-------

.. code-block:: bash

   # Setup a virtual environment
   $ mkdir tst_vfa
   $ cd tst_vfa
   $ python3 -m venv venv38
   $ . ./venv38/bin/activate
   (venv38) feite@salmay:~/tst_vfa$

   $ pip install virtual_finance_api

With *virtual_finance_api* installed, it is directly available via the commandline:

.. code-block:: bash

   $ virtual_finance_api --help
   Usage: virtual_finance_api [OPTIONS] COMMAND [ARGS]...

     Virtual Finance API commandline app.

   Options:
     --help  Show this message and exit.

   Commands:
     financials
     history
     holders
     profile     Profile.


... additional help on the *history* command:

.. code-block:: bash

   virtual_finance_api history --help
   Usage: virtual_finance_api history [OPTIONS] TICKER

   Options:
     --period [1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max]
     --interval [1m|2m|5m|15m|30m|60m|90m|1h|1d|5d|1wk|1mo|3mo]
     --csv
     --help                          Show this message and exit.

So, lets query for some history for IBM ...

.. code-block:: bash

   $ virtual_finance_api history IBM
                              Open        High         Low       Close   Volume
   2021-03-01 14:30:00  120.349998  122.320000  119.860001  120.739998  5714500
   2021-03-02 14:30:00  120.739998  121.900002  120.260002  120.330002  4522200
   2021-03-03 14:30:00  120.500000  122.629997  119.980003  122.360001  7396200
   2021-03-04 14:30:00  122.000000  123.220001  118.760002  120.110001  8062100
   2021-03-05 14:30:00  120.639999  123.750000  120.250000  122.830002  6944900
   2021-03-08 14:30:00  122.989998  126.849998  122.879997  124.809998  7236600
   2021-03-09 14:30:00  125.400002  126.430000  124.160004  124.180000  5608200
   2021-03-10 14:30:00  125.050003  128.240005  124.610001  127.870003  7243500
   2021-03-11 14:30:00  128.089996  128.639999  126.779999  127.139999  5145000
   2021-03-12 14:30:00  127.190002  127.680000  126.610001  127.610001  4009600
   2021-03-15 13:30:00  127.769997  128.750000  127.540001  128.580002  3420600
   2021-03-16 13:30:00  128.279999  128.520004  127.339996  128.240005  4630400
   2021-03-17 13:30:00  128.460007  129.490005  127.489998  129.029999  4244800
   2021-03-18 13:30:00  128.940002  131.000000  127.790001  130.059998  5834600
   2021-03-19 13:30:00  130.020004  130.440002  128.529999  128.899994  9830600
   2021-03-22 13:30:00  128.500000  130.720001  127.889999  130.550003  4164900
   2021-03-23 13:30:00  130.440002  131.559998  129.800003  130.460007  4356400
   2021-03-24 13:30:00  130.949997  132.110001  130.570007  130.619995  4005000
   2021-03-25 13:30:00  130.330002  133.240005  129.770004  133.070007  5554000
   2021-03-26 13:30:00  133.289993  136.479996  133.119995  136.380005  5562500
   2021-03-29 13:30:00  135.979996  137.070007  135.509995  135.860001  4620900


The `Virtual Finance API` provides access to data from financial sites as if it was a REST-API.
Currently covered:

  + yahoo 'endpoints' to get:

    - profile
    - holders
    - financials
    - history

  + business inisder 'endpoint':

    - fetch ISIN code

  + yfinance compatibility 'endpoints'


With `request-classes` for these endpoints, getting data is as easy as:

.. code-block:: python

   >>> import json
   >>> import virtual_finance_api as fa
   >>> import virtual_finance_api.endpoints.yahoo as yh

   >>> client = fa.Client()
   >>> r = yh.Holders('IBM')
   >>> rv = client.request(r)
   # lets get the 'major' holders from that JSON response
   >>> print(json.dumps(rv['major'], indent=2))

   {
      "0": {
        "0": "0.13%",
        "1": "58.58%",
        "2": "58.66%",
        "3": "2561"
      },
      "1": {
        "0": "% of Shares Held by All Insider",
        "1": "% of Shares Held by Institutions",
        "2": "% of Float Held by Institutions",
        "3": "Number of Institutions Holding Shares"
      }
   }

Yfinance compatibility
----------------------

There is a compatibility layer with `Yfinance <https://github.com/ranaroussi/yfinance>`_ too. It provides
requests derived from the base requests, extended with properties that give the same information
as `Yfinance <https://github.com/ranaroussi/yfinance>`_  does.

The *Holders*-example from above becomes:

.. code-block:: python

   >>> import json
   >>> import virtual_finance_api as fa
   >>> import virtual_finance_api.compat.yfinance.endpoints as yf

   >>> client = fa.Client()
   >>> r = yf.Holders('IBM')
   >>> rv = client.request(r)
   >>> # lets get the 'major' holders from that JSON response
   >>> print(r.major)


           0                                      1
   0   0.13%        % of Shares Held by All Insider
   1  58.58%       % of Shares Held by Institutions
   2  58.66%        % of Float Held by Institutions
   3    2561  Number of Institutions Holding Shares

   >>> # or, that same information from the dataframe in JSON
   >>> # (dump, load, dump to 'pretty print')
   >>> print(json.dumps(json.loads(r.major.to_json()), indent=2))
   {
      "0": {
        "0": "0.13%",
        "1": "58.58%",
        "2": "58.66%",
        "3": "2561"
      },
      "1": {
        "0": "% of Shares Held by All Insider",
        "1": "% of Shares Held by Institutions",
        "2": "% of Float Held by Institutions",
        "3": "Number of Institutions Holding Shares"
      }
   }

   >>> print(r.institutional)
                                          Holder    Shares Date Reported   % Out       Value
   0                  Vanguard Group, Inc. (The)  73806391    2020-12-30  0.0826  9290748499
   1                              Blackrock Inc.  62271273    2020-12-30  0.0697  7838707845
   2                    State Street Corporation  51941856    2020-12-30  0.0581  6538440833
   3               Geode Capital Management, LLC  13310817    2020-12-30  0.0149  1675565643
   4  Charles Schwab Investment Management, Inc.  12571878    2020-12-30  0.0141  1582548002
   5                  Northern Trust Corporation  10652880    2020-12-30  0.0119  1340984534
   6                              Morgan Stanley   9853901    2020-12-30  0.0110  1240409057
   7         Bank Of New York Mellon Corporation   9628160    2020-12-30  0.0108  1211992780
   8           Norges Bank Investment Management   8865649    2020-12-30  0.0099  1116007896
   9                 Bank of America Corporation   8074146    2020-12-30  0.0090  1016373498

See the `<https://virtual-finance-api.readthedocs.io/en/latest/?badge=latest>`_ for details.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
