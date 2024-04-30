from typing import List
import os
from dotenv import load_dotenv
from binance.um_futures import UMFutures
from collections import namedtuple

SERVER_TIME = 'serverTime'

Candle = namedtuple('Candle', ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time'])


class BinanceFuturesClient:
    BASE_URL_TESTNET_FUTURE = "https://testnet.binancefuture.com"  # Testnet base URL

    def __init__(self, api_key, api_secret, testing=True):
        load_dotenv()
        if (api_key is None) or (api_secret is None):
            api_key = os.getenv("FUTURE_API_KEY")
            api_secret = os.getenv("FUTURE_API_SECRET")

        print(f"API_KEY:{api_key}")
        print(f"API_SECRET:{api_secret}")

        """Initialize the Binance Futures client with API keys."""
        base_url = "https://testnet.binancefuture.com" if testing else "https://fapi.binance.com"
        self.client = UMFutures(key=api_key, secret=api_secret, base_url=base_url)

    def get_server_time(self):
        """Retrieve the server time from Binance."""
        return self.client.time()[SERVER_TIME]

    def get_balance(self):
        """Get the account balance for USDT."""
        account_info = self.get_account_info()
        balances = account_info['assets']
        usdt_balance = next((asset['balance'] for asset in balances if asset['asset'] == 'USDT'), None)
        return float(usdt_balance)

    def get_account_info(self):
        """Get the account information, including current positions."""
        return self.client.account()

    # get the assets which are available (not 0)
    def get_available_assets(self):
        account_info = self.get_account_info()
        balances = account_info['assets']
        available_assets = [asset for asset in balances if float(asset['walletBalance']) != 0]
        return available_assets

    # get the UnRealized PnL
    def get_unrealized_pnl(self):
        account_info = self.get_account_info()
        return float(account_info['totalUnrealizedProfit'])

    def place_order(self, symbol, side, order_type, quantity, price=None, position_side='BOTH', time_in_force='GTC'):
        """Place a new order on Binance Futures."""
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'positionSide': position_side
        }
        if price:
            params['price'] = price
        if order_type == 'LIMIT':
            params['timeInForce'] = time_in_force

        return self.client.new_order(**params)

    def close_position(self, symbol, position_side):
        """Close a specific position (LONG or SHORT) in hedge mode for a given symbol."""
        account_info = self.get_account_info()
        positions = account_info['positions']
        position_info = next(
            (pos for pos in positions if pos['symbol'] == symbol and pos['positionSide'] == position_side), None)

        if position_info and float(position_info['positionAmt']) != 0:
            side = 'SELL' if position_side == 'LONG' else 'BUY'
            quantity = abs(float(position_info['positionAmt']))

            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity,
                'positionSide': position_side
            }
            return self.client.new_order(**order_params)
        else:
            return "No open position to close for this symbol or side."

    def get_open_positions(self):
        """Retrieve all open positions (both LONG and SHORT) in hedge mode."""
        account_info = self.get_account_info()
        positions = account_info['positions']
        open_positions = [pos for pos in positions if float(pos['positionAmt']) != 0]
        return open_positions

    # close all current positions
    def close_all_positions(self):
        account_info = self.get_account_info()
        positions = account_info['positions']
        res = []
        for position in positions:
            if (float(position['positionAmt']) != 0):
                res.append(self.close_position(position['symbol'], position['positionSide']))
        return res

    # change leverage
    def change_leverage(self, symbol, leverage):
        return self.client.change_leverage(symbol=symbol, leverage=leverage)

    # get leverage
    def get_leverage(self, symbol):
        try:
            acc = self.get_account_info()
            positions = acc.get('positions', [])
            pos = next((p for p in positions if p['symbol'] == symbol), None)
            return float(pos['leverage']) if pos else None
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

    def set_leverage(self, symbol, leverage):
        return self.client.change_leverage(symbol=symbol, leverage=leverage)

    def klines(self, symbol, interval, limit=500) -> List[Candle]:
        klines = self.client.klines(symbol=symbol, interval=interval, limit=limit)
        # Kline response item:
        # [
        #     1499040000000,      // Open time
        #     "0.01634790",       // Open
        #     "0.80000000",       // High
        #     "0.01575800",       // Low
        #     "0.01577100",       // Close
        #     "148976.11427815",  // Volume
        #     1499644799999,      // Close time
        #     "2434.19055334",    // Quote asset volume
        #     308,                // Number of trades
        #     "1756.87402397",    // Taker buy base asset volume
        #     "28.46694368",      // Taker buy quote asset volume
        #     "17928899.62484339" // Ignore.
        # ]
        return [
            Candle(
                open_time=bar[0],
                open=float(bar[1]),
                high=float(bar[2]),
                low=float(bar[3]),
                close=float(bar[4]),
                volume=float(bar[5]),
                close_time=bar[6]
            )
            for bar in klines
        ]
