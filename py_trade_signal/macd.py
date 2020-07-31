#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from pandas.errors import EmptyDataError
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
            adjust: bool = True) -> bool:
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :return:
        """
        if self.df is None or len(self.df.index) < 1:
            raise EmptyDataError("[!] Dataframe cannot be None.")

        try:
            raw_macd = TA.MACD(self.df, period_fast, period_slow, signal, column, adjust)
        except TradeSignalException as error:
            raise error

        else:

            _is_negative = raw_macd["MACD"].iloc[-1] < 0
            _below_signal = raw_macd["MACD"].iloc[-1] < raw_macd["SIGNAL"].iloc[-1]
            buying = _is_negative and _below_signal

            if self.df2 is not None:
                try:
                    raw_macd2 = TA.MACD(self.df2, period_fast, period_slow, signal, column, adjust)
                except TradeSignalException as error:
                    raise error

                else:
                    _is_negative = raw_macd2["MACD"].iloc[-1] < 0
                    _below_signal = raw_macd2["MACD"].iloc[-1] < raw_macd2["SIGNAL"].iloc[-1]
                    buying = buying and _is_negative and _below_signal

            return buying

    def sell(self,
            period_fast: int = 12,
            period_slow: int = 26,
            signal: int = 9,
            column: str = "close",
            adjust: bool = True) -> bool:
        """Calculate a moving average convergence-divergence sell signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period

        :return:
        """
        if self.df is None:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")

        try:
            raw_macd = TA.MACD(self.df, period_fast, period_slow, signal, column, adjust)
        except TradeSignalException as error:
            raise error

        else:

            _is_positive = raw_macd["MACD"].iloc[-1] > 0
            _above_signal = raw_macd["MACD"].iloc[-1] > raw_macd["SIGNAL"].iloc[-1]
            selling = _is_positive and _above_signal

            if self.df2 is not None:
                try:
                    raw_macd2 = TA.MACD(self.df2, period_fast, period_slow, signal, column, adjust)
                except TradeSignalException as error:
                    raise error

                else:
                    _is_positive = raw_macd2["MACD"].iloc[-1] > 0
                    _above_signal = raw_macd2["MACD"].iloc[-1] < raw_macd2["SIGNAL"].iloc[-1]
                    selling = selling and _is_positive and _above_signal

            return selling
