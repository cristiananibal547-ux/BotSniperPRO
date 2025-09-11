import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

# ===== Menú principal =====
def main_menu():
    keyboard = [
        [InlineKeyboardButton("⚡ Scalping (segundos)", callback_data="scalping")],
        [InlineKeyboardButton("⏱ Operaciones en minutos", callback_data="minutos")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== Menú scalping =====
def scalping_menu():
    keyboard = [
        [InlineKeyboardButton("5 segundos", callback_data="op_5s")],
        [InlineKeyboardButton("10 segundos", callback_data="op_10s")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="volver_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== Menú minutos =====
def minutos_menu():
    keyboard = [
        [InlineKeyboardButton("1 minuto", callback_data="op_1m")],
        [InlineKeyboardButton("3 minutos", callback_data="op_3m")],
        [InlineKeyboardButton("5 minutos", callback_data="op_5m")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="volver_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== Comando /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bienvenido a *Bot Sniper PRO*.\nSeleccioná el modo de operación:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ===== Manejo de botones =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "scalping":
        await query.edit_message_text("Seleccioná el tiempo de scalping:", reply_markup=scalping_menu())
    elif query.data == "minutos":
        await query.edit_message_text("Seleccioná el tiempo en minutos:", reply_markup=minutos_menu())
    elif query.data.startswith("op_"):
        await query.edit_message_text(f"✅ Opción seleccionada: {query.data}")
    elif query.data == "volver_main":
        await query.edit_message_text("📋 Menú principal:", reply_markup=main_menu())

# ===== Función principal =====
def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot corriendo en modo sniper 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
