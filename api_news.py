import requests

# --- CONFIGURACIÓN ---
API_KEY = "2d812f1e7c8e46fc8e4e561e953fe8d3"
BASE_URL = "https://newsapi.org/v2/everything"

# --- FUNCIÓN PARA TRAER NOTICIAS ---
def obtener_noticias(query="trading"):
    """
    Consulta NewsAPI y devuelve noticias relacionadas con la palabra clave.
    query: palabra clave (ejemplo: "forex", "bitcoin", "acciones")
    """
    try:
        params = {
            "q": query,
            "language": "es",         # noticias en español
            "sortBy": "publishedAt",  # ordenar por fecha de publicación
            "apiKey": API_KEY
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return f"⚠️ Error obteniendo noticias: {data}"

        noticias = data.get("articles", [])[:5]  # solo 5 noticias más recientes
        resultado = []
        for noticia in noticias:
            titulo = noticia.get("title", "Sin título")
            url = noticia.get("url", "")
            resultado.append(f"📰 {titulo}\n🔗 {url}")

        return "\n\n".join(resultado)

    except Exception as e:
        return f"❌ Error: {e}"

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("📊 Noticias sobre Trading:\n")
    print(obtener_noticias("trading"))
