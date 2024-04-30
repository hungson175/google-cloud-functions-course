from binance_futures_client import BinanceFuturesClient
from tb_long_dual_sma import TradingBot_Long_Dual_SMA

def execute_strategy(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    request_args = request.args
    response = ""
    if request_args and 'symbol' in request_args:
        symbol = request_args['symbol']
    else:
        symbol = 'BTCUSDT'
        # bot = TradingBot( BinanceFuturesClient(None, None, testing=True))
        # bot.execute_strategy(symbol,interval='4h', period=50, quantity=0.005)
        bot = TradingBot_Long_Dual_SMA(BinanceFuturesClient(None, None, True))
        response = bot.execute_strategy('BTCUSDT',
                                        '5m',
                                        60,
                                        0.01,
                                        12,
                                        0.01,
                                        0.01)
        print(response)
    return f'Trading bot response:  {response}.'
