# -*- coding: utf-8 -*-

"""Responses.

responses serve both testing purpose aswell as dynamic docstring replacement
"""
responses = {
  "_je_financials": {
    "url": "/quote/{ticker}/financials",
    "response": {
      "yearly": [
        {
          "date": 2017,
          "revenue": 79139000000,
          "earnings": 5753000000
        },
        {
          "date": 2018,
          "revenue": 79591000000,
          "earnings": 8728000000
        },
        {
          "date": 2019,
          "revenue": 77147000000,
          "earnings": 9431000000
        },
        {
          "date": 2020,
          "revenue": 73621000000,
          "earnings": 5590000000
        }
      ],
      "quarterly": [
        {
          "date": "1Q2020",
          "revenue": 17571000000,
          "earnings": 1175000000
        },
        {
          "date": "2Q2020",
          "revenue": 18121000000,
          "earnings": 1361000000
        },
        {
          "date": "3Q2020",
          "revenue": 17561000000,
          "earnings": 1698000000
        },
        {
          "date": "4Q2020",
          "revenue": 20368000000,
          "earnings": 1356000000
        }
      ]
    }
  },
  "_je_holders": {
    "url": "/quote/{ticker}/holders",
    "response": {
       "major": [
         [
           "0.13%",
           "% of Shares Held by All Insider"
         ],
         [
           "58.24%",
           "% of Shares Held by Institutions"
         ],
         [
           "58.32%",
           "% of Float Held by Institutions"
         ],
         [
           "2692",
           "Number of Institutions Holding Shares"
         ]
       ],
    }
  },
  "_je_profile": {
    "url": "/quote/{ticker}/profile",
    "response": {
    }
  },
  "_je_options": {
    "url": "/quote/{ticker}/options",
    "response": {
    }
  },
  "_je_history": {
    "url": "/quote/{ticker}/history",
    "params": {
        'interval': '1d',
        'period': 'max',
        'actions': True,
    },
    "response": {
    }
  }
}
