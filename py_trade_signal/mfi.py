#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from pandas.errors import EmptyDataError
from finta import TA


class MfiSignal:

    __module__ = "py_trade_signal"

    def __init__(self):
        pass

    @staticmethod
    def buy(dataframe):
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period
        :param dataframe:
        :return:
        """
        if dataframe is None or len(list(dataframe.keys())) < 1:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")
        try:
            raw_mfi = TA.MFI(dataframe)
        except TradeSignalException as error:
            raise error
        else:
            return raw_mfi.iloc[-1] > 10 and min(raw_mfi.iloc[-4:-2]) <= 10

    @staticmethod
    def sell(dataframe):
        """Calculate a moving average convergence-divergence buy signal from a bullish signal crossover.

        An optional second dataframe can be used to calculate the signal for a different time period
        :param dataframe:
        :return:
        """
        if dataframe is None or len(list(dataframe.keys())) < 1:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")
        try:
            raw_mfi = TA.MFI(dataframe)
        except TradeSignalException as error:
            raise error
        else:
            return raw_mfi.iloc[-1] > 90 and min(raw_mfi.iloc[-4:-2]) <= 90
