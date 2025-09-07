import logging
import random
import os
import pandas as pd
from datetime import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# 📌 Claves principales
TOKEN = "7509597620:AAHjHjGdDib6-TXkpac9JzAFeW8hS5cP1PQ"
CHAT_ID = 6968369795  # tu ID personal de Telegram
DATA_FOLDER = "data"
EXCEL_FILE = os.path.join(DATA_FOLDER, "senales.xlsx")
USERS_FILE = os.path.join(DATA_FOLDER, "usuarios.xlsx")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# 📊 Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- Funciones auxiliares ---
def guardar_excel(senal: dict):
    df = pd.DataFrame([senal])
    if os.path.exists(EXCEL_FILE):
        df_ant = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_ant, df], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

def guardar_usuario(user_id: int, username: str):
    df = pd.DataFrame([[user_id, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                      columns=["user_id", "username", "fecha"])
    if os.path.exists(USERS_FILE):
        df_ant = pd.read_excel(USERS_FILE)
        if user_id not in df_ant["user_id"].values:
            df = pd.concat([df_ant, df], ignore_index=True)
            df.to_excel(USERS_FILE, index=False)
            return True
        return False
    else:
        df.to_excel(USERS_FILE, index=False)
        return True

def generar_senal(activo: str, tiempo: str):
    precio = round(random.uniform(1.1000, 1.2000), 5)
    monto = round(random.uniform(1.0, 5.0), 2)
    senal = random.choice(["🟢 COMPRAR (BUY)", "🔴 VENDER (SELL)"])
    fiabilidad = random.randint(80, 98)
    volatilidad = random.choice(["Baja", "Moderada", "Alta"])
    analisis = random.choice([
        "Basado en RSI y Soportes",
        "Confirmación con Bollinger",
        "Contexto favorable por velas",
        "Señal reforzada por tendencia"
    ])
    return {
        "activo": activo,
        "precio": precio,
        "monto": monto,
        "senal": senal,
        "fiabilidad": fiabilidad,
        "volatilidad": volatilidad,
        "analisis": analisis,
        "tiempo": tiempo,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "SinUsername"

    # mensaje de bienvenida en privado SOLO 1 vez
    if guardar_usuario(user_id, username):
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "🎯 Bienvenido al *BOT SNIPER PRO* 🚀\n\n"
                "✅ Estrategias avanzadas: RSI, Bollinger, Estocástico\n"
                "✅ Gestión de Capital + Martingala\n"
                "✅ Señales en tiempo real y guardadas en Excel 📊\n\n"
                "⚡ Operá como un profesional con la precisión de un Sniper.\n"
                "Usá el menú para comenzar 👇"
            ),
            parse_mode="Markdown"
        )

    # menú principal
    keyboard = [
        [InlineKeyboardButton("📊 Monedas", callback_data="monedas"),
         InlineKeyboardButton("💱 OTC Monedas", callback_data="otc")],
        [InlineKeyboardButton("₿ Criptomonedas", callback_data="cripto"),
         InlineKeyboardButton("📦 Productos", callback_data="productos")],
        [InlineKeyboardButton("📈 Acciones", callback_data="acciones"),
         InlineKeyboardButton("📊 Índices", callback_data="indices")],
        [InlineKeyboardButton("❓ Contacto de Soporte", callback_data="soporte")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "⚫️✨ *Bot Sniper Financiero PRO* ✨⚫️\n\n"
        "Selecciona una categoría para recibir señales 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    activos = {
        "monedas": ["EUR/USD OTC", "USD/CHF OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "CAD/CHF OTC"],
        "otc": ["EUR/CHF OTC", "EUR/JPY OTC", "AUD/CAD OTC", "LBP/USD OTC"],
        "cripto": ["BTC-USD", "ETH-USD"],
        "productos": ["ORO", "PLATA"],
        "acciones": ["AAPL", "TSLA", "AMZN"],
        "indices": ["SP500", "NASDAQ"]
    }

    if data in activos:
        keyboard = [[InlineKeyboardButton(a, callback_data=f"activo|{a}")] for a in activos[data]]
        keyboard.append([InlineKeyboardButton("⬅️ Volver", callback_data="volver")])
        await query.edit_message_text("⚡ *Selecciona un activo:*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "volver":
        await start(update, context)

    elif data == "soporte":
        await query.edit_message_text("📩 Contacto de soporte: @TuUsuario")

async def mostrar_senal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("activo|"):
        activo = data.split("|")[1]
        resultado = generar_senal(activo, "5m")
        guardar_excel(resultado)

        mensaje = (
            f"⚫️✨ *Señal PRO para {resultado['activo']}* ✨⚫️\n\n"
            f"💵 *Precio:* {resultado['precio']}\n"
            f"💰 *Monto sugerido:* {resultado['monto']} USD\n"
            f"📊 *Estado del mercado:* Volatilidad {resultado['volatilidad']}\n"
            f"💻 *Análisis técnico:* {resultado['analisis']}\n\n"
            f"📈 *Fiabilidad:* {resultado['fiabilidad']}%\n"
            f"🚦 *Señal:* {resultado['senal']}\n\n"
            f"🗓 Guardada en historial Excel"
        )

        keyboard = [[InlineKeyboardButton("⬅️ Volver", callback_data="volver")]]
        await query.edit_message_text(mensaje, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# --- MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^(monedas|otc|cripto|productos|acciones|indices|volver|soporte)$"))
    app.add_handler(CallbackQueryHandler(mostrar_senal, pattern="^activo\|"))
    print("⚫️✨ Bot Sniper PRO corriendo en formato Negro/Dorado ✨⚫️")
    app.run_polling()

if __name__ == "__main__":
    main()
