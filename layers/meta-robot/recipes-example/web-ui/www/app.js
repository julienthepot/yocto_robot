// app.js extrait de main.html
const statusEl = document.getElementById('status');
const v1 = document.getElementById('value1');
const v2 = document.getElementById('value2');
const v3 = document.getElementById('value3');
const ts = document.getElementById('timestamp');

function setStatus(text, cls) {
  statusEl.className = cls || '';
  statusEl.textContent = text;
}

let ws;
function connect() {
  ws = new WebSocket("ws://localhost:8765/api/ws");
  ws.onopen = () => setStatus("Connecté", "ok");
  ws.onmessage = e => {
    try {
      const data = JSON.parse(e.data);
      ts.textContent = data.timestamp || '--';
      v1.textContent = data.values?.[0] ?? '--';
      v2.textContent = data.values?.[1] ?? '--';
      v3.textContent = data.values?.[2] ?? '--';
    } catch {
      setStatus("Données invalides", "warn");
    }
  };
  ws.onerror = () => setStatus("Erreur WebSocket", "err");
  ws.onclose = () => {
    setStatus("Déconnecté - reconnexion...", "warn pulse");
    setTimeout(connect, 2000);
  };
}
connect();
