import os
import time
import unittest
from collections import namedtuple
from unittest.mock import patch
import utils
from binance_futures_client import BinanceFuturesClient, Candle



class TestBinanceFuturesClient(unittest.TestCase):
    # run before all tests
    @classmethod
    def setUpClass(cls):
        # client = BinanceFuturesClient(FUTURE_API_KEY, FUTURE_API_SECRET, testing=True)
        # cls.leverage = client.get_leverage('BTCUSDT')
        pass

    # run after all tests
    @classmethod
    def tearDownClass(cls):
        # client = BinanceFuturesClient(FUTURE_API_KEY, FUTURE_API_SECRET, testing=True)
        # client.set_leverage('BTCUSDT', cls.leverage)
        pass

    def setUp(self):
        # Setup runs before each test method
        self.client = BinanceFuturesClient(None, None, testing=True)
        self.client.close_all_positions()

    # function close all current positions to set up for testing
    @patch('binance.um_futures.UMFutures.time')
    def test_get_server_time(self, mock_time):
        # Setup the mock to return a specific value
        mock_time.return_value = {'serverTime': 1234567890}

        # Call the function
        response = self.client.get_server_time()
        print(response)

        # Check if the response ikliness as expected
        self.assertEqual(response, 1234567890)

        # Ensure the mock was called
        mock_time.assert_called_once()

    @patch('binance.um_futures.UMFutures.account')
    def test_get_account_info_failure(self, mock_account):
        # Configure the mock to raise an exception
        mock_account.side_effect = Exception("API Error")

        # Use assertRaises to ensure it raises the exception
        with self.assertRaises(Exception) as context:
            self.client.get_account_info()

        # Optionally check the message
        self.assertTrue('API Error' in str(context.exception))

    # add real test for get_server_time
    def test_get_server_time_real(self):
        response = self.client.get_server_time()
        self.assertTrue(type(response) == int)

    # add real test include several steps:
    # 1. get account info, store the current balance
    # 2. place 3 orders: 2 LONG, 1 SHORT
    # 3. get account info again, check whether the positions are opened and correct
    # 4. close all positions
    # 5. get account info again, check whether the positions are closed and correct
    # write that test
    def test_open_close_positions(self):
        # 1. get account info, store the current balance
        account_info = self.client.get_account_info()
        # balance = self.client.get_balance()
        # print(f"Balance: {balance}")
        # print(utils.beautify_json(account_info))

        # 2. place 3 orders: 2 LONG, 1 SHORT
        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)
        # print(utils.beautify_json(response))

        params = {
            'symbol': 'ETHUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.1,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)
        # print(utils.beautify_json(response))

        params = {
            'symbol': 'BTCUSDT',
            'side': 'SELL',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'SHORT'
        }

        response = self.client.place_order(**params)
        # print(utils.beautify_json(response))

        # 3. get account info again, check whether the positions are opened and correct
        account_info = self.client.get_account_info()
        # print(utils.beautify_json(account_info))
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 3)

        self.assertEqual(type(self.client.get_unrealized_pnl()), float)

        # 4. close all positions
        response = self.client.close_all_positions()
        self.assertEqual(len(response), 3)

        # 5. get account info again, check whether the positions are closed and correct
        # account_info = self.client.get_account_info()
        # print(utils.beautify_json(account_info))
        self.assertEqual(len(self.client.get_open_positions()), 0)

    # test the function get_unrealized_pnl:
    # 1. place an order
    # 2. wait for 5s
    # 3. get unrealized pnl and check if it is a number, and != 0
    def test_get_unrealized_pnl(self):
        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)

        time.sleep(5)

        pnl = self.client.get_unrealized_pnl()
        self.assertTrue(type(pnl) == float)
        self.assertNotEqual(pnl, 0.0)

    # write tests for earch method in binance_futures_client.py
    # test_place_order
    def test_place_order(self):
        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)
        self.assertTrue('orderId' in response)
        # get open positions and assert
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 1)
        self.assertEqual(open_positions[0]['symbol'], 'BTCUSDT')
        self.assertEqual(open_positions[0]['positionSide'], 'LONG')
        self.assertEqual(float(open_positions[0]['positionAmt']), 0.01)

    # test_close_position
    def test_close_position(self):
        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)

        response = self.client.close_position('BTCUSDT', 'LONG')
        self.assertTrue('orderId' in response)
        # get open positions and assert
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 0)

    # test_get_open_positions
    def test_get_open_positions(self):
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 0)

        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 1)

        params = {
            'symbol': 'BTCUSDT',
            'side': 'SELL',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'SHORT'
        }
        response = self.client.place_order(**params)
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 2)

    # test_close_all_positions
    def test_close_all_positions(self):
        response = self.client.close_all_positions()
        self.assertEqual(len(response), 0)

        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)

        params = {
            'symbol': 'ETHUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.1,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)

        params = {
            'symbol': 'BTCUSDT',
            'side': 'SELL',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'SHORT'
        }

        response = self.client.place_order(**params)

        response = self.client.close_all_positions()
        self.assertEqual(len(response), 3)
        # get open positions and assert
        open_positions = self.client.get_open_positions()
        self.assertEqual(len(open_positions), 0)

    # test_change_leverage
    def test_change_leverage(self):
        response = self.client.change_leverage('BTCUSDT', 10)
        print(response)
        self.assertTrue('leverage' in response)
        self.assertEqual(response['leverage'], 10)
        # open LONG position
        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'order_type': 'MARKET',
            'quantity': 0.01,
            'position_side': 'LONG'
        }
        response = self.client.place_order(**params)
        print(response)

    # test get/set leverage
    def test_get_set_leverage(self):
        response = self.client.set_leverage('BTCUSDT', 20)
        self.assertTrue('leverage' in response)
        self.assertEqual(response['leverage'], 20)

        leverage = self.client.get_leverage('BTCUSDT')
        self.assertEqual(leverage, 20)

        response = self.client.set_leverage('BTCUSDT', 10)
        self.assertTrue('leverage' in response)
        self.assertEqual(response['leverage'], 10)

        leverage = self.client.get_leverage('BTCUSDT')
        self.assertEqual(leverage, 10)

        response = self.client.set_leverage('BTCUSDT', 20)
        self.assertTrue('leverage' in response)
        self.assertEqual(response['leverage'], 20)


    # test klines
    def test_klines(self):
        klines = self.client.klines('BTCUSDT', '1m', 5)
        self.assertEqual(len(klines), 5)
        # Timed_Candle = namedtuple('Timed_Candle', ['open_dt', 'open', 'high', 'low', 'close', 'volume', 'close_dt'])

        # bars = [
        #     Timed_Candle(
        #         open_dt=utils.ms_to_datetime(candle.open_time),
        #         open=float(candle.open),
        #         high=float(candle.high),
        #         low=float(candle.low),
        #         close=float(candle.close),
        #         volume=float(candle.volume),
        #         close_dt=utils.ms_to_datetime(candle.close_time)
        #     )
        #     for candle in klines
        # ]
        # print(bars)
