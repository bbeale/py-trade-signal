#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from py_trade_signal.signal_utils import SignalUtils as SU
from finta.utils import trending_up, trending_down
from finta import TA
import pandas as pd
import numpy as np


class RsiSignal(object):

    __module__ = "py_trade_signal"

    def __init__(self,
                 df: pd.DataFrame,
                 df2: pd.DataFrame = None):
        self.df = df
        self.df2 = df2

    def buy(self,
            period: int = 14,
            period2: int = 14,
            lower_bound: int = 10) -> np.bool_:
        """
        :param period:
        :param period2:
        :param lower_bound:
        :return:
        """
        try:
            raw_rsi = TA.RSI(self.df, period)
        except TradeSignalException as error:
            raise error
        else:
            buying = raw_rsi.iloc[-1] > lower_bound and raw_rsi.iloc[-2] <= lower_bound and trending_up(raw_rsi.iloc[:-2], period=int(period/2)).iloc[-1]
            if SU.is_valid_dataframe(self.df2):
                try:
                    raw_rsi2 = TA.RSI(self.df2, period2)
                except TradeSignalException as error:
                    raise error
                else:
                    buying = buying and raw_rsi2.iloc[-1] > lower_bound and raw_rsi2.iloc[-2] <= lower_bound and trending_up(raw_rsi2.iloc[:-2], period=int(period2/2)).iloc[-1]

            return buying

    def sell(self,
            period: int = 14,
            period2: int = 14,
            upper_bound: int = 90) -> np.bool_:
        """
        :param period:
        :param period2:
        :param upper_bound:
        :return:
        """
        try:
            raw_rsi = TA.RSI(self.df, period)
        except TradeSignalException as error:
            raise error
        else:
            selling = raw_rsi.iloc[-1] < upper_bound and raw_rsi.iloc[-2] >= upper_bound and trending_down(raw_rsi.iloc[:-2], period=int(period/2)).iloc[-1]
            if SU.is_valid_dataframe(self.df2):
                try:
                    raw_rsi2 = TA.RSI(self.df2, period)
                except TradeSignalException as error:
                    raise error
                else:
                    selling = selling and raw_rsi2.iloc[-1] < upper_bound and raw_rsi2.iloc[-2] >= upper_bound and trending_down(raw_rsi2.iloc[:-2], period=int(period2/2)).iloc[-1]

            return selling
