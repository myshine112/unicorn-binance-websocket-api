#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_demo.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019, Oliver Zehentleitner
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
import os
import time
import threading

# import class to process stream data
from unicorn_binance_websocket_api_process_streams import BinanceWebSocketApiProcessStreams

# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager and provide the function for stream processing
#binance_websocket_api_manager = BinanceWebSocketApiManager(BinanceWebSocketApiProcessStreams.process_stream_data)
binance_websocket_api_manager = BinanceWebSocketApiManager()


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)
        else:
            try:
                # remove # to activate the print function:
                print(oldest_stream_data_from_stream_buffer)
                pass
            except Exception:
                # not able to process the data? write it back to the stream_buffer
                binance_websocket_api_manager.add_to_stream_buffer(oldest_stream_data_from_stream_buffer)


# start a worker process to process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

print("\r\n========================================== Starting aggTrade ==========================================\r\n")
# start
markets = {'bnbbtc', 'ethbtc', 'btcusdt', 'bchabcusdt', 'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt',
           'neousdt', 'bnbusdt', 'adabtc', 'ethusdt', 'trxbtc', 'bchabcbtc', 'ltcbtc', 'xrpbtc',
           'ontbtc', 'bttusdt', 'eosbtc', 'xlmbtc', 'bttbtc', 'tusdusdt', 'xlmusdt', 'qkcbtc', 'zrxbtc',
           'neobtc', 'adaeth', 'icxusdt', 'btctusd', 'icxbtc', 'btcusdc', 'wanbtc', 'zecbtc', 'wtcbtc',
           'batbtc', 'adabnb', 'etcusdt', 'qtumusdt', 'xmrbtc', 'trxeth', 'adatusd', 'trxxrp', 'trxbnb',
           'dashbtc', 'rvnbnb', 'bchabctusd', 'etcbtc', 'bnbeth', 'ethpax', 'nanobtc', 'xembtc', 'xrpbnb',
           'bchabcpax', 'xrpeth', 'bttbnb', 'ltcbnb', 'agibtc', 'zrxusdt', 'xlmbnb', 'ltceth', 'eoseth',
           'ltctusd', 'polybnb', 'scbtc', 'steembtc', 'trxtusd', 'npxseth', 'kmdbtc', 'polybtc', 'gasbtc',
           'engbtc', 'zileth', 'xlmeth', 'eosbnb', 'xrppax', 'lskbtc', 'npxsbtc', 'xmrusdt', 'ltcpax',
           'ethtusd', 'batusdt', 'mcobtc', 'neoeth', 'bntbtc', 'eostusd', 'lrcbtc', 'funbtc', 'zecusdt',
           'bnbpax', 'linkusdt', 'hceth', 'zrxeth', 'icxeth', 'xmreth', 'neobnb', 'etceth', 'zeceth', 'xmrbnb',
           'wanbnb', 'zrxbnb', 'agibnb', 'funeth', 'arketh', 'engeth'}
aggtrade_stream_id = binance_websocket_api_manager.create_stream(["aggTrade"], markets)
time.sleep(3)
# stop
binance_websocket_api_manager.stop_stream(aggtrade_stream_id)
time.sleep(2)
print("\r\n=========================================== Stopped aggTrade ==========================================\r\n")

print("\r\n====================================== Starting trade and kline_1m ====================================\r\n")
trade_stream_id = binance_websocket_api_manager.create_stream(["trade"], ['bnbbtc', 'ethbtc', 'btcusdt', 'bchabcusdt'])
markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}
kline_1m_stream_id = binance_websocket_api_manager.create_stream("kline_1m", markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(trade_stream_id)
binance_websocket_api_manager.stop_stream(kline_1m_stream_id)
time.sleep(2)
print("\r\n====================================== Stopped trade and kline_1m =====================================\r\n")

print("\r\n======================================== Starting ticker BNB/BTC ======================================\r\n")
ticker_bnbbtc_stream_id = binance_websocket_api_manager.create_stream(["ticker"], ["bnbbtc"])
time.sleep(3)
binance_websocket_api_manager.stop_stream(ticker_bnbbtc_stream_id)
time.sleep(2)
print("\r\n======================================== Stopped ticker BNB/BTC =======================================\r\n")

print("\r\n========================================== Starting miniticker ========================================\r\n")
markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}
miniticker_stream_id = binance_websocket_api_manager.create_stream(["miniTicker"], markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(miniticker_stream_id)
time.sleep(2)
print("\r\n========================================= Stopped miniticker  =========================================\r\n")

print("\r\n========================================== Starting kline_5m ==========================================\r\n")
markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}
kline_5m_stream_id = binance_websocket_api_manager.create_stream(["kline_5m"], markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(kline_5m_stream_id)
time.sleep(2)
print("\r\n========================================= Stopped kline_5m  ===========================================\r\n")

print("\r\n=========================================== Starting depth5 ===========================================\r\n")
markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}
depth5_stream_id = binance_websocket_api_manager.create_stream(["depth5"], markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(depth5_stream_id)
time.sleep(2)
print("\r\n========================================== Stopped depth5  ============================================\r\n")

print("\r\n========================================== Starting depth =============================================\r\n")
markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}
depth_stream_id = binance_websocket_api_manager.create_stream(["depth"], markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(depth_stream_id)
time.sleep(2)
print("\r\n============================================ Stopped depth  ===========================================\r\n")

print("\r\n========================================== Starting !miniticker ========================================\r\n")
markets = {'xrpusdt', 'rvnbtc', 'ltcusdt', 'adausdt', 'eosusdt', 'neousdt'}
miniticker_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!miniTicker"])
time.sleep(4)
binance_websocket_api_manager.stop_stream(miniticker_stream_id)
time.sleep(2)
print("\r\n========================================= Stopped !miniticker  =========================================\r\n")

print("\r\n========================================== Starting ticker all ========================================\r\n")
ticker_all_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!ticker"])
time.sleep(4)
binance_websocket_api_manager.stop_stream(ticker_all_stream_id)
time.sleep(2)
print("\r\n=========================================== Stopped ticker all ========================================\r\n")

print("\r\n=================================== Starting multi multi socket =======================================\r\n")
channels = {'trade', 'kline_1', 'kline_5', 'kline_15', 'kline_30', 'kline_1h', 'kline_12h', 'kline_1w',
            'miniTicker', 'depth20'}
print(channels)
print(markets, "\r\n")
time.sleep(1)
multi_multi_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(3)
binance_websocket_api_manager.stop_stream(multi_multi_stream_id)
time.sleep(2)
print("\r\n================================== Stopped multi multi socket  ========================================\r\n")

print("\r\n============================= Starting multi multi socket subscribe ===================================\r\n")
channels = {'trade', 'kline_1', 'kline_5', 'kline_15', 'kline_30', 'kline_1h', 'kline_12h', 'kline_1w',
            'miniTicker', 'depth20', '!miniTicker', '!ticker'}
channels = {'trade', '!miniTicker'}
print(channels)
print(markets, "\r\n")
time.sleep(1)
multi_multi_stream_id = binance_websocket_api_manager.create_stream(channels, markets)
time.sleep(5)
binance_websocket_api_manager.stop_stream(multi_multi_stream_id)
time.sleep(2)
print("\r\n============================== Stopped multi multi socket subscribe ===================================\r\n")


print("\r\n=============================== Stopping BinanceWebSocketManager ======================================\r\n")
binance_websocket_api_manager.stop_manager_with_all_streams()
print("finished!")
