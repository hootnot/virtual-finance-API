# -*- coding: utf-8 -*-
"""Exceptions."""


class VirtualFinanceAPIError(Exception):
    """Generic error class.
    In case of HTTP response codes >= 400 this class can be used
    to raise an exception representing that error.
    """

    def __init__(self, code: int, msg: str):
        """Instantiate a VirtualFinanceError.

        Parameters
        ----------
        code : int
            the HTTP-code of the response
        msg : str
            the message returned with the response
        """
        super(VirtualFinanceAPIError, self).__init__(msg)
        self.code = code


class ConversionHookError(Exception):
    def __init__(self, code: int, msg: str):
        super(ConversionHookError, self).__init__(msg)
        self.code = code
