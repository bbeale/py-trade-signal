#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.exception import TradeSignalException
from pandas.errors import EmptyDataError
from finta import TA


class VzoSignal:

    __module__ = "py_trade_signal"

    def __init__(self):
        pass

    @staticmethod
    def buy(dataframe):
        """Bullish buy signal calculation based on volume zone oscillator (VZO).

        The flag is generated based on a number of conditional statements generated from technical indicators.
        The basic buy rule is to buy when a bullish crossover happens -- the VZO crossing over the -40% line

        Along with the bullish crossover, we can use a 14 period average directional index (ADX), directional
        movement index (DMI), and a 60 period EMA to confirm the trend. We do this by making sure the ADX is
        at least 20, the DMI is trending upward (DI+ > DI-) and that the close price has crossed over the 60 day EMA.

        An example usage might look like:

        if vzo.buy() and some_other_indicator():
            execute_buy_order()

        :param dataframe:
        :return:
        """
        if dataframe is None or len(list(dataframe.keys())) < 1:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")
        try:
            # grab the indicators we need (VZO, ADX, DMI, EMA) for this signal
            vzo = TA.VZO(dataframe)
            adx = TA.ADX(dataframe)
            dmi = TA.DMI(dataframe)
            ema = TA.EMA(dataframe, period=60)
        except TradeSignalException as error:
            raise error
        else:
            _vzo_bullish_cross = vzo.iloc[-1] > -40 and vzo.iloc[-4:-2].mean() <= -40
            _adx_trending = adx.iloc[-1] > 20
            _dmi_positive = dmi["DI+"] > dmi["DI-"]
            _ema_bullish_cross = dataframe["close"].iloc[-1] > ema.iloc[-1] and dataframe["close"].iloc[-4:-2].mean() < ema.iloc[-4:-2].mean()
            return _vzo_bullish_cross and (_adx_trending or _dmi_positive) and _ema_bullish_cross

    @staticmethod
    def sell(dataframe):
        """Bearish sell signal calculation based on volume zone oscillator (VZO).

        The flag is generated based on a number of conditional statements generated from technical indicators.
        The basic buy rule is to sell when a bearish crossover happens -- the VZO crossing below the 40% line

        Along with the bearish crossover, we can use a 14 period average directional index (ADX), directional
        movement index (DMI), and a 60 period EMA to confirm the trend. We do this by making sure the close
        price has crossed below the 60 day EMA and either an ADX less than 20 or a downward DMI (DI- > DI+).

        An example usage might look like:

        if vzo.sell() or difference(current_price, entry_price) == profit_target:
            execute_sell_order()

        :param dataframe:
        :return:
        """
        if dataframe is None or len(list(dataframe.keys())) < 1:
            raise EmptyDataError("[!] Dataframe is empty or not valid.")
        try:
            # grab the indicators we need (VZO, ADX, DMI, EMA) for this signal
            vzo = TA.VZO(dataframe)
            adx = TA.ADX(dataframe)
            dmi = TA.DMI(dataframe)
            ema = TA.EMA(dataframe, period=60)
        except TradeSignalException as error:
            raise error
        else:
            _vzo_bearish_cross = vzo.iloc[-1] < 40 and vzo.iloc[-4:-2].mean() >= 40
            _adx_trending = adx.iloc[-1] < 20
            _dmi_negative = dmi["DI-"] > dmi["DI+"]
            _ema_bearish_cross = dataframe["close"].iloc[-1] < ema.iloc[-1] and dataframe["close"].iloc[-4:-2].mean() > ema.iloc[-4:-2].mean()
            return _vzo_bearish_cross and (_adx_trending or _dmi_negative) and _ema_bearish_cross


