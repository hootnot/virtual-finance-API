# -*- coding: utf-8 -*-

import pytest
from virtual_finance_api.generic import isin


def test__isin():
    """ISINCode."""
    ic = isin.ISINCode("BE0003788057")
    assert (
        ic.country == "BE"
        and ic.NSIN == "000378805"
        and ic.code == "BE0003788057"
        and ic.passed is True
        and str(ic)
        == str(
            {
                "ISIN": "BE0003788057",
                "COUNTRY": "BE",
                "NSIN": "000378805",
                "CHKSUM": True,
            }
        )
    )


def test__isin_err():
    """ISINCode."""
    code = "E0003788057"
    with pytest.raises(ValueError) as err:
        isin.ISINCode(code)
    assert code in str(err.value)
