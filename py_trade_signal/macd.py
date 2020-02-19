#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from pandas.errors import EmptyDataError
from finta import TA


class MacdSignal:

    __module__ = "py_trade_signal"

    def __init__(self):
        pass

    @staticmethod
    def buy(dataframe, dataframe2=None):
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period
        :param dataframe:
        :param dataframe2:
        :return:
        """
        if dataframe is None:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")

        try:
            raw_macd = TA.MACD(dataframe)
        except TradeSignalException as error:
            raise error

        else:

            _is_negative = raw_macd["MACD"].iloc[-1] < 0
            _previous_below_signal = min(raw_macd["MACD"].iloc[-4:-2]) < raw_macd["SIGNAL"].iloc[-1]
            _current_above_signal = raw_macd["MACD"].iloc[-1] > raw_macd["SIGNAL"].iloc[-1]
            _bullish_cross = _previous_below_signal and _current_above_signal

            signal = _is_negative and _bullish_cross

            if dataframe2 is not None:
                try:
                    raw_macd2 = TA.MACD(dataframe2)
                except TradeSignalException as error:
                    raise error

                else:
                    _is_negative = raw_macd2["MACD"].iloc[-1] < 0
                    _previous_below_signal = min(raw_macd2["MACD"].iloc[-4:-2]) < raw_macd2["SIGNAL"].iloc[-1]
                    _current_above_signal = raw_macd2["MACD"].iloc[-1] > raw_macd2["SIGNAL"].iloc[-1]
                    _bullish_cross = _previous_below_signal and _current_above_signal

                    signal = signal and _is_negative and _bullish_cross

            return signal

    @staticmethod
    def sell(dataframe, dataframe2=None):
        """Calculate a moving average convergence-divergence sell signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period
        :param dataframe:
        :param dataframe2:
        :return:
        """
        if not dataframe or dataframe is None:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")

        try:
            raw_macd = TA.MACD(dataframe)
        except TradeSignalException as error:
            raise error

        else:

            _is_positive = raw_macd["MACD"].iloc[-1] > 0
            _previous_above_signal = min(raw_macd["MACD"].iloc[-4:-2]) > raw_macd["SIGNAL"].iloc[-1]
            _current_below_signal = raw_macd["MACD"].iloc[-1] < raw_macd["SIGNAL"].iloc[-1]
            _bearish_cross = _previous_above_signal and _current_below_signal
            signal = _is_positive and _bearish_cross

            if dataframe2 is not None:
                try:
                    raw_macd2 = TA.MACD(dataframe2)
                except TradeSignalException as error:
                    raise error

                else:
                    _is_positive = raw_macd2["MACD"].iloc[-1] > 0
                    _previous_above_signal = min(raw_macd2["MACD"].iloc[-4:-2]) > raw_macd2["SIGNAL"].iloc[-1]
                    _current_below_signal = raw_macd2["MACD"].iloc[-1] < raw_macd2["SIGNAL"].iloc[-1]
                    _bearish_cross = _previous_above_signal and _current_below_signal

                    signal = signal and _is_positive and _bearish_cross

            return signal
