#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from pandas.errors import EmptyDataError
from finta import TA
import pandas as pd


class MfiSignal(object):

    __module__ = "py_trade_signal"

    def __init__(self,
                 df: pd.DataFrame,
                 df2: pd.DataFrame = None):
        self.df = df
        self.df2 = df2

    def buy(self, period: int = 14) -> bool:
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :return:
        """
        if self.df is None or len(self.df.index) < 1:
            raise EmptyDataError("[!] Dataframe cannot be None.")

        try:
            raw_mfi = TA.MFI(self.df, period)
        except TradeSignalException as error:
            raise error
        else:
            buying = raw_mfi.iloc[-1] > 10 and min(raw_mfi.iloc[-4:-2]) <= 10
            if self.df2 is not None:
                try:
                    raw_mfi2 = TA.MFI(self.df2, period)
                except TradeSignalException as error:
                    raise error
                else:
                    buying = buying and raw_mfi2.iloc[-1] > 10 and min(raw_mfi2.iloc[-4:-2]) <= 10

            return buying

    def sell(self, period: int = 14) -> bool:
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :return:
        """
        if self.df is None or len(self.df.index) < 1:
            raise EmptyDataError("[!] Dataframe cannot be None.")

        try:
            raw_mfi = TA.MFI(self.df, period)
        except TradeSignalException as error:
            raise error
        else:
            selling = raw_mfi.iloc[-1] > 90 and min(raw_mfi.iloc[-4:-2]) <= 90
            if self.df2 is not None:
                try:
                    raw_mfi2 = TA.MFI(self.df2, period)
                except TradeSignalException as error:
                    raise error
                else:
                    selling = selling and raw_mfi2.iloc[-1] > 90 and min(raw_mfi2.iloc[-4:-2]) <= 90

            return selling
