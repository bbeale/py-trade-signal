#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal import TradeSignalException, is_valid_dataframe
from finta import TA
from finta.utils import trending_up, trending_down
import pandas as pd


class VzoSignal(object):

    __module__ = "py_trade_signal"

    def __init__(self,
                 df: pd.DataFrame,
                 df2: pd.DataFrame = None):
        self.df = df
        self.df2 = df2

    def buy(self,
            period: int = 14,
            ema_period: int = 60,
            column: str = "close",
            adjust: bool = True,
            period2: int = 14,
            ema_period2: int = 60,
            column2: str = "close",
            adjust2: bool = True) -> bool:
        """Bullish buy signal calculation based on volume zone oscillator (VZO).

        The flag is generated based on a number of conditional statements generated from technical indicators.
        The basic buy rule is to buy when a bullish crossover happens -- the VZO crossing over the -40% line

        Along with the bullish crossover, we can use a 14 period average directional index (ADX), directional
        movement index (DMI), and a 60 period EMA to confirm the trend. We do this by making sure the ADX is
        at least 20, the DMI is trending upward (DI+ > DI-) and that the close price has crossed over the 60 day EMA.

        An example usage might look like:

        if vzo.buy() and some_other_indicator():
            execute_buy_order()

        :param period:
        :param ema_period:
        :param column:
        :param adjust:
        :param period2:
        :param ema_period2:
        :param column2:
        :param adjust2:
        :return bool:
        """
        try:
            # grab the indicators we need (VZO, ADX, DMI, EMA) for this signal
            vzo = TA.VZO(self.df, period, column, adjust)
            adx = TA.ADX(self.df, period, adjust)
            dmi = TA.DMI(self.df, period, adjust)
            ema = TA.EMA(self.df, ema_period, column, adjust)
        except TradeSignalException as error:
            raise error
        else:
            _vzo_bullish_cross = vzo.iloc[-1] > -40 and trending_up(vzo.iloc[:-2], period=int(period/2))
            _adx_trending = adx.iloc[-1] > 20
            _dmi_positive = dmi["DI+"] > dmi["DI-"]
            _ema_bullish_cross = self.df["close"].iloc[-1] > ema.iloc[-1] and \
                trending_up(self.df["close"].iloc[:-2], period=int(period/2))
            buying = _vzo_bullish_cross and \
                (_adx_trending or _dmi_positive) and \
                _ema_bullish_cross

            if is_valid_dataframe(self.df2):
                try:
                    # grab the indicators we need (VZO, ADX, DMI, EMA) for this signal
                    vzo2 = TA.VZO(self.df2, period2, column2, adjust2)
                    adx2 = TA.ADX(self.df2, period2, adjust2)
                    dmi2 = TA.DMI(self.df2, period2, adjust2)
                    ema2 = TA.EMA(self.df2, ema_period2, column2, adjust2)
                except TradeSignalException as error:
                    raise error
                else:
                    _vzo_bullish_cross2 = vzo2.iloc[-1] > -40 and trending_up(vzo2.iloc[:-2], period=int(period2/2))
                    _adx_trending2 = adx2.iloc[-1] > 20
                    _dmi_positive2 = dmi2["DI+"] > dmi2["DI-"]
                    _ema_bullish_cross2 = self.df2["close"].iloc[-1] > ema2.iloc[-1] and \
                        trending_up(self.df2["close"].iloc[:-2], period=int(period2/2))
                    buying = buying and _vzo_bullish_cross2 and (_adx_trending2 or _dmi_positive2) and _ema_bullish_cross2

            return buying

    def sell(self,
             period: int = 14,
             ema_period: int = 60,
             column: str = "close",
             adjust: bool = True,
             period2: int = 14,
             ema_period2: int = 60,
             column2: str = "close",
             adjust2: bool = True) -> bool:
        """Bearish sell signal calculation based on volume zone oscillator (VZO).

        The flag is generated based on a number of conditional statements generated from technical indicators.
        The basic buy rule is to sell when a bearish crossover happens -- the VZO crossing below the 40% line

        Along with the bearish crossover, we can use a 14 period average directional index (ADX), directional
        movement index (DMI), and a 60 period EMA to confirm the trend. We do this by making sure the close
        price has crossed below the 60 day EMA and either an ADX less than 20 or a downward DMI (DI- > DI+).

        An example usage might look like:

        if vzo.sell() or difference(current_price, entry_price) == profit_target:
            execute_sell_order()

        :param period:
        :param ema_period:
        :param column:
        :param adjust:
        :param period2:
        :param ema_period2:
        :param column2:
        :param adjust2:
        :return:
        """
        try:
            # grab the indicators we need (VZO, ADX, DMI, EMA) for this signal
            vzo = TA.VZO(self.df, period, column, adjust)
            adx = TA.ADX(self.df, period, adjust)
            dmi = TA.DMI(self.df, period, adjust)
            ema = TA.EMA(self.df, ema_period, column, adjust)
        except TradeSignalException as error:
            raise error
        else:
            _vzo_bearish_cross = vzo.iloc[-1] < 40 and trending_down(vzo.iloc[:-2], period=int(period/2))
            _adx_trending = adx.iloc[-1] < 20
            _dmi_negative = dmi["DI-"] > dmi["DI+"]
            _ema_bearish_cross = self.df["close"].iloc[-1] < ema.iloc[-1] and \
                trending_down(self.df["close"].iloc[:-2], period=int(period/2))
            selling = _vzo_bearish_cross and (_adx_trending or _dmi_negative) and _ema_bearish_cross

            if is_valid_dataframe(self.df2):
                try:
                    # grab the indicators we need (VZO, ADX, DMI, EMA) for this signal
                    vzo2 = TA.VZO(self.df2, period2, column2, adjust2)
                    adx2 = TA.ADX(self.df2, period2, adjust2)
                    dmi2 = TA.DMI(self.df2, period2, adjust2)
                    ema2 = TA.EMA(self.df2, ema_period2, column2, adjust2)
                except TradeSignalException as error:
                    raise error
                else:
                    _vzo_bearish_cross2 = vzo2.iloc[-1] < 40 and trending_down(vzo2.iloc[:-2], period=int(period2/2))
                    _adx_trending2 = adx2.iloc[-1] < 20
                    _dmi_negative2 = dmi2["DI-"] > dmi2["DI+"]
                    _ema_bearish_cross2 = self.df2["close"].iloc[-1] < ema2.iloc[-1] and \
                        trending_down(self.df2["close"].iloc[:-2], period=int(period2/2))
                    selling = selling and _vzo_bearish_cross2 and (_adx_trending2 or _dmi_negative2) and _ema_bearish_cross2

            return selling
