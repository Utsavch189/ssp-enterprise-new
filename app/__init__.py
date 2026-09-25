from flask import Flask, jsonify
from app.router.main_router import register_router
from app.middleware import session_data
from app.tables import create_tables
import os
import time
import threading
import requests

_keep_alive_started = False

def start_keep_alive():
    global _keep_alive_started
    if _keep_alive_started:
        return
    _keep_alive_started = True

    def ping_loop():
        while True:
            time.sleep(300)  # 5 minutes
            # RENDER_EXTERNAL_URL is automatically injected by Render for web services
            base_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("APP_URL")
            if base_url:
                ping_url = f"{base_url.rstrip('/')}/ping"
                try:
                    response = requests.get(ping_url, timeout=10)
                    print(f"[Keep-Alive] Pinged {ping_url} - Status: {response.status_code}")
                except Exception as e:
                    print(f"[Keep-Alive] Failed to ping {ping_url}: {e}")

    thread = threading.Thread(target=ping_loop, daemon=True)
    thread.start()

def create_app()->Flask:
    app = Flask(__name__)
    register_router(app)
    app.before_request(session_data)

    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({"status": "alive"}), 200

    os.makedirs(name='app/media',exist_ok=True)
    os.makedirs(name='app/media/importedExcels',exist_ok=True)
    os.makedirs(name='app/media/userQuery',exist_ok=True)
    create_tables()

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        start_keep_alive()

    return app