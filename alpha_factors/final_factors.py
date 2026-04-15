import pandas as pd
import numpy as np


class FinalAlphaFactors:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.factors = pd.DataFrame(index=df.index)

    def calculate_all_factors(self):
        """计算 15 个 Alpha 因子"""
        # 原有 10 个因子
        self._rsi(14)
        self._macd()
        self._bollinger_bands(20, 2)
        self._volume_ratio(5)
        self._momentum(10)
        self._volatility(20)
        self._price_position(20)
        self._obv()
        self._atr(14)
        self._stochastic(14)

        # 新增 5 个低相关因子
        self._volume_change(5)
        self._price_change(5)
        self._high_low_ratio(10)
        self._close_position(10)
        self._volume_price_trend(10)

        return self.factors

    # ============ 原有因子 ============

    def _rsi(self, period=14):
        delta = self.df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.factors['RSI'] = rsi / 100

    def _macd(self):
        exp1 = self.df['close'].ewm(span=12, adjust=False).mean()
        exp2 = self.df['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        macd_hist = macd - signal
        if macd_hist.std() > 0:
            self.factors['MACD'] = macd_hist / macd_hist.std()
        else:
            self.factors['MACD'] = 0

    def _bollinger_bands(self, period=20, std=2):
        sma = self.df['close'].rolling(window=period).mean()
        rolling_std = self.df['close'].rolling(window=period).std()
        upper_band = sma + (rolling_std * std)
        lower_band = sma - (rolling_std * std)
        bb_position = (self.df['close'] - lower_band) / (upper_band - lower_band)
        self.factors['BB'] = bb_position.fillna(0.5)

    def _volume_ratio(self, period=5):
        avg_volume = self.df['volume'].rolling(window=period).mean()
        volume_ratio = self.df['volume'] / avg_volume
        self.factors['VolRatio'] = volume_ratio.clip(0, 3) / 3

    def _momentum(self, period=10):
        momentum = self.df['close'].pct_change(period)
        self.factors['Momentum'] = momentum.clip(-0.1, 0.1) / 0.1

    def _volatility(self, period=20):
        returns = self.df['close'].pct_change()
        volatility = returns.rolling(window=period).std() * np.sqrt(252)
        self.factors['Volatility'] = volatility.clip(0, 1)

    def _price_position(self, period=20):
        rolling_min = self.df['close'].rolling(window=period).min()
        rolling_max = self.df['close'].rolling(window=period).max()
        price_position = (self.df['close'] - rolling_min) / (rolling_max - rolling_min)
        self.factors['PricePos'] = price_position.fillna(0.5)

    def _obv(self):
        obv = (np.sign(self.df['close'].diff()) * self.df['volume']).cumsum()
        obv_min = obv.min()
        obv_max = obv.max()
        if obv_max > obv_min:
            obv_normalized = (obv - obv_min) / (obv_max - obv_min)
        else:
            obv_normalized = 0.5
        self.factors['OBV'] = obv_normalized.fillna(0.5)

    def _atr(self, period=14):
        high_low = self.df['high'] - self.df['low']
        high_close = abs(self.df['high'] - self.df['close'].shift())
        low_close = abs(self.df['low'] - self.df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        if atr.max() > 0:
            self.factors['ATR'] = atr / atr.max()
        else:
            self.factors['ATR'] = 0

    def _stochastic(self, period=14):
        low_min = self.df['low'].rolling(window=period).min()
        high_max = self.df['high'].rolling(window=period).max()
        stoch = (self.df['close'] - low_min) / (high_max - low_min) * 100
        self.factors['Stoch'] = stoch / 100

    # ============ 新增 5 个低相关因子 ============

    def _volume_change(self, period=5):
        """成交量变化率 - 与价格相关性低"""
        volume_change = self.df['volume'].pct_change(period)
        self.factors['VolChange'] = volume_change.clip(-1, 1)

    def _price_change(self, period=5):
        """价格变化率 - 简单动量，与复杂因子相关性低"""
        price_change = self.df['close'].pct_change(period)
        self.factors['PriceChange'] = price_change.clip(-0.05, 0.05) / 0.05

    def _high_low_ratio(self, period=10):
        """日内波幅比率 - 与波动率相关但计算方式不同"""
        high_low_ratio = (self.df['high'] - self.df['low']) / self.df['close']
        hl_sma = high_low_ratio.rolling(window=period).mean()
        self.factors['HLRatio'] = hl_sma.clip(0, 0.05) / 0.05

    def _close_position(self, period=10):
        """收盘价位置 - 在当日区间的位置"""
        close_position = (self.df['close'] - self.df['low']) / (self.df['high'] - self.df['low'])
        self.factors['ClosePos'] = close_position.fillna(0.5)

    def _volume_price_trend(self, period=10):
        """量价趋势 - 价格变化与成交量变化的组合"""
        price_change = self.df['close'].pct_change(period)
        volume_change = self.df['volume'].pct_change(period)
        vpt = price_change * volume_change
        self.factors['VPT'] = vpt.clip(-1, 1)