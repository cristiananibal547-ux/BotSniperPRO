import os
import threading
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


# ------------------------------
# Menú principal
# ------------------------------
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📈 Divisas", callback_data="divisas")],
        [InlineKeyboardButton("⚡ Scalping (5s / 10s)", callback_data="scalping")],
        [InlineKeyboardButton("⏱️ Operaciones en Minutos", callback_data="minutos")],
        [InlineKeyboardButton("❌ Salir", callback_data="exit")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ------------------------------
# Comando /start
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bienvenida = (
        "🤖 ¡Bienvenido a *SniperTradingBot PRO*! ⚡\n\n"
        "🚀 Este bot te ayudará con:\n"
        "• 📊 Cotizaciones en tiempo real\n"
        "• 📰 Noticias y alertas económicas\n"
        "• 🎯 Estrategias rápidas para trading\n\n"
        "⚡ Disponible 24/7 gracias a la nube.\n\n"
        "👉 Usá el menú de abajo para comenzar."
    )

    await update.message.reply_text(
        bienvenida,
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


# ------------------------------
# Handler de botones
# ------------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "divisas":
        keyboard = [
            [InlineKeyboardButton("🇪🇺 EUR/USD", callback_data="eurusd")],
            [InlineKeyboardButton("🇺🇸 USD/JPY", callback_data="usdjpy")],
            [InlineKeyboardButton("🇬🇧 GBP/USD", callback_data="gbpusd")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_main")],
        ]
        await query.edit_message_text("📊 Elegí una divisa:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "scalping":
        keyboard = [
            [InlineKeyboardButton("⚡]()
