import pandas as pd

RESPONSE_CODE_SUCCESS = 0
RESPONSE_CODE_NO_ACTION = 1
OPEN_LONG = 'OPEN_LONG'
CLOSE_LONG = 'CLOSE_LONG'


class TradingBot_Long_Dual_SMA:
    __client = None

    def __init__(self, client):
        self.__client = client

    def execute_strategy(self,
                         symbol,
                         interval,
                         slow_ma, entry_pct,
                         fast_ma, tolerance_pct,
                         quantity):
        """Execute the trading strategy based on moving average."""
        entry_pct = entry_pct / 100
        tolerance_pct = tolerance_pct / 100
        candles = self.__client.klines(symbol, interval, 300)
        df = pd.DataFrame(candles)
        current_position = self.get_long_position(symbol)
        if (current_position is None) and self.should_open_long(df, slow_ma, entry_pct):
            params = {
                'symbol': symbol,
                'side': 'BUY',
                'order_type': 'MARKET',
                'quantity': quantity,
                'position_side': 'LONG'
            }
            response = self.__client.place_order(**params)
            return {
                'response_code': RESPONSE_CODE_SUCCESS,
                'order_type': OPEN_LONG,
                'order_response': response
            }
        elif (current_position is not None) and self.should_close_long(df, fast_ma, tolerance_pct):
            response = self.__client.close_position(symbol, 'LONG')
            return {
                'response_code': RESPONSE_CODE_SUCCESS,
                'order_type': CLOSE_LONG,
                'order_response': response
            }
        else:
            return {
                'response_code': RESPONSE_CODE_NO_ACTION,
                'message': 'No action taken'
            }

    def get_long_position(self, symbol):
        positions = self.__client.get_open_positions()
        long_positions = [pos for pos in positions if (pos['positionSide'] == 'LONG' and pos['symbol'] == symbol)]
        return None if len(long_positions) == 0 else long_positions[0]

    @staticmethod
    def should_open_long(df, ma_window, pct):
        # calculate the moving average
        ma_frame = pd.DataFrame()
        ma_frame['ma'] = df['close'].rolling(window=ma_window).mean()
        # check whether the last candle cuts the ma from below (open < ma, close > ma)
        next_to_last_candle = df.iloc[-2]
        last_candle = df.iloc[-1]
        last_ma = ma_frame.iloc[-1]['ma']
        return True if ((last_candle['open'] < last_ma or next_to_last_candle['open'] < last_ma)
                        and last_candle['close'] > last_ma * (1 + pct)) \
            else False

    @staticmethod
    def should_close_long(self, df, ma_window, pct):
        # should close when: the last candle cuts the ma from above (open > ma, close < ma)
        ma_frame = pd.DataFrame()
        ma_frame['ma'] = df['close'].rolling(window=ma_window).mean()
        next_to_last_candle = df.iloc[-2]
        last_candle = df.iloc[-1]
        last_ma = ma_frame.iloc[-1]['ma']
        return True if (
                (last_candle['open'] > last_ma or next_to_last_candle['open'] > last_ma)
                and last_candle['close'] < last_ma * (1 - pct)) \
            else False

# if __name__ == '__main__':
#     bot = TradingBot_Long_Dual_SMA(BinanceFuturesClient(None, None, True))
#     response = bot.execute_strategy('BTCUSDT',
#                          '5m',
#                          21,
#                          0.01,
#                          7,
#                          0.01,
#                          0.01)
#     print(response)