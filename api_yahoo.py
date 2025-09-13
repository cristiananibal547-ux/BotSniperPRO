import yfinance as yf

def precio_yahoo(symbol="EURUSD=X"):
    try:
        data = yf.download(symbol, period="1d", interval="1m")
        ultimo = data["Close"].iloc[-1]
        return round(float(ultimo), 5)
    except Exception as e:
        return f"Error obteniendo {symbol}: {e}"
