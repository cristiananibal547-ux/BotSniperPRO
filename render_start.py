# render_start.py
# Wrapper simple para Render: lanza sniper_bot.py en background y levanta
# un server HTTP mínimo para que Render mantenga el servicio vivo.

import os
import subprocess
import time
import signal
import sys
from aiohttp import web

# Si tu bot requiere python específico, Render ya usa el entorno que definiste.
BOT_PY = "sniper_bot.py"

# Lanzar el bot como subproceso (stdout/err van al log)
proc = None
def start_bot():
    global proc
    if proc is None:
        proc = subprocess.Popen([sys.executable, BOT_PY], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(f"[render_start] started subprocess pid={proc.pid}")

def stop_bot():
    global proc
    if proc:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

async def handle(request):
    return web.Response(text="SniperPro OK")

def run_web():
    port = int(os.environ.get("PORT", "8000"))
    app = web.Application()
    app.router.add_get("/", handle)
    # Ruta para healthcheck
    app.router.add_get("/healthz", handle)
    print(f"[render_start] web server listening on 0.0.0.0:{port}")
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    try:
        start_bot()
        # Loop web (bloqueante) — Render necesita que proceso principal escuche en $PORT.
        run_web()
    except KeyboardInterrupt:
        print("[render_start] keyboard interrupt, stopping")
    finally:
        stop_bot()
        print("[render_start] done")
