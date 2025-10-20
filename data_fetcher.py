import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import config
class ForexDataFetcher:
"""
Classe per recuperare dati forex in tempo reale da Alpha Vantage.
"""
def __init__(self):
self.api_key = config.ALPHA_VANTAGE_KEY
self.base_url = "https://www.alphavantage.co/query"
self.call_count = 0
self.last_call_time = None
def _rate_limit(self):
"""
Implementa rate limiting per rispettare i limiti API:
- 5 chiamate al minuto
- Aspetta 12 secondi tra una chiamata e l'altra
"""
if self.last_call_time:
elapsed = time.time() - self.last_call_time
if elapsed < 12: # 12 secondi = 5 chiamate/minuto
sleep_time = 12 - elapsed
print(f"  Rate limit: attendo {sleep_time:.1f} secondi...")
time.sleep(sleep_time)
self.last_call_time = time.time()
self.call_count += 1
def get_forex_data(self, pair, interval='60min', outputsize='compact'):
"""
Recupera dati forex da Alpha Vantage.
Args:
pair (str): Coppia forex (es: 'EURUSD')
interval (str): Timeframe ('1min', '5min', '15min', '30min', '60min')
outputsize (str): 'compact' (100 punti) o 'full' (anni di dati)
Returns:
pandas.DataFrame: DataFrame con colonne [timestamp, open, high, low, close, volume]
"""
# Applica rate limiting
self._rate_limit()
# Costruisci parametri API
from_symbol = pair[:3] # Es: EUR
to_symbol = pair[3:] # Es: USD
params = {
'function': 'FX_INTRADAY',
'from_symbol': from_symbol,
'to_symbol': to_symbol,
'interval': interval,
'apikey': self.api_key,
'outputsize': outputsize,
'datatype': 'json'
}
try:
print(f"  Recuperando dati per {pair} da Alpha Vantage...")
# Effettua la richiesta
response = requests.get(self.base_url, params=params, timeout=30)
response.raise_for_status()
data = response.json()
# Controlla errori API
if 'Error Message' in data:
raise Exception(f"Errore API: {data['Error Message']}")
if 'Note' in data:
raise Exception(f"Limite API raggiunto: {data['Note']}")
# Estrai time series
time_series_key = f'Time Series FX ({interval})'
if time_series_key not in data:
raise Exception(f"Dati non disponibili. Risposta API: {data}")
time_series = data[time_series_key]
# Converti in DataFrame
records = []
for timestamp_str, values in time_series.items():
records.append({
'timestamp': pd.to_datetime(timestamp_str),
'open': float(values['1. open']),
'high': float(values['2. high']),
'low': float(values['3. low']),
'close': float(values['4. close']),
'volume': 0 # Forex non ha volume reale nel mercato spot
})
# Crea DataFrame e ordina per timestamp
df = pd.DataFrame(records)
df = df.sort_values('timestamp', ascending=True)
df = df.reset_index(drop=True)
print(f"  Recuperati {len(df)} dati per {pair}")
print(f" Periodo: {df['timestamp'].min()} → {df['timestamp'].max()}")
return df
except requests.exceptions.RequestException as e:
print(f"  Errore di rete: {e}")
return None
except Exception as e:
print(f"  Errore recupero dati per {pair}: {e}")
return None
def get_latest_price(self, pair):
"""
Ottiene il prezzo più recente di una coppia.
Returns:
float: Prezzo di chiusura più recente
"""
df = self.get_forex_data(pair, interval='60min', outputsize='compact')
if df is not None and len(df) > 0:
return df.iloc[-1]['close']
return None
def get_data_for_analysis(self, pair, bars=100):
"""
Recupera dati ottimizzati per l'analisi tecnica.
Args:
pair (str): Coppia forex
bars (int): Numero di candele necessarie
Returns:
pandas.DataFrame: DataFrame pronto per l'analisi
"""
# Alpha Vantage compact restituisce circa 100 punti
# Se servono più dati, usa 'full'
outputsize = 'full' if bars > 100 else 'compact'
df = self.get_forex_data(pair, interval='60min', outputsize=outputsize)
if df is not None and len(df) > 0:
# Restituisci gli ultimi N bars
return df.tail(bars).reset_index(drop=True)
return None
# Test della classe (eseguito solo se lanciato direttamente)
if __name__ == "__main__":
fetcher = ForexDataFetcher()
# Test su EURUSD
print("\n  TEST: Recupero dati EURUSD\n")
df = fetcher.get_data_for_analysis('EURUSD', bars=50)
if df is not None:
print("\n  Ultimi 5 dati:")
print(df.tail())
print(f"\n  Test completato con successo!")
else:
print("\n  Test fallito")