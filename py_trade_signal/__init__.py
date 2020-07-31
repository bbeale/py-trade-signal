#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .macd import MacdSignal
from .mfi import MfiSignal
from .vzo import VzoSignal
import pandas as pd
from pandas.errors import EmptyDataError, ParserError


class TradeSignal(object):

    def __init__(self, dataframe: pd.DataFrame):
        """Initialize the TradeSignal class

        This class uses trading instrument agnostic technical indicators from peerchemist's finta Python module: https://github.com/peerchemist/finta
        """
        self.dataframe = dataframe

        if is_valid_dataframe(self.dataframe) is False:
            try:
                validate_dataframe(self.dataframe)
            except EmptyDataError as err:
                print('[?] A valid dataframe must be provided before any calculations can be performed')
                raise err
            except ParserError as err:
                print('[!] A parsing error occurred')
                raise err

        self.macd_signal = MacdSignal()
        self.mfi_signal = MfiSignal()
        self.vzo_signal = VzoSignal()


def is_valid_dataframe(dataframe):
    raise NotImplementedError


def validate_dataframe(dataframe):
    raise NotImplementedError


class TradeSignalException(Exception):
    pass
