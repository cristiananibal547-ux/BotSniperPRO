from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from menu_divisas import obtener_menu_divisas
from estrategias import analizar_senal
from api_yahoo import precio_yahoo
from api_news import ultimas_noticias
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Monedas", callback_data="menu_monedas"),
         InlineKeyboardButton("Criptomonedas", callback_data="menu_cripto")],
        [InlineKeyboardButton("Acciones", callback_data="menu_acciones"),
         InlineKeyboardButton("Índices", callback_data="menu_indices")],
        [InlineKeyboardButton("Scalping 5s/10s ⚡", callback_data="menu_scalping")],
        [InlineKeyboardButton("📢 Noticias", callback_data="menu_news")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Bienvenido a **Sniper PRO Bot** ⚔️📊\n"
                                    "Analizo +26 parámetros técnicos y noticias 24/7 🚀",
                                    reply_markup=reply_markup)

# === Precios ===
async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Uso: /precio EURUSD=X")
        return
    symbol = context.args[0]
    resultado = precio_yahoo(symbol)
    await update.message.reply_text(f"📊 Precio de {symbol}: {resultado}")

# === Noticias ===
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = ultimas_noticias()
    await update.message.reply_text(f"📰 Noticias recientes:\n{resultado}")

# === Botón handler ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("menu_"):
        menu = obtener_menu_divisas(data)
        await query.edit_message_text("📌 Elegí una opción:", reply_markup=menu)

    elif data.startswith("scalping_"):
        tiempo = data.split("_")[1]
        resultado = analizar_senal("AUD/CHF", tiempo)  # ejemplo
        await query.edit_message_text(resultado)

    elif data == "menu_news":
        resultado = ultimas_noticias()
        await query.edit_message_text(f"📰 Noticias recientes:\n{resultado}")

# === Main ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Sniper PRO corriendo 24/7 en modo sniper...")
    app.run_polling()

if __name__ == "__main__":
    main()
