#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas.errors import EmptyDataError, ParserError

class TradeSignalException(EmptyDataError, ParserError, TypeError, ValueError, Exception):
    pass
