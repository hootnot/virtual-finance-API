# -*- coding: utf-8 -*-


class ISINCode:
    def __init__(self, code):
        self._code = code
        self._passed = False
        self.verify()
        self._country = self._code[0:2]
        self._NSIN = self._code[2:11]

    def verify(self):
        if not self.code or len(self._code) > 12:
            raise ValueError(self._code)

        _l = []
        for c in self._code:
            _l.append(str(int((ord(c) - 55) if c not in
                      [str(_) for _ in range(10)] else c)))

        _l = ''.join(_l)
        ctrl = int(_l[-1])

        even = _l[:-1][0::2]
        odd = _l[:-1][1::2]
        if len(even) > len(odd):
            odd, even = even, odd

        even = [int(x) for x in even]
        _even = [int(x) for x in ''.join([str(y) for y in even])]

        Xodd = [int(x)*2 for x in odd]
        _odd = [int(x) for x in ''.join([str(y) for y in Xodd])]
        chksum = sum(_even + _odd)

        self._passed = ((chksum + ctrl) % 10 == 0)
        if not self._passed:
            raise ValueError(self.code)

    def __str__(self):
        return str({'ISIN': self.code,
                    'COUNTRY': self.country,
                    'NSIN': self.NSIN,
                    'CHKSUM': self.passed})

    @property
    def code(self):
        return self._code

    @property
    def country(self):
        return self._country

    @property
    def NSIN(self):
        return self._NSIN

    @property
    def passed(self):
        return self._passed
