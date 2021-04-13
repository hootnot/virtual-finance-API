"""Responses.

responses serve both testing purpose aswell as dynamic docstring replacement
"""
responses = {
    "_get_isin": {
        "url": "ajax/SearchController_Suggest",
        "params": {"query": "IBM"},
        "response": {"ticker": "IBM", "ISIN": "US4592001014"},
    }
}
