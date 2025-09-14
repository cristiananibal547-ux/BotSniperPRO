import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Comando /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ¡Bienvenido a *Bot Sniper PRO*! 🚀\n\n"
        "📊 Estoy listo para analizar y darte señales 24/7.\n"
        "👉 Usá /precio EURUSD=X para ver precios en vivo\n"
        "👉 Usá /noticias para ver últimas noticias del mercado"
    )

# === Comando /precio ===
async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Uso: /precio EURUSD=X")
        return

    symbol = context.args[0]
    # Acá deberías llamar a tu función de análisis de precios
    resultado = f"Precio simulado de {symbol}: 1.2345"
    await update.message.reply_text(f"📈 {resultado}")

# === Comando /noticias ===
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Acá deberías integrar con tu función de noticias reales
    resultado = "Ejemplo de noticia: El mercado se mantiene volátil 📉📈"
    await update.message.reply_text(f"📰 Noticias:\n{resultado}")

# === Handler de botones (si después usás inline keyboards) ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Botón presionado 🎯")

# === Main ===
def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("❌ No se encontró TELEGRAM_TOKEN. Configuralo en tu .env o en Render.")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot Sniper PRO corriendo 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
