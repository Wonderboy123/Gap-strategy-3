# Python version of your WICKSNIPER_V9_43 for Gareth X mobile
RISK_PERCENT = 0.5
RR = 3.0
MIN_WICK_PERCENT = 50
SR_LOOKBACK = 100
SR_BUFFER = 40
MAX_TRADES = 10

def check_wick_rejection(candle, support, resistance, buffer):
    o,h,l,c = candle['open'],candle['high'],candle['low'],candle['close']
    body = abs(c-o)
    if body == 0: return 0
    upper_wick = h - max(o,c)
    lower_wick = min(o,c) - l
    if lower_wick/body*100 >= MIN_WICK_PERCENT and abs(l-support) <= buffer:
        return 1  # BUY like your circles
    if upper_wick/body*100 >= MIN_WICK_PERCENT and abs(h-resistance) <= buffer:
        return -1 # SELL
    return 0

def get_lot_size(balance, sl_points, point_val, tick_val, tick_size):
    risk = balance * (RISK_PERCENT/100)
    money_per_point = tick_val / tick_size * point_val
    lot = risk / (sl_points * money_per_point)
    return round(max(0.01, lot), 2)
