import requests
import os

API_KEY_NEWS = os.getenv("NEWS_API_KEY")

def ultimas_noticias():
    try:
        url = f"https://newsapi.org/v2/top-headlines?language=es&apiKey={API_KEY_NEWS}"
        r = requests.get(url)
        data = r.json()
        if "articles" not in data:
            return "No se encontraron noticias."
        titulos = [art["title"] for art in data["articles"][:5]]
        return "\n".join(titulos)
    except Exception as e:
        return f"Error obteniendo noticias: {e}"