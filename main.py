import asyncio
import schedule
import time
from datetime import datetime
import pytz
import config
from data_fetcher import ForexDataFetcher
from strategy import TradingStrategy
from telegram_bot import TelegramNotifier
class ForexTradingBot:
"""
Bot principale per il trading forex automatizzato.
"""
def __init__(self):
self.data_fetcher = ForexDataFetcher()
self.strategy = TradingStrategy()
self.notifier = TelegramNotifier()
self.signals_today = 0
self.last_signal_date = None
print("\n" + "="*70)
print("  FOREX AI TRADING BOT - INIZIALIZZAZIONE")
print("="*70)
print(f"  Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"  Coppie: {', '.join(config.FOREX_PAIRS)}")
print(f"  Analisi: Ogni ora")
print(f"  Segnali max/giorno: {config.MAX_SIGNALS_PER_DAY}")
print(f"  API: Alpha Vantage (dati reali)")
print("="*70 + "\n")
def is_trading_hours(self):
"""
Verifica se siamo in orario di trading.
Returns:
bool: True se è orario di trading
"""
now = datetime.now()
current_hour = now.hour
# Verifica se siamo nell'orario configurato
if current_hour < config.TRADING_START_HOUR or current_hour >= config.TRADING_END_HOUR:
return False
# Verifica se è weekend (sabato=5, domenica=6)
if now.weekday() >= 5:
return False
return True
def reset_daily_counter(self):
"""
Resetta il contatore giornaliero dei segnali.
"""
today = datetime.now().date()
if self.last_signal_date != today:
self.signals_today = 0
self.last_signal_date = today
print(f"  Contatore segnali resettato per {today}")
async def analyze_markets(self):
"""
Analizza tutti i mercati forex e genera segnali.
Questa è la funzione principale chiamata ogni ora.
"""
print("\n" + "="*70)
print(f"  ANALISI MERCATI - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*70)
# Reset contatore giornaliero se è un nuovo giorno
self.reset_daily_counter()
# Verifica orario di trading
if not self.is_trading_hours():
print("  Fuori orario di trading - analisi saltata")
print(f" Orario operativo: {config.TRADING_START_HOUR}:00 - {config.TRADING_END_print("="*70 + "\n")
return
# Verifica se abbiamo raggiunto il limite giornaliero
if self.signals_today >= config.MAX_SIGNALS_PER_DAY:
print(f"  Limite giornaliero raggiunto ({config.MAX_SIGNALS_PER_DAY} segnali)")
print("="*70 + "\n")
return
signals_sent_this_cycle = 0
# Analizza ogni coppia forex
for pair in config.FOREX_PAIRS:
try:
# Verifica se possiamo ancora inviare segnali
if self.signals_today >= config.MAX_SIGNALS_PER_DAY:
print(f"  Limite segnali raggiunto, salto {pair}")
break
print(f"\n  Analizzando {pair}...")
# 1. Recupera dati reali da Alpha Vantage
df = self.data_fetcher.get_data_for_analysis(
pair=pair,
bars=config.DATA_POINTS
)
if df is None or len(df) < 50:
print(f"   Dati insufficienti per {pair}")
continue
# 2. Analizza con la strategia
signal = self.strategy.analyze(df)
# 3. Se c'è un segnale valido, invialo
if signal:
print(f"   SEGNALE {signal['type']} rilevato!")
print(f" Entry: {signal['entry']}")
print(f" TP: {signal['take_profit']}")
print(f" SL: {signal['stop_loss']}")
print(f" R/R: 1:{signal['rr_ratio']}")
# Invia su Telegram
await self.notifier.send_signal(pair, signal)
self.signals_today += 1
signals_sent_this_cycle += 1
# Piccola pausa tra un segnale e l'altro
await asyncio.sleep(2)
else:
print(f"   Nessun segnale per {pair}")
except Exception as e:
print(f"   Errore analizzando {pair}: {e}")
await self.notifier.send_error_notification(f"Errore su {pair}: {str(e)}")
# Riepilogo del ciclo
print(f"\n{'='*70}")
if signals_sent_this_cycle > 0:
print(f"  Ciclo completato: {signals_sent_this_cycle} segnali inviati")
else:
print("  Ciclo completato: nessun segnale generato")
print(f"  Segnali oggi: {self.signals_today}/{config.MAX_SIGNALS_PER_DAY}")
print(f"{'='*70}\n")
async def start(self):
"""
Avvia il bot e inizia il loop principale.
"""
# Invia messaggio di avvio su Telegram
if config.ENABLE_STARTUP_MESSAGE:
await self.notifier.send_startup_message()
# Prima analisi immediata
print("  Eseguo la prima analisi...")
await self.analyze_markets()
# Schedula analisi oraria
schedule.every().hour.at(":00").do(
lambda: asyncio.create_task(self.analyze_markets())
)
print("  Bot in esecuzione... (Ctrl+C per fermare)")
print(f"  Prossima analisi: {datetime.now().replace(minute=0, second=0, microsecond=# Loop principale
while True:
schedule.run_pending()
await asyncio.sleep(60) # Controlla ogni minuto
def main():
"""
Funzione principale.
"""
try:
bot = ForexTradingBot()
asyncio.run(bot.start())
except KeyboardInterrupt:
print("\n\n  Bot fermato dall'utente")
except Exception as e:
print(f"\n\n  Errore critico: {e}")
import traceback
traceback.print_exc()
if __name__ == "__main__":
main()