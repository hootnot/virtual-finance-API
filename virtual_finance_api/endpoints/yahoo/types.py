# -*- coding: utf-8 -*-

from enum import Enum


class AdjustType(str, Enum):
    auto = "auto"
    backadjust = "backadjust"


class Period(str, Enum):
    p_1d = "1d"
    p_5d = "5d"
    p_1mo = "1mo"
    p_3mo = "3mo"
    p_6mo = "6mo"
    p_1y = "1y"
    p_2y = "2y"
    p_5y = "5y"
    p_10y = "10y"
    p_ytd = "ytd"
    p_max = "max"


class Interval(str, Enum):
    i_1m = "1m"
    i_2m = "2m"
    i_5m = "5m"
    i_15m = "15m"
    i_30m = "30m"
    i_60m = "60m"
    i_90m = "90m"
    i_1h = "1h"
    i_1d = "1d"
    i_5d = "5d"
    i_1wk = "1wk"
    i_1mo = "1mo"
    i_3mo = "3mo"
