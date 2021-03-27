Motivation
==========

While building a service on a task based concept using `Celery <https://docs.celeryproject.org/en/stable/index.html>`_ or
`Dramatiq <https://dramatiq.io>`_, I ran into connection related issues using for instance a library like
`yfinance <https://github.com/ranaroussi/yfinance>`_ . These issues occured when firing a large number of
requests asynchronously.

In the need of an, over all, more fine grained control I, decided to write a new library:

    + easy to scale
    + easy to maintain
    + easy to extend
    + integrated logging
    + compatibility layers

      - *yfinance* compatibility package


REST-API
--------

Since I'm a fan of REST-API's, the thought was to approach this as a wrapper for a REST-API, in this case
a *"virtual-REST-API"*.

Two basic components
^^^^^^^^^^^^^^^^^^^^

    *Request* classes to represent the specfic requests providing an API like a REST-API
    with *route-parameters* and *query parameters*. When executed the request instance will
    hold the response and the HTTP-status.

    A *Client* performing the requests.

Since `<finance.yahoo.com>`_ provides no real REST-API, the requests of the wrappper fake the REST-API.
A *request* instance holds the details for the URL to call. In case it is HTML-data that needs to be
processed to scrape the information, a *conversion* method is run after the HTML-data is received.

This second stage of processing gives the desired JSON-response or, in case of errors some 4xx
error code is returned. The client processes this the same way as if it was the response of a REST-API.

In case the second stage processing fails the original status code is set to a code identifying
the final state:

     + if processing was without errors but the desired result could not be created the status code is changed to 404, 'Not Found'
     + if processing gave errors the status code is changed to 422, 'Unprocessable Entity'

These status codes represent a REST-API server responding to client requests.


There are a handful of endpoints that provide the information we need.
The request classes wrap the logic to provide the JSON data fetched from
the response, so acting as if that response was provided by Yahoo Finance.
