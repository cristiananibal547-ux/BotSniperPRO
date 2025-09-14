import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# === Configuración ===
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Falta configurar TELEGRAM_TOKEN en .env o en Render Environment")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === Menú principal ===
def main_menu():
    keyboard = [
        [InlineKeyboardButton("⚡ Scalping (segundos)", callback_data="menu_scalping")],
        [InlineKeyboardButton("⏱ Operaciones en minutos", callback_data="menu_minutos")],
        [InlineKeyboardButton("📞 Soporte", callback_data="menu_soporte")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bienvenido a *Bot Sniper PRO*.\nSeleccioná el modo de operación:",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )

# === Callbacks ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_scalping":
        await query.edit_message_text("⚡ Modo Scalping activado (segundos).", reply_markup=main_menu())
    elif query.data == "menu_minutos":
        await query.edit_message_text("⏱ Modo Operaciones en minutos activado.", reply_markup=main_menu())
    elif query.data == "menu_soporte":
        await query.edit_message_text("📞 Contacto de soporte: @TuUsuarioSoporte", reply_markup=main_menu())

# === Main ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
