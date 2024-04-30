from binance_futures_client import BinanceFuturesClient
from trading_bot import TradingBot, execute_strategy
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
    if request_args and 'symbol' in request_args:
        symbol = request_args['symbol']
    else:
        symbol = 'BTCUSDT'
    bot = TradingBot( BinanceFuturesClient(None, None, testing=True))
    bot.execute_strategy(symbol,interval='4h', period=50, quantity=0.005)
    return f'Trading bot executed for {symbol}.'




