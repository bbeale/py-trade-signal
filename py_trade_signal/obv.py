#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from py_trade_signal.signal_utils import SignalUtils as SU
from finta.utils import trending_up, trending_down
from finta import TA
import pandas as pd
import numpy as np


class ObvSignal(object):

    __module__ = "py_trade_signal"

    def __init__(self,
                 df: pd.DataFrame,
                 df2: pd.DataFrame = None):
        self.df = df
        self.df2 = df2

    def buy(self, column: str = "close", lookback: int = 5) -> np.bool_:

        try:
            raw_obv = TA.OBV(self.df, column)
        except TradeSignalException as error:
            raise error
        else:
            buying = trending_up(self.df["close"], lookback).iloc[-1] and trending_down(raw_obv, lookback).iloc[-1]
            if SU.is_valid_dataframe(self.df2):
                try:
                    raw_obv2 = TA.OBV(self.df2, column)
                except TradeSignalException as error:
                    raise error
                else:
                    buying = buying and trending_up(self.df2["close"], lookback).iloc[-1] and trending_down(raw_obv2, lookback).iloc[-1]

            return buying

    def sell(self, column: str = "close", lookback: int = 5) -> np.bool_:

        try:
            raw_obv = TA.OBV(self.df, column)
        except TradeSignalException as error:
            raise error
        else:
            selling = trending_down(self.df["close"], lookback).iloc[-1] and trending_up(raw_obv, lookback).iloc[-1]
            if SU.is_valid_dataframe(self.df2):
                try:
                    raw_obv2 = TA.OBV(self.df2, column)
                except TradeSignalException as error:
                    raise error
                else:
                    selling = selling and trending_down(self.df2["close"], lookback).iloc[-1] and trending_up(raw_obv2, lookback).iloc[-1]

            return selling
