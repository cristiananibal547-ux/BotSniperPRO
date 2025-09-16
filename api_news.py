import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def obtener_noticias(query="trading"):
    url = f"https://newsapi.org/v2/everything?q={query}&language=es&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            return f"Error en la API de noticias: {data.get('message', 'Desconocido')}"

        articulos = data.get("articles", [])[:5]  # Trae solo las 5 últimas noticias
        if not articulos:
            return "No se encontraron noticias recientes."

        resultado = "📰 Últimas Noticias:\n\n"
        for art in articulos:
            resultado += f"- {art['title']} ({art['source']['name']})\n"

        return resultado
    except Exception as e:
        return f"Error obteniendo noticias: {e}"
