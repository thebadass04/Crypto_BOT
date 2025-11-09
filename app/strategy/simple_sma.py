import pandas as pd
import numpy as np
from typing import List, Tuple
from app.models import Signal, Kline


class SimpleSMA:
    def __init__(self, fast_period: int = 9, slow_period: int = 21):
        self.fast_period = fast_period
        self.slow_period = slow_period
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        if len(prices) < period:
            return 0.0
        return sum(prices[-period:]) / period
    
    def generate_signal(self, klines: List[Kline]) -> Tuple[Signal, float, float]:
        if len(klines) < self.slow_period:
            return Signal.HOLD, 0.0, 0.0
        
        closes = [k.close for k in klines]
        
        sma_fast = self.calculate_sma(closes, self.fast_period)
        sma_slow = self.calculate_sma(closes, self.slow_period)
        
        if len(klines) >= self.slow_period + 1:
            prev_closes = closes[:-1]
            prev_sma_fast = self.calculate_sma(prev_closes, self.fast_period)
            prev_sma_slow = self.calculate_sma(prev_closes, self.slow_period)
            
            if prev_sma_fast <= prev_sma_slow and sma_fast > sma_slow:
                return Signal.BUY, sma_fast, sma_slow
            elif prev_sma_fast >= prev_sma_slow and sma_fast < sma_slow:
                return Signal.SELL, sma_fast, sma_slow
        
        return Signal.HOLD, sma_fast, sma_slow
    
    def analyze_with_pandas(self, klines: List[Kline]) -> Tuple[Signal, float, float]:
        if len(klines) < self.slow_period:
            return Signal.HOLD, 0.0, 0.0
        
        df = pd.DataFrame([
            {
                'timestamp': k.timestamp,
                'close': k.close
            } for k in klines
        ])
        
        df[f'sma_{self.fast_period}'] = df['close'].rolling(window=self.fast_period).mean()
        df[f'sma_{self.slow_period}'] = df['close'].rolling(window=self.slow_period).mean()
        
        df.dropna(inplace=True)
        
        if len(df) < 2:
            return Signal.HOLD, 0.0, 0.0
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        sma_fast = last_row[f'sma_{self.fast_period}']
        sma_slow = last_row[f'sma_{self.slow_period}']
        prev_sma_fast = prev_row[f'sma_{self.fast_period}']
        prev_sma_slow = prev_row[f'sma_{self.slow_period}']
        
        if prev_sma_fast <= prev_sma_slow and sma_fast > sma_slow:
            return Signal.BUY, float(sma_fast), float(sma_slow)
        elif prev_sma_fast >= prev_sma_slow and sma_fast < sma_slow:
            return Signal.SELL, float(sma_fast), float(sma_slow)
        
        return Signal.HOLD, float(sma_fast), float(sma_slow)


sma_strategy = SimpleSMA()
