import unittest
from virtual_finance_api.exceptions import (  # noqa F401
    ConversionHookError,
    VirtualFinanceAPIError
)
from virtual_finance_api.generic import isin


try:
    from parameterized import parameterized  # noqa F401

except Exception as err:  # noqa F841
    print("*** Please install 'parameterized' to run these tests ***")
    exit(0)


client = None
API_URL = 'https://test.com'


class TestGeneric(unittest.TestCase):
    """Tests regarding the 'generic' module."""

    def setUp(self):
        """setup for all tests."""
        global client
        # self.maxDiff = None
        try:
            # client = Client(headers={"Content-Type": "application/json"})
            # api.api_url = 'https://test.com'
            pass
        except Exception as e:
            print("%s" % e)
            exit(0)

    def test__isin(self):
        """ISINCode."""
        ic = isin.ISINCode('BE0003788057')
        self.assertTrue(ic.country == 'BE' and
                        ic.NSIN == '000378805' and
                        ic.code == 'BE0003788057' and
                        ic.passed is True and
                        str(ic) == str({'ISIN': 'BE0003788057',
                                        'COUNTRY': 'BE',
                                        'NSIN': '000378805',
                                        'CHKSUM': True}))

    def test__isin_err(self):
        """ISINCode."""
        code = 'E0003788057'
        with self.assertRaises(ValueError) as err:
            isin.ISINCode(code)
        self.assertTrue(code in str(err.exception))
