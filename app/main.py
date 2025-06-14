from config import EXCHANGES, SYMBOLS, TIMEFRAME
from utils import is_long_upper_shadow
import ccxt
import pandas as pd


def fetch_candles(exchange, symbol, timeframe):
    print(f"📈 Fetching {symbol} on {exchange.id}...")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def main():
    results = []

    for ex_name in EXCHANGES:
        try:
            ex = getattr(ccxt, ex_name)()
        except Exception as e:
            print(f"❌ 无法初始化交易所 {ex_name}: {e}")
            continue

        for symbol in SYMBOLS.get(ex_name, []):
            try:
                df = fetch_candles(ex, symbol, TIMEFRAME)
                last_candle = df.iloc[-2]  # 上一个交易日
                if is_long_upper_shadow(last_candle):
                    results.append((ex_name, symbol, last_candle["timestamp"]))
            except Exception as e:
                print(f"⚠️ Error fetching {symbol} on {ex_name}: {e}")
                continue

    if results:
        print("\n✅ 满足放量长上影线的币种：")
        for r in results:
            print(f"{r[0]:<10} {r[1]:<15} {r[2]}")
    else:
        print("\n🚫 无符合条件的币种。")


if __name__ == "__main__":
    main()
