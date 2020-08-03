#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .exception import TradeSignalException
from .signal_utils import SignalUtils
from .macd import MacdSignal
from .mfi import MfiSignal
from .obv import ObvSignal
from .rsi import RsiSignal
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

        if not SignalUtils.is_valid_dataframe(self.dataframe):
            raise TradeSignalException("[!] Signal calculations require at least one valid dataframe.")

        self.macd = MacdSignal(self.dataframe, self.dataframe2)
        self.mfi = MfiSignal(self.dataframe, self.dataframe2)
        self.obv = ObvSignal(self.dataframe, self.dataframe2)
        self.rsi = RsiSignal(self.dataframe, self.dataframe2)
        self.vzo = VzoSignal(self.dataframe, self.dataframe2)
