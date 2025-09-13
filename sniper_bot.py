import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from api_yahoo import precio_yahoo
from api_news import ultimas_noticias

# === Configuración ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === Comando /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 BotSniperPRO activo 24/7. Usá /precio para ver un activo o /noticias para últimas noticias.")

# === Comando /precio ===
async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("📌 Uso: /precio EURUSD=X")
        return
    symbol = context.args[0]
    resultado = precio_yahoo(symbol)
    await update.message.reply_text(f"💹 Precio de {symbol}: {resultado}")

# === Comando /noticias ===
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = ultimas_noticias()
    await update.message.reply_text(f"📰 Noticias recientes:\n{resultado}")

# === Botón handler (si lo necesitás después) ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Botón presionado 🚀")

# === Main ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot corriendo en modo sniper 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
