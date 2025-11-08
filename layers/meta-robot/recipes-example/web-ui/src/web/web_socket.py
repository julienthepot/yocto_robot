import os
import json
import random
import signal
import threading
from datetime import datetime, timezone
from flask import Flask, jsonify, send_from_directory
from flask_sock import Sock
import db
import sys

HOST = os.environ.get("WS_HOST", "0.0.0.0")
PORT = int(os.environ.get("WS_PORT", "8765"))
INTERVAL_SEC = float(os.environ.get("WS_INTERVAL", "5"))

app = Flask(__name__, instance_relative_config=True)
sock = Sock(app)

clients = set()
shutdown_event = threading.Event()

def make_payload():
  return {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "values": [
      random.uniform(0, 100),
      random.uniform(0, 100),
      random.uniform(0, 100),
    ]
  }

def broadcaster():
  while not shutdown_event.is_set():
    if clients:
      payload = json.dumps(make_payload())
      dead = []
      for ws in list(clients):
        try:
          ws.send(payload)
        except Exception:
          dead.append(ws)
      for d in dead:
        clients.discard(d)
    shutdown_event.wait(INTERVAL_SEC)

@sock.route("/api/ws")
def ws_endpoint(ws):
  clients.add(ws)
  try:
    while True:
      msg = ws.receive()
      if msg is None:
        break  # client fermé
      # On ignore les messages entrants
  finally:
    clients.discard(ws)

@app.route("/api/health")
def health():
  return jsonify(status="ok", clients=len(clients), interval=INTERVAL_SEC)


@app.route("/")
def index():
  path = os.path.join(os.path.dirname(__file__), "www", "main.html")
  with open(path, "r", encoding="utf-8") as f:
    return f.read()
  
@app.route("/ui/style.css")
def style_css():
  www_dir = os.path.join(os.path.dirname(__file__), "www")
  return send_from_directory(www_dir, "style.css", mimetype="text/css")
  
@app.route("/ui/app.js")
def app_js():
  www_dir = os.path.join(os.path.dirname(__file__), "www")
  return send_from_directory(www_dir, "app.js", mimetype="application/javascript")

def start_background():
  t = threading.Thread(target=broadcaster, daemon=True)
  t.start()

def handle_signal(_signum, _frame):
  # Signal handler: set shutdown flag; parameters unused (underscored to silence linters)
  print("Arrêt en cours...")
  shutdown_event.set()
  sys.exit(0)
  
if __name__ == "__main__":

  app.config.from_mapping(
    DEBUF=True,
    SECRET_KEY="dev",
    DATABASE=os.path.join(app.instance_path, "web-ui.sqlite"),
  )

  # ensure the instance folder exists
  try:
      os.makedirs(app.instance_path)
  except OSError:
      pass
  
  db.init_app(app)

  #for sig in (signal.SIGINT, signal.SIGTERM):
  #  signal.signal(sig, handle_signal)
  start_background()
  print(f"Serveur Flask + WebSocket sur http://{HOST}:{PORT}  (ws: /api/ws)")
  print(f"Diffusion de 3 valeurs aléatoires toutes les {INTERVAL_SEC}s (Ctrl-C pour arrêter)")
  # use_reloader=False pour que Ctrl-C (SIGINT) soit bien capturé dans ce process
  app.run(host=HOST, port=PORT, use_reloader=False)
