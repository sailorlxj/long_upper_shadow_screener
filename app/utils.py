def is_long_upper_shadow(candle):
    high = candle["high"]
    open_ = candle["open"]
    close = candle["close"]
    low = candle["low"]
    volume = candle["volume"]

    body = abs(close - open_)
    upper_shadow = high - max(open_, close)
    lower_shadow = min(open_, close) - low

    return (
        upper_shadow > body * 2 and
        upper_shadow > lower_shadow and
        volume > 0
    )
