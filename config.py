import os
from dotenv import load_dotenv
# Carica variabili d'ambiente
load_dotenv()
# ============================================
# CONFIGURAZIONI API
# ============================================
# Telegram Bot
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'IL_TUO_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'IL_TUO_CHAT_ID')
# Alpha Vantage (dati forex reali)
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', 'LA_TUA_CHIAVE_API')
# ============================================
# COPPIE FOREX DA MONITORARE
# ============================================
FOREX_PAIRS = [
'EURUSD', # Euro / Dollaro USA
'GBPUSD', # Sterlina / Dollaro USA
'USDJPY', # Dollaro USA / Yen Giapponese
'AUDUSD', # Dollaro Australiano / Dollaro USA
'USDCHF' # Dollaro USA / Franco Svizzero
]
# ============================================
# PARAMETRI STRATEGIA DI TRADING
# ============================================
# RSI (Relative Strength Index)
RSI_PERIOD = 14 # Periodo di calcolo RSI
RSI_OVERSOLD = 30 # Soglia ipervenduto (segnale LONG)
RSI_OVERBOUGHT = 70 # Soglia ipercomprato (segnale SHORT)
# MACD (Moving Average Convergence Divergence)
MACD_FAST = 12 # EMA veloce
MACD_SLOW = 26 # EMA lenta
MACD_SIGNAL = 9 # Linea di segnale
# ATR (Average True Range) - Per Stop Loss e Take Profit
ATR_PERIOD = 14 # Periodo di calcolo ATR
ATR_MULTIPLIER_SL = 2.0 # Stop Loss = Prezzo ± (ATR × 2)
ATR_MULTIPLIER_TP = 3.0 # Take Profit = Prezzo ± (ATR × 3)
# Risk/Reward Ratio risultante: 1:1.5
# ============================================
# CONFIGURAZIONI OPERATIVE
# ============================================
MAX_SIGNALS_PER_DAY = 3 # Massimo 3 segnali al giorno
ANALYSIS_INTERVAL = 3600 # Analisi ogni 1 ora (in secondi)
DATA_POINTS = 100 # Numero di candele da analizzare
# ============================================
# FILTRI TEMPORALI
# ============================================
# Evita trading durante orari con spread alto o liquidità bassa
TRADING_START_HOUR = 8 # Inizia alle 8:00 (ora locale)
TRADING_END_HOUR = 22 # Termina alle 22:00 (ora locale)
# ============================================
# CONFIGURAZIONI LOGGING
# ============================================
LOG_LEVEL = 'INFO' # Livello di logging (DEBUG, INFO, WARNING, ERROR)
ENABLE_STARTUP_MESSAGE = True # Invia messaggio su Telegram all'avvio