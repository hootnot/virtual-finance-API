Changelog
=========

[Unreleased]
------------

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

-  [config] requirements, Makefile

   update requirements: include rapidjson Makefile extended
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

-  [endpoints] business_insider

   ISIN request class
-  [generic] ISINCode

   class to handle ISIN-codes
-  [base] base classes

   classes to handle and setup API requests

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
