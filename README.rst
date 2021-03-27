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



The `Virtual Finance API` provides access to data from financial sites as if it was a REST-API.
Currently covered:

  + yahoo 'endpoints' to get:

    - profile
    - holders
    - financials
    - history

  + business inisder 'endpoint':

    - fetch ISIN code

With `request-classes` for these endpoints, getting data is as easy as:

.. code-block:: python

   import json
   import virtual_finance_api as fa
   import virtual_finance_api.endpoints.yahoo as yh

   client = fa.Client()
   r = yh.Holders('IBM')
   rv = client.request(r)
   # lets get the 'major' holders from that JSON response
   print(json.dumps(rv['major'], indent=2))

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



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
