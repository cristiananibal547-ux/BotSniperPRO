<<<<<<< HEAD
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
=======
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from menu_divisas import obtener_menu_divisas
from estrategias import analizar_senal

# Configuración básica
logging.basicConfig(level=logging.INFO)
TOKEN = "7509597620:AAHjHjGdDib6-TXkpac9JzAFeW8hS5cP1PQ"

# 🎯 MENÚ PRINCIPAL
def main_menu():
    keyboard = [
        [InlineKeyboardButton("💱 Divisas", callback_data="menu_monedas"),
         InlineKeyboardButton("₿ Criptos", callback_data="menu_cripto")],
        [InlineKeyboardButton("📈 Acciones", callback_data="menu_acciones"),
         InlineKeyboardButton("🌍 Índices", callback_data="menu_indices")],
        [InlineKeyboardButton("⚡ Scalping", callback_data="menu_scalping")]
    ]
    return InlineKeyboardMarkup(keyboard)

# 🚀 Mensaje de bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    welcome_message = (
        f"🎯 Bienvenido {user} a **SNIPER PRO BOT** 🔥\n\n"
        "📊 El asistente financiero diseñado para dar **señales claras y fáciles de operar** en trading.\n"
        "⚡ Podés elegir activos (divisas, criptos, acciones, índices) o el modo **Scalping Sniper 5s / 10s**.\n\n"
        "✅ Cualquiera puede usarlo, incluso sin experiencia. "
        "El objetivo es que todos puedan ganar de forma simple 💵.\n\n"
        "👉 Elegí una opción del menú:"
    )
    await update.message.reply_text(welcome_message, reply_markup=main_menu())

# 🎯 Callback para manejar menús y señales
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("menu_"):
        menu = query.data
        await query.edit_message_text(
            text="📋 Elegí un activo:",
            reply_markup=obtener_menu_divisas(menu)
        )

    elif query.data.startswith("scalping_"):
        par = query.data.replace("scalping_", "")
        tiempo = "Scalping 5s" if par == "5s" else "Scalping 10s" if par == "10s" else "1 min"
        senal = analizar_senal(par, tiempo)
        await query.edit_message_text(senal, reply_markup=main_menu())

    elif query.data == "menu_main":
        await query.edit_message_text("📋 Menú principal:", reply_markup=main_menu())
>>>>>>> 7c10417b3077f9d3042102bad8f30a4566e67a75

# 🚀 Lanzar bot
def main():
<<<<<<< HEAD
    if not TELEGRAM_TOKEN:
        raise ValueError("❌ No se encontró TELEGRAM_TOKEN. Configuralo en tu .env o en Render.")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot Sniper PRO corriendo 24/7...")
=======
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
>>>>>>> 7c10417b3077f9d3042102bad8f30a4566e67a75
    app.run_polling()

if __name__ == "__main__":
    main()
