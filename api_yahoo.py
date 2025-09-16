import yfinance as yf

def precio_yahoo(symbol="EURUSD=X"):
    """
    Devuelve el último precio de un símbolo de Yahoo Finance.
    Ejemplo: EURUSD=X para divisas, AAPL para acciones, BTC-USD para crypto.
    """
    try:
        data = yf.download(symbol, period="1d", interval="1m")
        if data.empty:
            return f"No hay datos disponibles para {symbol}"
        
        ultimo = data["Close"].iloc[-1]
        return round(float(ultimo), 5)
    except Exception as e:
        return f"Error obteniendo {symbol}: {e}"
