#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_trade_signal.mfi import MfiSignal
import pandas as pd
import numpy as np
import os


def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


data_file = os.path.join(rootdir(), "data/bittrex:btc-usdt.csv")

ohlc = pd.read_csv(data_file, index_col="date", parse_dates=True)

signal = MfiSignal(df=ohlc)


def test_buy():
    res = signal.buy()
    assert res is not None
    assert type(res) == np.bool_


def test_sell():
    res = signal.sell()
    assert res is not None
    assert type(res) == np.bool_
