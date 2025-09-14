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

# 🚀 Lanzar bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
