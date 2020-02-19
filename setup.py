#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textwrap import dedent
import setuptools


setuptools.setup(
      name="py_trade_signal",
      version="1.0.3",
      packages=["py_trade_signal"],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      license=dedent("""\
      Copyright (c) 2019 bbeale

      Permission is hereby granted, free of charge, to any person obtaining a copy
      of this software and associated documentation files (the "Software"), to deal
      in the Software without restriction, including without limitation the rights
      to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
      copies of the Software, and to permit persons to whom the Software is
      furnished to do so, subject to the following conditions:

      The above copyright notice and this permission notice shall be included in all
      copies or substantial portions of the Software.

      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
      IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
      FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
      AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
      LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
      OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
      SOFTWARE."""),
      description="A collection of trade signals calculated via traditional technical and fundamental analysis, with the inclusion of sentiment based indicators.",
      long_description=dedent("""\
      Getting Started:
      
            python setup.py install
      
      With pip:
      
            pip install py_trade_signal
      """),
      long_description_content_type="text/markdown",
      author="bbeale",
      author_email="beale.ben@gmail.com",
      url="https://github.com/bbeale/py-trade-signal",
      setup_requires=["wheel", "setuptools"],
      requires=["finta", "numpy", "pandas", "python_dateutil", "pytz", "six"]
      )
