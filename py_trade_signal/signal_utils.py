#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd


class SignalUtils(object):

    @staticmethod
    def is_valid_dataframe(dataframe: pd.DataFrame) -> bool:
        return dataframe is not None and len(dataframe.index) > 0
