import pandas as pd


class SingleMALong:
    def __init__(self, client):
        self.__client = client

    def execute_strategy(self,
                         symbol, interval,
                         ma_period,
                         entry_pct, tolerance_pct,
                         quantity):
        entry_pct = entry_pct / 100
        tolerance_pct = tolerance_pct / 100
        candles = self.__client.klines(symbol, interval, 300)
        df = pd.DataFrame(candles)
        current_position = self.get_long_position(symbol)
        df['ma'] = df['close'].rolling(window=ma_period).mean()
        if self.should_open_long(df, current_position, ma_period, entry_pct):
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
        elif self.should_close_long(df, current_position, ma_period, tolerance_pct):
            response = self.__client.close_position(symbol, 'LONG')
            return {
                'response_code': 0,
                'order_type': 'CLOSE_LONG',
                'order_response': response
            }
        pass

    def get_long_position(self, symbol):
        positions = self.__client.get_open_positions()
        long_positions = [pos for pos in positions if (pos['positionSide'] == 'LONG' and pos['symbol'] == symbol)]
        return None if len(long_positions) == 0 else long_positions[0]

    @staticmethod
    def should_open_long(df, current_position, ma_window, pct):
        if current_position is not None:
            return False

        last_close = df['close'].iloc[-1]
        last_ma = df['ma'].iloc[-1]
        return last_close > last_ma * (1 + pct)

    @staticmethod
    def should_close_long(df, current_position, ma_window, pct):
        if current_position is None:
            return False
        df['ma'] = df['close'].rolling(window=ma_window).mean()
        last_close = df['close'].iloc[-1]
        last_ma = df['ma'].iloc[-1]
        return last_close < last_ma * (1 - pct)
