import yfinance as yf

def precio_yahoo(symbol="EURUSD=X"):
    """
    Devuelve el último precio de un activo usando Yahoo Finance.
    - EURUSD=X → divisas
    - AAPL → acciones Apple
    - BTC-USD → Bitcoin
    """
    try:
        data = yf.download(symbol, period="1d", interval="1m")
        ultimo = data["Close"].iloc[-1]
        return round(float(ultimo), 5)
    except Exception as e:
        return f"Error obteniendo {symbol}: {e}"

# Ejemplo de uso:
if __name__ == "__main__":
    print("EUR/USD:", precio_yahoo("EURUSD=X"))
    print("Apple:", precio_yahoo("AAPL"))
    print("Bitcoin:", precio_yahoo("BTC-USD"))
