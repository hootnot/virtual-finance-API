Virtual Finance API
===================


.. .. image:: https://img.shields.io/pypi/v/virtual_finance_api.svg
        :target: https://pypi.python.org/pypi/virtual_finance_api

.. image:: https://img.shields.io/travis/hootnot/virtual-finance-API.svg
        :target: https://travis-ci.com/hootnot/virtual-finance-API

.. .. image:: https://readthedocs.org/projects/virtual-finance-api/badge/?version=latest
        :target: https://virtual-finance-api.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/hootnot/virtual-finance-API/badge.svg?branch=main
        :target: https://coveralls.io/github/hootnot/virtual-finance-API?branch=main



Virtual Finance API provides access to data from financial sites as if it was a REST-API.

As easy as:

.. code-block::

   import json
   import virtual_finance_api as fa
   import virtual_finance_api.endpoints.yahoo as yh

   client = fa.Client()
   r = yh.Holders('IBM')
   rv = client.request(r)
   print(json.dumps(rv, indent=2))

   {
     "major": {
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
     },
     "institutional": {
       "Holder": {
         "0": "Vanguard Group, Inc. (The)",
         "1": "Blackrock Inc.",
         "2": "State Street Corporation",
         "3": "Geode Capital Management, LLC",
         "4": "Charles Schwab Investment Management, Inc.",
         "5": "Northern Trust Corporation",
         "6": "Morgan Stanley",
         "7": "Bank Of New York Mellon Corporation",
         "8": "Norges Bank Investment Management",
         "9": "Bank of America Corporation"
       },
       "Shares": {
         "0": 73806391,
         "1": 62271273,
         "2": 51941856,
         "3": 13310817,
         "4": 12571878,
         "5": 10652880,
         "6": 9853901,
         "7": 9628160,
         "8": 8865649,
         "9": 8074146
       },
       "Date Reported": {
         "0": "Dec 30, 2020",
         "1": "Dec 30, 2020",
         "2": "Dec 30, 2020",
         "3": "Dec 30, 2020",
         "4": "Dec 30, 2020",
         "5": "Dec 30, 2020",
         "6": "Dec 30, 2020",
         "7": "Dec 30, 2020",
         "8": "Dec 30, 2020",
         "9": "Dec 30, 2020"
       },
       "% Out": {
         "0": "8.26%",
         "1": "6.97%",
         "2": "5.81%",
         "3": "1.49%",
         "4": "1.41%",
         "5": "1.19%",
         "6": "1.10%",
         "7": "1.08%",
         "8": "0.99%",
         "9": "0.90%"
       },
       "Value": {
         "0": 9290748499,
         "1": 7838707845,
         "2": 6538440833,
         "3": 1675565643,
         "4": 1582548002,
         "5": 1340984534,
         "6": 1240409057,
         "7": 1211992780,
         "8": 1116007896,
         "9": 1016373498
       }
     },
     "mutualfund": {
       "Holder": {
         "0": "Vanguard Total Stock Market Index Fund",
         "1": "Vanguard 500 Index Fund",
         "2": "SPDR S&P 500 ETF Trust",
         "3": "Fidelity 500 Index Fund",
         "4": "Vanguard Institutional Index Fund-Institutional Index Fund",
         "5": "iShares Core S&P 500 ETF",
         "6": "Vanguard Index-Value Index Fund",
         "7": "SPDR Dow Jones Industrial Average ETF",
         "8": "Franklin Custodian Funds-Income Fund",
         "9": "Schwab Strategic Tr-Schwab U.S. Dividend Equity ETF"
       },
       "Shares": {
         "0": 25108610,
         "1": 17854830,
         "2": 9085980,
         "3": 8074523,
         "4": 7327901,
         "5": 6866860,
         "6": 5998301,
         "7": 5493768,
         "8": 4487000,
         "9": 4463676
       },
       "Date Reported": {
         "0": "Dec 30, 2020",
         "1": "Dec 30, 2020",
         "2": "Feb 27, 2021",
         "3": "Jan 30, 2021",
         "4": "Dec 30, 2020",
         "5": "Feb 27, 2021",
         "6": "Dec 30, 2020",
         "7": "Feb 27, 2021",
         "8": "Dec 30, 2020",
         "9": "Nov 29, 2020"
       },
       "% Out": {
         "0": "2.81%",
         "1": "2.00%",
         "2": "1.02%",
         "3": "0.90%",
         "4": "0.82%",
         "5": "0.77%",
         "6": "0.67%",
         "7": "0.61%",
         "8": "0.50%",
         "9": "0.50%"
       },
       "Value": {
         "0": 3160671826,
         "1": 2247566000,
         "2": 1080595601,
         "3": 961756434,
         "4": 922436177,
         "5": 816675659,
         "6": 755066129,
         "7": 653373828,
         "8": 564823560,
         "9": 551353259
       }
     }
   }



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
