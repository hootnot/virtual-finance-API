=====
Usage
=====

To use Virtual Finance API in a project simply create a *Client* and *Requests*
to be performed by the *Client* like:

.. code-block:: python

   import virtual_finance_api as fa
   import virtual_finance_api.endpoints.yahoo as yh
   import json


   client = fa.Client()
   ticker = 'IBM'
   r = yh.Profile(ticker)
   print(json.dumps(client.request(r), indent=2))

    {
      "defaultKeyStatistics": {
        "annualHoldingsTurnover": null,
        "enterpriseToRevenue": 2.274,
        "beta3Year": null,
        "profitMargins": 0.07593,
        "enterpriseToEbitda": 10.955,
        "52WeekChange": 0.2859279,
        "morningStarRiskRating": null,
        "forwardEps": 12.08,
        "revenueQuarterlyGrowth": null,
        "sharesOutstanding": 893593984,
        "fundInceptionDate": null,
        "annualReportExpenseRatio": null,
        "totalAssets": null,
        "bookValue": 23.074,
        "sharesShort": 30005072,
        "sharesPercentSharesOut": 0.0336,
        "fundFamily": null,
        "lastFiscalYearEnd": 1609372800,
        "heldPercentInstitutions": 0.58584,
        "netIncomeToCommon": 5501000192,
        "trailingEps": 6.233,
        ....             And a lot more ....
        "maxAge": 86400
      },
      "pageViews": {
        "shortTermTrend": "UP",
        "midTermTrend": "UP",
        "longTermTrend": "UP",
        "maxAge": 1
      }
    }


Exceptions
----------

To catch exceptions, wrap the *client.request()* in a try/catch like:

.. code-block:: python

   import virtual_finance_api as fa
   import virtual_finance_api.endpoints.yahoo as yh
   import json


   client = fa.Client()
   ticker = 'IBM'
   r = yh.Profile(ticker)
   try:
       rv = client.request(r)

   except fa.VirtualFinanceAPIError as err:
       print(err)

   else:
       print(json.dumps(rv, indent=2))


Logging
-------

The *virtual_finance_library* has logging integrated. By simply importing
the *logging* module and configuring it, you will have logging available.

.. code-block:: python

   import virtual_finance_api as fa
   import virtual_finance_api.endpoints.yahoo as yh
   import json
   import logging


   logging.basicConfig(
       filename="./your_appl_name.log",
       level=logging.INFO,
       format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
   )

   client = fa.Client()
   ticker = 'IBM'
   r = yh.Profile(ticker)
   try:
       rv = client.request(r)

   except fa.VirtualFinanceAPIError as err:
       print(err)

   else:
       print(json.dumps(rv, indent=2))

... and the log looks like:

 ::

  2021-04-09 14:26:28,884 [INFO] virtual_finance_api.client : performing request https://finance.yahoo.com/quote/IBM
  2021-04-09 14:26:29,359 [INFO] virtual_finance_api.endpoints.yahoo.ticker_bundle : conversion_hook: IBM OK
