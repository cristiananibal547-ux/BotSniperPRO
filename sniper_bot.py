import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

# ====== Menú principal ======
def main_menu():
    keyboard = [
        [InlineKeyboardButton("⚡ Scalping (segundos)", callback_data="scalping")],
        [InlineKeyboardButton("⏱ Operaciones en minutos", callback_data="minutos")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== Menú scalping ======
def scalping_menu():
    keyboard = [
        [InlineKeyboardButton("5 segundos", callback_data="op_5s")],
        [InlineKeyboardButton("10 segundos", callback_data="op_10s")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="volver_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== Menú minutos ======
def minutos_menu():
    keyboard = [
        [InlineKeyboardButton("1 minuto", callback_data="op_1m")],
        [InlineKeyboardButton("3 minutos", callback_data="op_3m")],
        [InlineKeyboardButton("5 minutos", callback_data="op_5m")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="volver_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== Comando /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bienvenido a *Bot Sniper PRO*.\nSeleccioná el modo de operación:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ====== Manejador de botones ======
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "scalping":
        await query.edit_message_text("⚡ *Modo Scalping*: Elegí el tiempo:", 
                                      reply_markup=scalping_menu(), parse_mode="Markdown")

    elif query.data == "minutos":
        await query.edit_message_text("⏱ *Modo Minutos*: Elegí el tiempo:", 
                                      reply_markup=minutos_menu(), parse_mode="Markdown")

    elif query.data.startswith("op_"):
        await query.edit_message_text(f"✅ Operación configurada en: {query.data.replace('op_', '')}")

    elif query.data == "volver_main":
        await query.edit_message_text("🚀 Menú principal: elegí el modo de operación:", 
                                      reply_markup=main_menu(), parse_mode="Markdown")

# ====== Main ======
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
