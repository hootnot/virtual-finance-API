Changelog
=========

[Unreleased]
------------

v0.5.0 (2021-05-30)
-------------------

New Features
~~~~~~~~~~~~

-  [types] types Period, Interval added

Refactoring
~~~~~~~~~~~

-  [cli] type hints, apply yahoo types

-  [tests] switch to pytest from unittest

-  [cli] rename entrypoint to vfapi

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  [README] minor changes/extension in install

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [setup] correct URL to repository

v0.4.3 (2021-05-17)
-------------------

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  [README] add codestyle ‘black’ badge

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [setup.py] delete ‘version=’ from version

v0.4.2 (2021-05-17)
-------------------

Bug Fixes
~~~~~~~~~

-  [yahoo.Profile] add a 404

Refactoring
~~~~~~~~~~~

-  apply typing

v0.4.1 (2021-04-15)
-------------------

Style Fixes
~~~~~~~~~~~

-  [black] black applied to library + tests + setup.py

Refactoring
~~~~~~~~~~~

-  [endpoints] make the basic requests return the standardized JSON of
   the extensions.stdjson requests. Remove the extensions.stdjson.
   Modify compat.yfinance to use the standardized JSON.

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [pre-commit] added / configured pre-commit

v0.4.0 (2021-04-13)
-------------------

New Features
~~~~~~~~~~~~

-  [endpoints] extensions.stdjson, a standardized JSON layer

Tests
~~~~~

-  [unittest] unittests regarding virtual_finance_api.extensions.stdjson
   virtual_finance_api.client

-  [unittest] yfinance Ticker class tests extended

Bug Fixes
~~~~~~~~~

-  [Makefile] prevent link creation by pandoc

-  [compat.yfinance] Ticker property code fixed for properties:
   dividends splits actions

Style Fixes
~~~~~~~~~~~

-  minor EOL whitespace / empty line changes

Refactoring
~~~~~~~~~~~

-  [enpoints] History, Options now VirtualAPIRequests

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  [endpoints] extensions.stdjson added

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [CHANGELOG] templates to generate CHANGELOG

v0.3.2 (2021-03-30)
-------------------

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [requirements] python 3.6 up to pandas 1.1.5

v0.3.1 (2021-03-30)
-------------------

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  [README] badges added

-  [README] extended with various components

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [config] setup.py include requirements correctly

-  [travis] fix deployment to pypi

v0.3.0 (2021-03-30)
-------------------

New Features
~~~~~~~~~~~~

-  [endpoints] yfinance compatibility endpoints

Tests
~~~~~

-  [unitttest] yfinance compatible endpoint tests

Bug Fixes
~~~~~~~~~

-  [docs] requirements_dev: missing packages

Refactoring
~~~~~~~~~~~

-  [endpoints] use rapidjson instead of json

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [config] requirements, Makefile update requirements: include
   rapidjson Makefile extended

-  [config] update travis / tox config

v0.2.2 (2021-03-27)
-------------------

Bug Fixes
~~~~~~~~~

-  [docs] fix sphinx build

v0.2.1 (2021-03-27)
-------------------

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-  [sphinx] initial documentation setup

-  [README] example added

v0.2.0 (2021-03-26)
-------------------

New Features
~~~~~~~~~~~~

-  [yahoo endpoints] Yahoo endpoint request classes

-  [endpoints] business_insider ISIN request class

-  [generic] ISINCode class to handle ISIN-codes

-  [base] base classes classes to handle and setup API requests

Tests
~~~~~

-  [yahoo endpoints] unittests for yahoo endpoints

-  [unittests] test business_insider endpoint(s)

-  [unittest] tests to test Client and generic module

Administration and Chores
~~~~~~~~~~~~~~~~~~~~~~~~~

-  [config] setup travis for coverage, add badges to README.rst

-  [config] setup.py and requirements

-  [travis] removed unsupported python 3.5

-  [config] fix tox config

-  [requirements] packages added
