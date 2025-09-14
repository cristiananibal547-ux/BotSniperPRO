import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# === Cargar variables de entorno ===
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Función start con menú principal ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🤖 Bienvenido a *Bot Sniper PRO* 🚀\n\n"
        "Analizo más de 26 parámetros de análisis técnico 24/7 📊.\n\n"
        "👉 Elegí una opción del menú:"
    )
    reply_markup = main_menu()
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# === Menú principal ===
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📈 Monedas", callback_data="menu_monedas"),
         InlineKeyboardButton("💰 Criptomonedas", callback_data="menu_crypto")],
        [InlineKeyboardButton("📊 Acciones", callback_data="menu_acciones"),
         InlineKeyboardButton("🌍 Índices", callback_data="menu_indices")],
        [InlineKeyboardButton("⚡ Scalping 5s", callback_data="scalping_5s"),
         InlineKeyboardButton("⚡ Scalping 10s", callback_data="scalping_10s")],
        [InlineKeyboardButton("❓ Soporte", callback_data="menu_soporte")]
    ]
    return InlineKeyboardMarkup(keyboard)

# === Callback para manejar menús y señales ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("menu_"):
        menu = query.data
        await query.edit_message_text(
            text=f"📌 Elegiste: {menu.replace('menu_', '').capitalize()}",
            reply_markup=main_menu()
        )

    elif query.data.startswith("scalping_"):
        tiempo = query.data.replace("scalping_", "")
        await query.edit_message_text(
            text=f"⚡ Activado modo scalping a {tiempo} ⏱",
            reply_markup=main_menu()
        )

    elif query.data == "menu_soporte":
        await query.edit_message_text(
            text="📞 Contacto de soporte: @TuUsuarioSoporte",
            reply_markup=main_menu()
        )

# === Main ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("🚀 Bot Sniper PRO corriendo en modo sniper 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
