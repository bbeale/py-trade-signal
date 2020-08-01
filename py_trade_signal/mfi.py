#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal import TradeSignalException, is_valid_dataframe
from finta.utils import trending_up, trending_down
from finta import TA
import pandas as pd


class MfiSignal(object):

    __module__ = "py_trade_signal"

    def __init__(self,
                 df: pd.DataFrame,
                 df2: pd.DataFrame = None):
        self.df = df
        self.df2 = df2

    def buy(self, period: int = 14, period2: int = 14) -> bool:
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :param period:
        :param period2:
        :return:
        """
        try:
            raw_mfi = TA.MFI(self.df, period)
        except TradeSignalException as error:
            raise error
        else:
            buying = raw_mfi.iloc[-1] > 10 and raw_mfi.iloc[-2] <= 10 and trending_up(raw_mfi.iloc[:-2], period=int(period/2))
            if is_valid_dataframe(self.df2):
                try:
                    raw_mfi2 = TA.MFI(self.df2, period2)
                except TradeSignalException as error:
                    raise error
                else:
                    buying = buying and raw_mfi2.iloc[-1] > 10 and raw_mfi2.iloc[-2] <= 10 and trending_up(raw_mfi2.iloc[:-2], period=int(period2/2))

            return buying

    def sell(self, period: int = 14, period2: int = 14) -> bool:
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :param period:
        :param period2:
        :return:
        """
        try:
            raw_mfi = TA.MFI(self.df, period)
        except TradeSignalException as error:
            raise error
        else:
            selling = raw_mfi.iloc[-1] < 90 and raw_mfi.iloc[-2] >= 90 and trending_down(raw_mfi.iloc[:-2], period=int(period/2))
            if is_valid_dataframe(self.df2):
                try:
                    raw_mfi2 = TA.MFI(self.df2, period)
                except TradeSignalException as error:
                    raise error
                else:
                    selling = selling and raw_mfi2.iloc[-1] < 90 and raw_mfi2.iloc[-2] >= 90 and trending_down(raw_mfi2.iloc[:-2], period=int(period2/2))

            return selling
