import pandas as pd
import numpy as np
import ta
import config
class TradingStrategy:
"""
Implementa la strategia di trading basata su RSI + MACD + ATR.
"""
def __init__(self):
self.rsi_period = config.RSI_PERIOD
self.rsi_oversold = config.RSI_OVERSOLD
self.rsi_overbought = config.RSI_OVERBOUGHT
self.macd_fast = config.MACD_FAST
self.macd_slow = config.MACD_SLOW
self.macd_signal = config.MACD_SIGNAL
self.atr_sl_multiplier = config.ATR_MULTIPLIER_SL
self.atr_tp_multiplier = config.ATR_MULTIPLIER_TP
def calculate_indicators(self, df):
"""
Calcola tutti gli indicatori tecnici necessari.
Args:
df (DataFrame): DataFrame con colonne [open, high, low, close]
Returns:
DataFrame: DataFrame con indicatori aggiunti
"""
# Crea una copia per evitare modifiche al DataFrame originale
df = df.copy()
# RSI - Relative Strength Index
df['rsi'] = ta.momentum.RSIIndicator(
close=df['close'],
window=self.rsi_period
).rsi()
# MACD - Moving Average Convergence Divergence
macd_indicator = ta.trend.MACD(
close=df['close'],
window_slow=self.macd_slow,
window_fast=self.macd_fast,
window_sign=self.macd_signal
)
df['macd'] = macd_indicator.macd()
df['macd_signal'] = macd_indicator.macd_signal()
df['macd_diff'] = macd_indicator.macd_diff()
# ATR - Average True Range
df['atr'] = ta.volatility.AverageTrueRange(
high=df['high'],
low=df['low'],
close=df['close'],
window=self.atr_period
).average_true_range()
# Support e Resistance dinamici (50 periodi)
df['support'] = df['low'].rolling(window=50, min_periods=1).min()
df['resistance'] = df['high'].rolling(window=50, min_periods=1).max()
return df
def analyze(self, df):
"""
Analizza i dati e genera segnali di trading.
Args:
df (DataFrame): DataFrame con dati OHLC
Returns:
dict: Segnale di trading o None
"""
# Calcola indicatori
df = self.calculate_indicators(df)
# Verifica che ci siano abbastanza dati
if len(df) < max(self.rsi_period, self.macd_slow, self.atr_period) + 10:
print("  Dati insufficienti per l'analisi")
return None
# Prendi gli ultimi due valori per confronto
current = df.iloc[-1]
previous = df.iloc[-2]
# Verifica che gli indicatori siano validi (non NaN)
if pd.isna(current['rsi']) or pd.isna(current['macd_diff']) or pd.isna(current['atr']):
print("  Indicatori non validi (NaN)")
return None
signal = None
# ============================================
# LOGICA SEGNALE LONG (ACQUISTO)
# ============================================
if (current['rsi'] < 35 and previous['rsi'] >= 35 and # RSI entra in ipervenduto
current['macd_diff'] > 0 and previous['macd_diff'] <= 0 and # MACD incrocia al current['close'] > current['open']): # Candela rialzista
entry_price = current['close']
atr_value = current['atr']
# Calcola Stop Loss e Take Profit
stop_loss = entry_price - (atr_value * self.atr_sl_multiplier)
take_profit = entry_price + (atr_value * self.atr_tp_multiplier)
# Calcola Risk/Reward
risk = entry_price - stop_loss
reward = take_profit - entry_price
rr_ratio = reward / risk if risk > 0 else 0
# Determina confidenza del segnale
confidence = 'ALTA' if current['rsi'] < 30 else 'MEDIA'
signal = {
'type': 'LONG',
'entry': round(entry_price, 5),
'stop_loss': round(stop_loss, 5),
'take_profit': round(take_profit, 5),
'rsi': round(current['rsi'], 2),
'macd': round(current['macd'], 5),
'atr': round(atr_value, 5),
'confidence': confidence,
'rr_ratio': round(rr_ratio, 2),
'support': round(current['support'], 5),
'resistance': round(current['resistance'], 5)
}
# ============================================
# LOGICA SEGNALE SHORT (VENDITA)
# ============================================
elif (current['rsi'] > 65 and previous['rsi'] <= 65 and # RSI entra in ipercomprato
current['macd_diff'] < 0 and previous['macd_diff'] >= 0 and # MACD incrocia al current['close'] < current['open']): # Candela ribassista
entry_price = current['close']
atr_value = current['atr']
# Calcola Stop Loss e Take Profit
stop_loss = entry_price + (atr_value * self.atr_sl_multiplier)
take_profit = entry_price - (atr_value * self.atr_tp_multiplier)
# Calcola Risk/Reward
risk = stop_loss - entry_price
reward = entry_price - take_profit
rr_ratio = reward / risk if risk > 0 else 0
# Determina confidenza del segnale
confidence = 'ALTA' if current['rsi'] > 70 else 'MEDIA'
signal = {
'type': 'SHORT',
'entry': round(entry_price, 5),
'stop_loss': round(stop_loss, 5),
'take_profit': round(take_profit, 5),
'rsi': round(current['rsi'], 2),
'macd': round(current['macd'], 5),
'atr': round(atr_value, 5),
'confidence': confidence,
'rr_ratio': round(rr_ratio, 2),
'support': round(current['support'], 5),
'resistance': round(current['resistance'], 5)
}
return signal
def get_market_condition(self, df):
"""
Determina la condizione generale del mercato.
Returns:
str: 'BULLISH', 'BEARISH', o 'NEUTRAL'
"""
df = self.calculate_indicators(df)
current = df.iloc[-1]
if current['macd_diff'] > 0 and current['rsi'] < 50:
return 'BULLISH'
elif current['macd_diff'] < 0 and current['rsi'] > 50:
return 'BEARISH'
else:
return 'NEUTRAL'