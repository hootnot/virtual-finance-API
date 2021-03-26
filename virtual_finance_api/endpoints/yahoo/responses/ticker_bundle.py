"""Responses.

responses serve both testing purpose aswell as dynamic docstring replacement
"""
responses = {
  "_yh_holders": {
    "url": "/quote/{ticker}/holders",
    "response": {
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
          "2": 9017292,
          "3": 8074523,
          "4": 7327901,
          "5": 6640777,
          "6": 5998301,
          "7": 5480612,
          "8": 4487000,
          "9": 4463676
        },
        "Date Reported": {
          "0": "Dec 30, 2020",
          "1": "Dec 30, 2020",
          "2": "Jan 30, 2021",
          "3": "Jan 30, 2021",
          "4": "Dec 30, 2020",
          "5": "Jan 30, 2021",
          "6": "Dec 30, 2020",
          "7": "Jan 30, 2021",
          "8": "Dec 30, 2020",
          "9": "Nov 29, 2020"
        },
        "% Out": {
          "0": "2.81%",
          "1": "2.00%",
          "2": "1.01%",
          "3": "0.90%",
          "4": "0.82%",
          "5": "0.74%",
          "6": "0.67%",
          "7": "0.61%",
          "8": "0.50%",
          "9": "0.50%"
        },
        "Value": {
          "0": 3160671826,
          "1": 2247566000,
          "2": 1074049650,
          "3": 961756434,
          "4": 922436177,
          "5": 790982948,
          "6": 755066129,
          "7": 652795695,
          "8": 564823560,
          "9": 551353259
        }
      }
    }
  },
  "_yh_profile": {
    "url": "/quote/{ticker}",
    "response": {
      "defaultKeyStatistics": {
        "annualHoldingsTurnover": None,
        "enterpriseToRevenue": 2.282,
        "beta3Year": None,
        "profitMargins": 0.07593,
        "enterpriseToEbitda": 10.994,
        "52WeekChange": 0.36013508,
        "morningStarRiskRating": None,
        "forwardEps": 12.08,
        "revenueQuarterlyGrowth": None,
        "sharesOutstanding": 893593984,
        "fundInceptionDate": None,
        "annualReportExpenseRatio": None,
        "totalAssets": None,
        "bookValue": 23.074,
        "sharesShort": 30005072,
        "sharesPercentSharesOut": 0.0336,
        "___": "              /// and a lot more ///",
        "fundFamily": None,
        "lastFiscalYearEnd": 1609372800,
        "heldPercentInstitutions": 0.58584,
        "netIncomeToCommon": 5501000192,
        "trailingEps": 6.233,
        "lastDividendValue": 1.63,
        "SandP52WeekChange": 0.652609,
        "priceToBook": 5.6570168,
        "heldPercentInsiders": 0.0012800001,
        "nextFiscalYearEnd": 1672444800,
        "yield": None,
        "impliedSharesOutstanding": None,
        "category": None,
        "fiveYearAverageReturn": None
      },
      "details": None,
      "summaryProfile": {
        "zip": "10504",
        "sector": "Technology",
        "fullTimeEmployees": 345900,
        "city": "Armonk",
        "___": "              /// and a lot more ///",
        "phone": "914 499 1900",
        "state": "NY",
        "country": "United States",
        "companyOfficers": [],
        "website": "http://www.ibm.com",
        "maxAge": 86400,
        "address1": "One New Orchard Road",
        "industry": "Information Technology Services"
      },
      "recommendationTrend": {
        "trend": [
          {
            "period": "0m",
            "strongBuy": 4,
            "buy": 3,
            "hold": 15,
            "sell": 3,
            "strongSell": 0
          },
          {
            "period": "-1m",
            "strongBuy": 4,
            "buy": 1,
            "hold": 10,
            "sell": 2,
            "strongSell": 0
          }
        ]
      },
      "financialsTemplate": {
        "code": "N",
        "maxAge": 1
      },
      "earnings": {
        "maxAge": 86400,
        "earningsChart": {
          "quarterly": [
            {
              "date": "1Q2020",
              "actual": 1.84,
              "estimate": 1.79
            },
            {
              "date": "2Q2020",
              "actual": 2.18,
              "estimate": 2.07
            }
          ]
        }
      }
    }
  },
  "_yh_financials": {
    "url": "/quote/{ticker}/financials",
    "response": {
      "financialsTemplate": {
        "code": "N",
        "maxAge": 1
      },
      "cashflowStatementHistory": {
        "cashflowStatements": [
          {
            "investments": -628000000,
            "changeToLiabilities": 138000000,
            "totalCashflowsFromInvestingActivities": -3028000000,
            "netBorrowings": -3714000000,
            "totalCashFromFinancingActivities": -9721000000,
            "changeToOperatingActivities": 3023000000,
            "netIncome": 5590000000,
            "changeInCash": 5361000000,
            "endDate": 1609372800,
            "repurchaseOfStock": -302000000,
            "effectOfExchangeRate": -87000000,
            "totalCashFromOperatingActivities": 18197000000,
            "depreciation": 6695000000,
            "dividendsPaid": -5797000000,
            "changeToInventory": -209000000,
            "changeToAccountReceivables": 5297000000,
            "otherCashflowsFromFinancingActivities": 92000000,
            "maxAge": 1,
            "changeToNetincome": -2337000000,
            "capitalExpenditures": -2618000000
          },
          {
            "investments": 268000000,
            "changeToLiabilities": -503000000,
            "totalCashflowsFromInvestingActivities": -26936000000,
            "netBorrowings": 16284000000,
            "totalCashFromFinancingActivities": 9042000000,
            "changeToOperatingActivities": 1159000000,
            "netIncome": 9431000000,
            "changeInCash": -3290000000,
            "endDate": 1577750400,
            "repurchaseOfStock": -1633000000,
            "effectOfExchangeRate": -167000000,
            "totalCashFromOperatingActivities": 14770000000,
            "depreciation": 6059000000,
            "dividendsPaid": -5707000000,
            "changeToInventory": 67000000,
            "changeToAccountReceivables": 502000000,
            "otherCashflowsFromFinancingActivities": 98000000,
            "maxAge": 1,
            "changeToNetincome": -1945000000,
            "capitalExpenditures": -2286000000
          },
          {
            "...": "         /// and a lot more data ///"
          }
        ]
      }
    }
  },
  "_yh_options": {
    "url": "v7/finance/options/{ticker}",
    "response": {
     "optionChain": {
       "result": [
         {
           "underlyingSymbol": "IBM",
           "expirationDates": [
             1616716800,
             1617235200,
             1617926400,
             1618531200,
             1619136000,
             1619740800,
             1621555200,
             1623974400,
             1626393600,
             1631836800,
             1634256000,
             1642723200,
             1674172800
           ],
           "strikes": [
             75.0,
             80.0,
             90.0,
             95.0,
             100.0,
             105.0,
             107.0,
             108.0,
             109.0,
             110.0,
             111.0,
             112.0,
             113.0,
             114.0,
             115.0,
             116.0,
             117.0,
             118.0,
             119.0,
             120.0,
             121.0,
             122.0,
             123.0,
             124.0,
             125.0,
             126.0,
             127.0,
             128.0,
             129.0,
             130.0,
             131.0,
             132.0,
             133.0,
             134.0,
             135.0,
             136.0,
             137.0,
             138.0,
             139.0,
             140.0,
             141.0,
             145.0,
             150.0
           ],
           "hasMiniOptions": False,
           "quote": {
             "language": "en-US",
             "region": "US",
             "quoteType": "EQUITY",
             "quoteSourceName": "Nasdaq Real Time Price",
             "triggerable": True,
             "currency": "USD",
             "firstTradeDateMilliseconds": -252322200000,
             "priceHint": 2,
             "postMarketChangePercent": -0.183842,
             "postMarketTime": 1616451187,
             "postMarketPrice": 130.31,
             "postMarketChange": -0.240005,
             "regularMarketChange": 1.65001,
             "regularMarketChangePercent": 1.28007,
             "regularMarketTime": 1616443202,
             "regularMarketPrice": 130.55,
             "regularMarketDayHigh": 130.715,
             "regularMarketDayRange": "127.89 - 130.715",
             "regularMarketDayLow": 127.89,
             "regularMarketVolume": 3827442,
             "regularMarketPreviousClose": 128.9,
             "bid": 130.19,
             "ask": 130.72,
             "bidSize": 9,
             "askSize": 31,
             "fullExchangeName": "NYSE",
             "financialCurrency": "USD",
             "regularMarketOpen": 128.5,
             "averageDailyVolume3Month": 6592085,
             "averageDailyVolume10Day": 5328433,
             "fiftyTwoWeekLowChange": 39.990005,
             "fiftyTwoWeekLowChangePercent": 0.44158575,
             "fiftyTwoWeekRange": "90.56 - 135.88",
             "fiftyTwoWeekHighChange": -5.330002,
             "fiftyTwoWeekHighChangePercent": -0.039225798,
             "fiftyTwoWeekLow": 90.56,
             "fiftyTwoWeekHigh": 135.88,
             "dividendDate": 1615334400,
             "earningsTimestamp": 1618862400,
             "earningsTimestampStart": 1618862400,
             "earningsTimestampEnd": 1618862400,
             "trailingAnnualDividendRate": 6.51,
             "trailingPE": 20.944971,
             "trailingAnnualDividendYield": 0.05050427,
             "epsTrailingTwelveMonths": 6.233,
             "epsForward": 12.08,
             "epsCurrentYear": 11.02,
             "priceEpsCurrentYear": 11.8466425,
             "sharesOutstanding": 893593984,
             "bookValue": 23.074,
             "fiftyDayAverage": 122.95,
             "fiftyDayAverageChange": 7.600006,
             "fiftyDayAverageChangePercent": 0.061813798,
             "twoHundredDayAverage": 122.19059,
             "twoHundredDayAverageChange": 8.359413,
             "twoHundredDayAverageChangePercent": 0.06841291,
             "marketCap": 116658700288,
             "forwardPE": 10.807119,
             "priceToBook": 5.6578836,
             "sourceInterval": 15,
             "exchangeDataDelayedBy": 0,
             "marketState": "POST",
             "exchange": "NYQ",
             "shortName": "International Business Machines",
             "longName": "International Business Machines Corporation",
             "messageBoardId": "finmb_112350",
             "exchangeTimezoneName": "America/New_York",
             "exchangeTimezoneShortName": "EDT",
             "gmtOffSetMilliseconds": -14400000,
             "market": "us_market",
             "esgPopulated": False,
             "tradeable": False,
             "displayName": "IBM",
             "symbol": "IBM"
           },
           "options": [
             {
               "expirationDate": 1616716800,
               "hasMiniOptions": False,
               "calls": [
                 {
                   "contractSymbol": "IBM210326C00100000",
                   "strike": 100.0,
                   "currency": "USD",
                   "lastPrice": 20.47,
                   "change": 0.0,
                   "percentChange": 0.0,
                   "volume": 5,
                   "openInterest": 5,
                   "bid": 28.9,
                   "ask": 31.95,
                   "contractSize": "REGULAR",
                   "expiration": 1616716800,
                   "lastTradeDate": 1614013862,
                   "impliedVolatility": 1.890625546875,
                   "inTheMoney": True
                 },
                 {
                   "contractSymbol": "IBM210326C00105000",
                   "strike": 105.0,
                   "currency": "USD",
                   "lastPrice": 16.0,
                   "change": 0.0,
                   "percentChange": 0.0,
                   "openInterest": 2,
                   "bid": 24.75,
                   "ask": 26.15,
                   "contractSize": "REGULAR",
                   "expiration": 1616716800,
                   "lastTradeDate": 1614878873,
                   "impliedVolatility": 1.2959019580078124,
                   "inTheMoney": True
                 },
                 {
                   "contractSymbol": "IBM210326C00107000",
                   "...": "        /// and a lot more data ///",
                 }
               ],
               "puts": [
                 {
                    "...": "        /// and a lot more data ///",
                 }
               ]
             }
           ]
         }
       ],
       "error": None
     }
    }
  }
}
