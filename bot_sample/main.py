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
    try:
        request_args = request.args
        symbol = request_args.get('symbol', "BTCUSDT")
        interval = request_args.get('interval', "4h")
        slow_ma = int(request_args.get('slow_ma', 109))
        fast_ma = int(request_args.get('fast_ma', 46))
        entry_pct = float(request_args.get('entry_pct', 0.3))
        tolerance_pct = float(request_args.get('tolerance_pct', 0.8))
        quantity = float(request_args.get('quantity', 0.405))

        bot = TradingBot_Long_Dual_SMA(BinanceFuturesClient(None, None, False))
        response = bot.execute_strategy(symbol, interval, slow_ma, entry_pct, fast_ma, tolerance_pct, quantity)
        return f'Trading bot response: {response}', 200, headers
    except ValueError as e:
        return f'Error processing parameters: {str(e)}', 400, headers
