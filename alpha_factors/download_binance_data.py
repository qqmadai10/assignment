import requests
import pandas as pd
import time
import os


def download_binance_klines(symbol='BTCUSDT', interval='1d', limit=1000):
    """
    从币安公开 API 获取历史K线
    interval: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    """
    all_klines = []
    start_time = None

    print(f"Downloading {symbol} {interval} data...")

    # 币安日线数据最多 1000 条，如果需要更多可以多次请求
    for _ in range(5):  # 最多 5000 条
        url = 'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        if start_time:
            params['startTime'] = start_time

        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            if not data:
                break

            all_klines.extend(data)
            # 更新起始时间为最后一条的时间+1ms
            start_time = data[-1][0] + 1
            time.sleep(0.1)  # 避免请求过快

            print(f"  Fetched {len(data)} records...")

        except Exception as e:
            print(f"Error: {e}")
            break

    if not all_klines:
        print("No data downloaded.")
        return None

    # 解析为 DataFrame
    df = pd.DataFrame(all_klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])

    # 转换数据类型
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    # 只保留需要的列
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df.set_index('timestamp', inplace=True)

    print(f"\nDownloaded {len(df)} records from {df.index[0]} to {df.index[-1]}")

    # 保存到 CSV
    df.to_csv('btc_data.csv')
    print("Saved to btc_data.csv")

    return df


def download_multiple_timeframes():
    """下载多个时间周期的数据"""
    timeframes = ['1d', '4h', '1h']

    for interval in timeframes:
        print("\n" + "=" * 50)
        print(f"Downloading {interval} data...")
        print("=" * 50)

        filename = f'btc_data_{interval}.csv'
        df = download_binance_klines(interval=interval, limit=1000)

        if df is not None:
            df.to_csv(filename)
            print(f"Saved to {filename}")


if __name__ == "__main__":
    # 下载日线数据（用于 Alpha 因子分析）
    download_binance_klines(interval='1d', limit=1000)

    # 可选：下载更多时间周期
    # download_multiple_timeframes()