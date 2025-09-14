import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# === Cargar variables de entorno ===
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Configuración de logs ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === MENÚ PRINCIPAL ===
def main_menu():
    keyboard = [
        [InlineKeyboardButton("⚡ Scalping (segundos)", callback_data="scalping")],
        [InlineKeyboardButton("⏱ Operaciones en minutos", callback_data="minutos")],
        [InlineKeyboardButton("📊 Divisas", callback_data="menu_monedas")],
        [InlineKeyboardButton("🛠 Soporte", callback_data="menu_soporte")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === Comando /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🤖 Bienvenido a *Bot Sniper PRO* 🚀\n\n"
        "Seleccioná el modo de operación:"
    )
    await update.message.reply_text(welcome_message, reply_markup=main_menu())

# === Manejo de botones ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "scalping":
        await query.edit_message_text(
            text="⚡ Activado modo *Scalping en segundos*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

    elif query.data == "minutos":
        await query.edit_message_text(
            text="⏱ Activado modo *Operaciones en minutos*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

    elif query.data == "menu_monedas":
        await query.edit_message_text(
            text="📊 Próximamente: señales en divisas.",
            reply_markup=main_menu()
        )

    elif query.data == "menu_soporte":
        await query.edit_message_text(
            text="🛠 Contacto de soporte: @TuUsuarioSoporte",
            reply_markup=main_menu()
        )

# === MAIN ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    logging.info("✅ Bot Sniper PRO corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
