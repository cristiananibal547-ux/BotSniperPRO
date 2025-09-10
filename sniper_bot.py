import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Cargar el token desde las variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Bot Sniper PRO activo y corriendo en Render 24/7.")

# Comando de prueba /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong ✅")

def main():
    # Crear aplicación del bot
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    # Usar long polling
    app.run_polling()

if __name__ == "__main__":
    main()
