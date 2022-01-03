#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_binance_jex.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api
# Documentation: https://lucit-systems-and-development.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import logging
import time
import threading
import os


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)


# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager for Binance Jersey
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="jex.com")

# set api key and secret for userData stream
userdata_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!userData"], api_key="aaa", api_secret="bb")

omt_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!optionMiniTicker"])
smt_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!spotMiniTicker"])
st_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!spotTicker"])

spot_markets = {'eosbtc', 'ltcbtc', 'ethbtc', 'dashbtc'}
spot_channels = {'spotTrade', 'spotMiniTicker', 'spotDepth20', 'spotDepthUpdate', 'spotTicker'}
binance_websocket_api_manager.create_stream(["spotTrade"], spot_markets)
binance_websocket_api_manager.create_stream(["spotDepth10"], spot_markets)
binance_websocket_api_manager.create_stream(["spotDepth20"], spot_markets)
binance_websocket_api_manager.create_stream(spot_channels, spot_markets)

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

# show an overview
while True:
    binance_websocket_api_manager.print_summary()
    #binance_websocket_api_manager.print_stream_info(userdata_stream_id)
    time.sleep(1)
