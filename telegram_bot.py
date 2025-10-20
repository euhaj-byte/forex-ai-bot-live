import asyncio
from telegram import Bot
from datetime import datetime
import config
class TelegramNotifier:
"""
Gestisce l'invio di notifiche su Telegram.
"""
def __init__(self):
self.bot = Bot(token=config.TELEGRAM_TOKEN)
self.chat_id = config.TELEGRAM_CHAT_ID
async def send_message(self, text, parse_mode='Markdown'):
"""
Invia un messaggio su Telegram.
Args:
text (str): Testo del messaggio
parse_mode (str): 'Markdown' o 'HTML'
"""
try:
await self.bot.send_message(
chat_id=self.chat_id,
text=text,
parse_mode=parse_mode
)
return True
except Exception as e:
print(f"  Errore invio messaggio Telegram: {e}")
return False
async def send_signal(self, pair, signal):
"""
Invia un segnale di trading formattato.
Args:
pair (str): Coppia forex (es: 'EURUSD')
signal (dict): Dizionario con dati del segnale
"""
# Emoji basato sul tipo di segnale
emoji = " " if signal['type'] == 'LONG' else " "
direction = "ACQUISTO" if signal['type'] == 'LONG' else "VENDITA"
# Formatta il messaggio
message = f"""
{emoji} **NUOVO SEGNALE {direction}** {emoji}
  **Coppia**: {pair}
  **Confidenza**: {signal['confidence']}
  **Risk/Reward**: 1:{signal['rr_ratio']}
**LIVELLI OPERATIVI**:
  Entry Price: `{signal['entry']}`
  Take Profit: `{signal['take_profit']}`
  Stop Loss: `{signal['stop_loss']}`
  **INDICATORI**:
• RSI: {signal['rsi']}
• MACD: {signal['macd']}
• ATR: {signal['atr']}
  **SUPPORTO/RESISTENZA**:
• Support: {signal['support']}
• Resistance: {signal['resistance']}
  **Orario**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
  **Come operare**:
1. Apri {direction} su {pair}
2. Imposta SL a {signal['stop_loss']}
3. Imposta TP a {signal['take_profit']}
4. Usa max 2% del capitale
  *Questo è un segnale automatizzato basato su analisi tecnica. Verifica sempre prima di entrare """
await self.send_message(message)
print(f"  Segnale {signal['type']} inviato per {pair}")
async def send_startup_message(self):
"""
Invia il messaggio di avvio del bot.
"""
message = """
  **BOT FOREX AI AVVIATO**  
  Il bot è ora attivo e operativo!
  **Configurazione**:
• **Coppie monitorate**: """ + ", ".join(config.FOREX_PAIRS) + """
• **Frequenza analisi**: Ogni ora
• **Segnali giornalieri**: Max """ + str(config.MAX_SIGNALS_PER_DAY) + """
• **Fonte dati**: Alpha Vantage (dati reali)
  **Strategia**:
• RSI + MACD + ATR
• Risk/Reward: 1:1.5
• Stop Loss dinamico
  **Orario operativo**: """ + f"{config.TRADING_START_HOUR}:00 - {config.TRADING_END_HOUR}:00"   Riceverai notifiche solo quando ci saranno opportunità di trading valide!
  **Ricorda**:
• Verifica sempre i segnali
• Usa solo account demo per i test
• Non rischiare più del 2% per trade
• Il trading comporta rischi di perdita
  Buon trading!
"""
await self.send_message(message)
print("  Messaggio di avvio inviato")
async def send_daily_summary(self, signals_sent, pairs_analyzed):
"""
Invia un riepilogo giornaliero.
Args:
signals_sent (int): Numero di segnali inviati oggi
pairs_analyzed (int): Numero di coppie analizzate
"""
message = f"""
  **RIEPILOGO GIORNALIERO**
  Segnali inviati: {signals_sent}
  Coppie analizzate: {pairs_analyzed}
  Data: {datetime.now().strftime('%d/%m/%Y')}
  Bot operativo e funzionante.
"""
await self.send_message(message)
async def send_error_notification(self, error_message):
"""
Invia una notifica di errore.
Args:
error_message (str): Descrizione dell'errore
"""
message = f"""
**ATTENZIONE - ERRORE BOT**
Si è verificato un errore:
`{error_message}`
Il bot continuerà a funzionare, ma controlla i logs su Render.
Orario: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
await self.send_message(message)