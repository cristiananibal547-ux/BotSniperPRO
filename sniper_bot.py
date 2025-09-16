import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Menú principal
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📈 Divisas", callback_data="divisas")],
        [InlineKeyboardButton("⚡ Scalping (5s / 10s)", callback_data="scalping")],
        [InlineKeyboardButton("⏱️ Operaciones en Minutos", callback_data="minutos")],
        [InlineKeyboardButton("❌ Salir", callback_data="exit")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bienvenido a *SniperTradingBot PRO* ⚡",
                                    parse_mode="Markdown",
                                    reply_markup=main_menu())

# Botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "divisas":
        keyboard = [
            [InlineKeyboardButton("EUR/USD", callback_data="eurusd")],
            [InlineKeyboardButton("USD/JPY", callback_data="usdjpy")],
            [InlineKeyboardButton("GBP/USD", callback_data="gbpusd")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_main")]
        ]
        await query.edit_message_text("📊 Elegí una divisa:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "scalping":
        keyboard = [
            [InlineKeyboardButton("⚡ 5 segundos", callback_data="scalp_5s")],
            [InlineKeyboardButton("⚡ 10 segundos", callback_data="scalp_10s")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_main")]
        ]
        await query.edit_message_text("⚡ Modo Scalping:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "minutos":
        keyboard = [
            [InlineKeyboardButton("1 Minuto", callback_data="min_1")],
            [InlineKeyboardButton("5 Minutos", callback_data="min_5")],
            [InlineKeyboardButton("15 Minutos", callback_data="min_15")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_main")]
        ]
        await query.edit_message_text("⏱️ Modo en Minutos:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "volver_main":
        await query.edit_message_text("📋 Menú principal:", reply_markup=main_menu())

    elif query.data == "exit":
        await query.edit_message_text("👋 Gracias por usar *SniperTradingBot PRO*")

    else:
        await query.edit_message_text(f"👉 Elegiste: {query.data}", reply_markup=main_menu())

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🚀 SniperTradingBot PRO corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
