#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal import TradeSignalException, is_valid_dataframe
from finta.utils import trending_up, trending_down
from finta import TA
import pandas as pd


class MacdSignal(object):

    __module__ = "py_trade_signal"

    def __init__(self,
                 df: pd.DataFrame,
                 df2: pd.DataFrame = None):
        self.df = df
        self.df2 = df2

    def buy(self,
            period_fast: int = 12,
            period_slow: int = 26,
            signal: int = 9,
            column: str = "close",
            adjust: bool = True,
            period_fast2: int = 12,
            period_slow2: int = 26,
            signal2: int = 9,
            column2: str = "close",
            adjust2: bool = True) -> bool:
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :param period_fast:
        :param period_slow:
        :param signal:
        :param column:
        :param adjust:
        :param period_fast2:
        :param period_slow2:
        :param signal2:
        :param column2:
        :param adjust2:
        :return bool:
        """

        try:
            raw_macd = TA.MACD(self.df, period_fast, period_slow, signal, column, adjust)
        except TradeSignalException as error:
            raise error

        else:

            _is_negative = raw_macd["MACD"].iloc[-1] < 0
            _below_signal = raw_macd["MACD"].iloc[-1] < raw_macd["SIGNAL"].iloc[-1]
            _trending_up = trending_up(raw_macd["MACD"].iloc[:-2], period=int(period_fast/2))
            buying = _is_negative and _below_signal and _trending_up

            if is_valid_dataframe(self.df2):
                try:
                    raw_macd2 = TA.MACD(self.df2, period_fast2, period_slow2, signal2, column2, adjust2)
                except TradeSignalException as error:
                    raise error

                else:
                    _is_negative2 = raw_macd2["MACD"].iloc[-1] < 0
                    _below_signal2 = raw_macd2["MACD"].iloc[-1] < raw_macd2["SIGNAL"].iloc[-1]
                    _trending_up2 = trending_up(raw_macd2["MACD"].iloc[:-2], period=int(period_fast2/2))
                    buying = buying and _is_negative2 and _below_signal2 and _trending_up2

            return buying

    def sell(self,
            period_fast: int = 12,
            period_slow: int = 26,
            signal: int = 9,
            column: str = "close",
            adjust: bool = True,
            period_fast2: int = 12,
            period_slow2: int = 26,
            signal2: int = 9,
            column2: str = "close",
            adjust2: bool = True) -> bool:
        """Calculate a moving average convergence-divergence sell signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period
        :param period_fast:
        :param period_slow:
        :param signal:
        :param column:
        :param adjust:
        :param period_fast2:
        :param period_slow2:
        :param signal2:
        :param column2:
        :param adjust2:
        :return bool:
        """
        try:
            raw_macd = TA.MACD(self.df, period_fast, period_slow, signal, column, adjust)
        except TradeSignalException as error:
            raise error

        else:

            _is_positive = raw_macd["MACD"].iloc[-1] > 0
            _above_signal = raw_macd["MACD"].iloc[-1] > raw_macd["SIGNAL"].iloc[-1]
            _trending_down = trending_down(raw_macd["MACD"].iloc[:-2], period=int(period_fast/2))
            selling = _is_positive and _above_signal and _trending_down

            if self.df2 is not None:
                try:
                    raw_macd2 = TA.MACD(self.df2, period_fast2, period_slow2, signal2, column2, adjust2)
                except TradeSignalException as error:
                    raise error

                else:
                    _is_positive2 = raw_macd2["MACD"].iloc[-1] > 0
                    _above_signal2 = raw_macd2["MACD"].iloc[-1] < raw_macd2["SIGNAL"].iloc[-1]
                    _trending_down2 = trending_down(raw_macd2["MACD"].iloc[:-2], period=int(period_fast2/2))
                    selling = selling and _is_positive2 and _above_signal2 and _trending_down2

            return selling
