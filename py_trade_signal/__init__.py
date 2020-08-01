#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .macd import MacdSignal
from .mfi import MfiSignal
from .vzo import VzoSignal
import pandas as pd


class TradeSignal(object):

    def __init__(self,
                 dataframe: pd.DataFrame,
                 dataframe2: pd.DataFrame = None):
        """Initialize the TradeSignal class

        This class uses trading instrument agnostic technical indicators from peerchemist's finta Python module: https://github.com/peerchemist/finta
        """
        self.dataframe = dataframe
        self.dataframe2 = dataframe2

        if not is_valid_dataframe(self.dataframe):
            raise TradeSignalException("[!] Signal calculations require at least one valid dataframe.")

        self.macd_signal = MacdSignal(self.dataframe, self.dataframe2)
        self.mfi_signal = MfiSignal(self.dataframe, self.dataframe2)
        self.vzo_signal = VzoSignal(self.dataframe, self.dataframe2)


def is_valid_dataframe(dataframe: pd.DataFrame) -> bool:
    return dataframe is not None and len(dataframe.index) > 0


class TradeSignalException(Exception):
    pass
