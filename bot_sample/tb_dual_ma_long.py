import pandas as pd
MAX_CANDLES = 500
CHECK_CUT_CANDLES = 5
class DualMALong:
    def __init__(self, client):
        self.__client = client

    def execute_strategy(self, symbol, interval, slow_ma_period, fast_ma_period, entry_pct, diff_pct, tolerance_pct, quantity):
        # Fetch recent candlesticks from Binance
        candles = self.__client.klines(symbol, interval, MAX_CANDLES)
        df = pd.DataFrame(candles, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['open'] = pd.to_numeric(df['open'])

        # Calculate moving averages
        slow_ma = df['close'].rolling(window=slow_ma_period).mean()
        fast_ma = df['close'].rolling(window=fast_ma_period).mean()

        # Check current position status
        current_position = self.get_long_position(symbol)
        last_index = len(df) - 1

        above_slow_ma = self.check_ma_cut(df['open'], df['close'], slow_ma, last_index, CHECK_CUT_CANDLES)
        under_fast_ma = self.check_ma_cut(df['open'], df['close'], fast_ma, last_index, CHECK_CUT_CANDLES, invert=True)

        if self.should_open_long(above_slow_ma, df['close'][last_index], slow_ma, fast_ma, last_index, entry_pct, diff_pct):
            params = {
                'symbol': symbol,
                'side': 'BUY',
                'order_type': 'MARKET',
                'quantity': quantity,
                'position_side': 'LONG'
            }
            response = self.__client.place_order(**params)
            return {
                'response_code': 0,
                'order_type': 'OPEN_LONG',
                'order_response': response
            }
        elif self.should_close_long(under_fast_ma, df['close'][last_index], fast_ma, last_index, tolerance_pct, current_position):
            response = self.__client.close_position(symbol, 'LONG')
            return {
                'response_code': 0,
                'order_type': 'CLOSE_LONG',
                'order_response': response
            }
        return {'response_code': 1, 'message': 'No action needed'}

    def get_long_position(self, symbol):
        positions = self.__client.get_open_positions()
        long_positions = [pos for pos in positions if (pos['positionSide'] == 'LONG' and pos['symbol'] == symbol)]
        return None if len(long_positions) == 0 else long_positions[0]

    @staticmethod
    def check_ma_cut(opens, closes, ma, last_index, k, invert=False):
        start_index = max(0, last_index - k + 1)
        for i in range(start_index, last_index + 1):
            if (opens[i] < ma[i] < closes[i]) != invert:
                return True
        return False

    @staticmethod
    def should_open_long(above_slow_ma, current_price, slow_ma, fast_ma, index, entry_pct, diff_pct):
        return above_slow_ma and \
               current_price > slow_ma[index] * (1 + entry_pct) and \
               fast_ma[index] > slow_ma[index] * (1 - diff_pct)

    @staticmethod
    def should_close_long(under_fast_ma, current_price, fast_ma, index, tolerance_pct, current_position):
        if current_position is None:
            return False
        return under_fast_ma and current_price < fast_ma[index] * (1 - tolerance_pct)
