#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║  ANTIGRAVITY - LOCAL ENVIRONMENT SETUP           ║
║  Configura todo lo necesario para ejecutar       ║
║  el sistema localmente con un solo click.        ║
╚══════════════════════════════════════════════════╝
"""
import http.server
import socketserver
import webbrowser
import json
import subprocess
import sys
import os
import threading
import urllib.parse
import time
import shutil

PORT = 9090
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────
#  HTML Interface
# ─────────────────────────────────────────────────
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity — Setup Local</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;500;700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0a0f;--surface:#12121a;--border:#1e1e2e;
  --accent:#00e5a0;--accent2:#00b4d8;--danger:#ff4d6a;--warn:#ffb347;
  --text:#e4e4ed;--muted:#6b6b80;
  --glass:rgba(18,18,26,0.7);--glow:0 0 40px rgba(0,229,160,0.15);
}
html{font-size:15px}
body{font-family:'Outfit',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}

/* Animated grid background */
body::before{content:'';position:fixed;inset:0;background:
  linear-gradient(rgba(0,229,160,0.03) 1px,transparent 1px),
  linear-gradient(90deg,rgba(0,229,160,0.03) 1px,transparent 1px);
  background-size:60px 60px;z-index:0;pointer-events:none;
  animation:gridShift 20s linear infinite}
@keyframes gridShift{to{background-position:60px 60px}}

.container{max-width:720px;margin:0 auto;padding:2rem 1.5rem;position:relative;z-index:1}

/* Header */
.header{text-align:center;margin-bottom:2.5rem}
.logo{font-size:2.6rem;font-weight:900;letter-spacing:-1px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.subtitle{font-size:.95rem;color:var(--muted);margin-top:.4rem;font-weight:300}
.badge{display:inline-block;margin-top:.8rem;padding:.3rem .9rem;
  border-radius:20px;font-size:.7rem;font-weight:700;letter-spacing:1.5px;
  text-transform:uppercase;color:var(--bg);
  background:linear-gradient(135deg,var(--accent),var(--accent2))}

/* Config Card */
.card{background:var(--glass);backdrop-filter:blur(20px);
  border:1px solid var(--border);border-radius:16px;padding:1.8rem;
  margin-bottom:1.2rem;box-shadow:var(--glow);
  transition:border-color .3s}
.card:hover{border-color:rgba(0,229,160,0.25)}
.card-title{font-size:1.1rem;font-weight:700;margin-bottom:1rem;
  display:flex;align-items:center;gap:.5rem}
.card-title .icon{font-size:1.3rem}

/* Form */
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-bottom:.8rem}
.form-group{display:flex;flex-direction:column;gap:.3rem}
.form-group.full{grid-column:1/-1}
label{font-size:.75rem;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:1px}
input,select{background:var(--bg);border:1px solid var(--border);border-radius:10px;
  padding:.65rem .9rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.85rem;
  transition:border-color .2s,box-shadow .2s;outline:none}
input:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(0,229,160,0.1)}

/* Buttons */
.btn-group{display:flex;gap:.8rem;margin-top:1.5rem;flex-wrap:wrap}
.btn{flex:1;min-width:200px;padding:.85rem 1.5rem;border:none;border-radius:12px;
  font-family:'Outfit',sans-serif;font-size:.95rem;font-weight:700;
  cursor:pointer;transition:all .25s;display:flex;align-items:center;justify-content:center;gap:.5rem}
.btn-primary{background:linear-gradient(135deg,var(--accent),var(--accent2));color:var(--bg)}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,229,160,0.3)}
.btn-primary:active{transform:scale(.97)}
.btn-secondary{background:var(--surface);color:var(--text);border:1px solid var(--border)}
.btn-secondary:hover{border-color:var(--accent);background:rgba(0,229,160,0.05)}
.btn:disabled{opacity:.5;cursor:not-allowed;transform:none!important}

/* Console */
.console{background:#070710;border:1px solid var(--border);border-radius:14px;
  padding:1rem 1.2rem;margin-top:1rem;max-height:420px;overflow-y:auto;
  font-family:'JetBrains Mono',monospace;font-size:.78rem;line-height:1.7;
  scrollbar-width:thin;scrollbar-color:var(--border) transparent}
.console::-webkit-scrollbar{width:6px}
.console::-webkit-scrollbar-track{background:transparent}
.console::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.log-line{padding:2px 0;display:flex;gap:.5rem;align-items:flex-start}
.log-time{color:var(--muted);flex-shrink:0;font-size:.7rem}
.log-ok{color:var(--accent)}
.log-err{color:var(--danger)}
.log-warn{color:var(--warn)}
.log-info{color:var(--accent2)}
.log-cmd{color:#c4b5fd}

/* Progress */
.progress-bar{width:100%;height:6px;background:var(--border);border-radius:3px;margin-top:1rem;overflow:hidden}
.progress-fill{height:100%;width:0%;border-radius:3px;transition:width .4s ease;
  background:linear-gradient(90deg,var(--accent),var(--accent2))}

/* Status chips */
.status-row{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1rem}
.chip{padding:.3rem .7rem;border-radius:8px;font-size:.7rem;font-weight:600;
  border:1px solid var(--border);color:var(--muted);
  display:flex;align-items:center;gap:.3rem}
.chip.done{border-color:var(--accent);color:var(--accent);background:rgba(0,229,160,0.05)}
.chip.running{border-color:var(--warn);color:var(--warn);background:rgba(255,179,71,0.05);
  animation:pulse 1.5s ease infinite}
.chip.error{border-color:var(--danger);color:var(--danger);background:rgba(255,77,106,0.05)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}

/* Responsive */
@media(max-width:600px){.form-row{grid-template-columns:1fr}.btn-group{flex-direction:column}}
</style>
</head>
<body>
<div class="container">
  <!-- Header -->
  <div class="header">
    <div class="logo">⚡ Antigravity</div>
    <div class="subtitle">Setup del Entorno Local — Work Order Management</div>
    <span class="badge">DevOps Tools v1.0</span>
  </div>

  <!-- DB Config -->
  <div class="card">
    <div class="card-title"><span class="icon">🐘</span> Configuración PostgreSQL</div>
    <div class="form-row">
      <div class="form-group">
        <label>Host</label>
        <input id="db_host" type="text" value="localhost">
      </div>
      <div class="form-group">
        <label>Puerto</label>
        <input id="db_port" type="number" value="5432">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>Usuario</label>
        <input id="db_user" type="text" value="postgres">
      </div>
      <div class="form-group">
        <label>Contraseña</label>
        <input id="db_pass" type="password" value="123456">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group full">
        <label>Nombre de Base de Datos</label>
        <input id="db_name" type="text" value="antigravity_test">
      </div>
    </div>
  </div>

  <!-- App Config -->
  <div class="card">
    <div class="card-title"><span class="icon">🚀</span> Configuración de la Aplicación</div>
    <div class="form-row">
      <div class="form-group">
        <label>Puerto Uvicorn</label>
        <input id="app_port" type="number" value="8000">
      </div>
      <div class="form-group">
        <label>Host Uvicorn</label>
        <input id="app_host" type="text" value="127.0.0.1">
      </div>
    </div>
  </div>

  <!-- Actions -->
  <div class="btn-group">
    <button class="btn btn-primary" id="btnSetup" onclick="runSetup()">
      <span>⚙️</span> Configurar Todo
    </button>
    <button class="btn btn-secondary" id="btnLaunch" onclick="launchApp()" disabled>
      <span>🖥️</span> Iniciar Aplicación
    </button>
  </div>

  <!-- Status chips -->
  <div class="status-row" id="statusRow">
    <div class="chip" id="s_venv">📦 Entorno Virtual</div>
    <div class="chip" id="s_deps">📚 Dependencias</div>
    <div class="chip" id="s_db">🐘 Base de Datos</div>
    <div class="chip" id="s_tables">📋 Tablas</div>
    <div class="chip" id="s_seed">🌱 Datos Semilla</div>
  </div>

  <!-- Progress -->
  <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>

  <!-- Console -->
  <div class="console" id="console"></div>
</div>

<script>
const $ = id => document.getElementById(id);
let totalSteps = 5, doneSteps = 0;

function log(msg, type='info') {
  const c = $('console');
  const t = new Date().toLocaleTimeString('es',{hour12:false});
  c.innerHTML += `<div class="log-line"><span class="log-time">${t}</span><span class="log-${type}">${msg}</span></div>`;
  c.scrollTop = c.scrollHeight;
}

function setChip(id, state) {
  const el = $(id);
  el.className = 'chip ' + state;
}

function progress(n) {
  doneSteps = n;
  $('progressFill').style.width = (n/totalSteps*100) + '%';
}

async function api(action, data={}) {
  const r = await fetch('/api', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({action, ...data})
  });
  return await r.json();
}

function getConfig() {
  return {
    db_host: $('db_host').value,
    db_port: $('db_port').value,
    db_user: $('db_user').value,
    db_pass: $('db_pass').value,
    db_name: $('db_name').value,
    app_port: $('app_port').value,
    app_host: $('app_host').value
  };
}

async function runSetup() {
  const btn = $('btnSetup');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Trabajando...';
  doneSteps = 0;
  $('console').innerHTML = '';
  const cfg = getConfig();

  const steps = [
    { id:'s_venv',   action:'check_venv',    label:'Entorno Virtual' },
    { id:'s_deps',   action:'install_deps',   label:'Dependencias' },
    { id:'s_db',     action:'create_db',      label:'Base de Datos' },
    { id:'s_tables', action:'create_tables',  label:'Tablas' },
    { id:'s_seed',   action:'seed_data',      label:'Datos Semilla' },
  ];

  for (const step of steps) {
    setChip(step.id, 'running');
    log(`▶ ${step.label}...`, 'cmd');
    try {
      const res = await api(step.action, cfg);
      if (res.ok) {
        log(`✓ ${res.msg}`, 'ok');
        setChip(step.id, 'done');
      } else {
        log(`✗ ${res.msg}`, 'err');
        setChip(step.id, 'error');
        btn.disabled = false;
        btn.innerHTML = '<span>⚙️</span> Reintentar';
        return;
      }
    } catch(e) {
      log(`✗ Error de red: ${e.message}`, 'err');
      setChip(step.id, 'error');
      btn.disabled = false;
      btn.innerHTML = '<span>⚙️</span> Reintentar';
      return;
    }
    progress(steps.indexOf(step) + 1);
  }

  log('', 'info');
  log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'ok');
  log('🎉  SISTEMA LISTO PARA OPERAR', 'ok');
  log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'ok');
  log(`   URL: http://${cfg.app_host}:${cfg.app_port}`, 'info');
  log(`   DB:  postgresql://${cfg.db_host}:${cfg.db_port}/${cfg.db_name}`, 'info');
  log(`   Usuario por defecto: SU / 123456`, 'warn');
  log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'ok');

  btn.innerHTML = '<span>✅</span> Completado';
  $('btnLaunch').disabled = false;
}

async function launchApp() {
  const cfg = getConfig();
  $('btnLaunch').disabled = true;
  $('btnLaunch').innerHTML = '<span>🔄</span> Iniciando...';
  log('▶ Iniciando Uvicorn...', 'cmd');
  const res = await api('launch_app', cfg);
  if (res.ok) {
    log(`✓ ${res.msg}`, 'ok');
    log(`🌐 Abriendo http://${cfg.app_host}:${cfg.app_port} ...`, 'info');
    setTimeout(() => { window.open(`http://${cfg.app_host}:${cfg.app_port}`, '_blank'); }, 1500);
    $('btnLaunch').innerHTML = '<span>🟢</span> Ejecutándose';
  } else {
    log(`✗ ${res.msg}`, 'err');
    $('btnLaunch').disabled = false;
    $('btnLaunch').innerHTML = '<span>🖥️</span> Iniciar Aplicación';
  }
}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────
#  Backend Actions
# ─────────────────────────────────────────────────

def run_cmd(cmd, cwd=PROJECT_DIR):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            timeout=120, shell=True, encoding='utf-8', errors='replace'
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Timeout (120s)"
    except Exception as e:
        return False, str(e)


def get_python():
    """Find the Python executable in .venv or system."""
    venv_py = os.path.join(PROJECT_DIR, '.venv', 'Scripts', 'python.exe')
    if os.path.exists(venv_py):
        return venv_py
    venv_py_unix = os.path.join(PROJECT_DIR, '.venv', 'bin', 'python')
    if os.path.exists(venv_py_unix):
        return venv_py_unix
    return sys.executable


def update_database_py(cfg):
    """Rewrite app/database.py with the given config."""
    db_url = f"postgresql://{cfg['db_user']}:{cfg['db_pass']}@{cfg['db_host']}:{cfg['db_port']}/{cfg['db_name']}"
    content = f'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection URL (auto-generated by setup_local.py)
SQLALCHEMY_DATABASE_URL = "{db_url}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    with open(os.path.join(PROJECT_DIR, 'app', 'database.py'), 'w', encoding='utf-8') as f:
        f.write(content)


def handle_action(data):
    action = data.get('action', '')
    python = get_python()

    # ── Step 1: Check / Create venv ──
    if action == 'check_venv':
        venv_dir = os.path.join(PROJECT_DIR, '.venv')
        if os.path.exists(venv_dir):
            return {"ok": True, "msg": "Entorno virtual .venv ya existe."}
        ok, out = run_cmd(f'"{sys.executable}" -m venv .venv')
        if ok:
            return {"ok": True, "msg": "Entorno virtual creado correctamente."}
        return {"ok": False, "msg": f"Error creando venv: {out}"}

    # ── Step 2: Install dependencies ──
    elif action == 'install_deps':
        req_file = os.path.join(PROJECT_DIR, 'requirements.txt')
        if not os.path.exists(req_file):
            return {"ok": False, "msg": "No se encontro requirements.txt"}
        pip_exe = os.path.join(PROJECT_DIR, '.venv', 'Scripts', 'pip.exe')
        if not os.path.exists(pip_exe):
            pip_exe = os.path.join(PROJECT_DIR, '.venv', 'bin', 'pip')
        ok, out = run_cmd(f'"{pip_exe}" install -r requirements.txt')
        if ok or 'already satisfied' in out.lower():
            return {"ok": True, "msg": "Dependencias instaladas (o ya presentes)."}
        return {"ok": False, "msg": f"Error instalando: {out[:300]}"}

    # ── Step 3: Create database ──
    elif action == 'create_db':
        # First update the database.py config
        update_database_py(data)
        # Try connecting and creating DB
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=data['db_host'], port=int(data['db_port']),
                user=data['db_user'], password=data['db_pass'],
                dbname='postgres'
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{data['db_name']}'")
            if cur.fetchone():
                msg = f"Base de datos '{data['db_name']}' ya existe."
            else:
                cur.execute(f"CREATE DATABASE {data['db_name']} ENCODING 'UTF8'")
                msg = f"Base de datos '{data['db_name']}' creada."
            cur.close()
            conn.close()
            return {"ok": True, "msg": msg}
        except Exception as e:
            return {"ok": False, "msg": f"Error PostgreSQL: {str(e)[:200]}"}

    # ── Step 4: Create tables ──
    elif action == 'create_tables':
        ok, out = run_cmd(f'"{python}" -m app.initialize_db')
        if ok:
            return {"ok": True, "msg": "Tablas creadas correctamente en PostgreSQL."}
        return {"ok": False, "msg": f"Error: {out[:300]}"}

    # ── Step 5: Seed data ──
    elif action == 'seed_data':
        ok, out = run_cmd(f'"{python}" -m app.seed')
        if ok:
            return {"ok": True, "msg": "Datos semilla cargados (usuarios, roles, marcas, etc)."}
        return {"ok": False, "msg": f"Error: {out[:300]}"}

    # ── Launch App ──
    elif action == 'launch_app':
        port = data.get('app_port', '8000')
        host = data.get('app_host', '127.0.0.1')
        try:
            subprocess.Popen(
                f'"{python}" -m uvicorn app.main:app --host {host} --port {port} --reload',
                cwd=PROJECT_DIR, shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            return {"ok": True, "msg": f"Uvicorn iniciado en http://{host}:{port}"}
        except Exception as e:
            return {"ok": False, "msg": str(e)}

    return {"ok": False, "msg": f"Accion desconocida: {action}"}


# ─────────────────────────────────────────────────
#  HTTP Server
# ─────────────────────────────────────────────────

class SetupHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logs

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_POST(self):
        if self.path == '/api':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            data = json.loads(body)
            result = handle_action(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def main():
    print(f"\n  ANTIGRAVITY - Setup Local")
    print(f"  Interfaz: http://localhost:{PORT}")
    print(f"  Presione Ctrl+C para cerrar\n")
    webbrowser.open(f'http://localhost:{PORT}')
    with socketserver.TCPServer(("", PORT), SetupHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[✓] Servidor de setup detenido.")
            httpd.shutdown()


if __name__ == "__main__":
    main()
