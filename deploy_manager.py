#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║  ANTIGRAVITY — DEPLOYMENT MANAGER                ║
║  Despliegue On-Premise (IIS/Apache) y            ║
║  Cloud gratuito (Render / Railway)               ║
╚══════════════════════════════════════════════════╝
"""
import http.server
import socketserver
import webbrowser
import json
import subprocess
import sys
import os
import shutil
import zipfile
from datetime import datetime

PORT = 9091
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────
#  HTML Interface
# ─────────────────────────────────────────────────
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity — Deploy Manager</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;500;700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#07070d;--surface:#0f0f1a;--surface2:#161625;--border:#1a1a2e;
  --accent:#845ef7;--accent2:#da77f2;--accent3:#5c7cfa;
  --success:#00e5a0;--danger:#ff4d6a;--warn:#ffb347;
  --text:#e4e4ed;--muted:#6b6b80;
  --glass:rgba(15,15,26,0.85);--glow:0 0 60px rgba(132,94,247,0.1);
}
html{font-size:15px}
body{font-family:'Outfit',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}

/* Mesh gradient background */
body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse at 20% 0%, rgba(132,94,247,0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 100%, rgba(218,119,242,0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(92,124,250,0.04) 0%, transparent 60%)}
body::after{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:linear-gradient(rgba(132,94,247,0.015) 1px,transparent 1px),
  linear-gradient(90deg,rgba(132,94,247,0.015) 1px,transparent 1px);
  background-size:50px 50px}

.container{max-width:800px;margin:0 auto;padding:2rem 1.5rem;position:relative;z-index:1}

/* Header */
.header{text-align:center;margin-bottom:2rem}
.logo{font-size:2.4rem;font-weight:900;letter-spacing:-1px;
  background:linear-gradient(135deg,var(--accent),var(--accent2),var(--accent3));
  background-size:200% 200%;animation:gradShift 4s ease infinite;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
@keyframes gradShift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.subtitle{font-size:.9rem;color:var(--muted);margin-top:.3rem;font-weight:300}
.badge{display:inline-block;margin-top:.7rem;padding:.25rem .8rem;
  border-radius:20px;font-size:.68rem;font-weight:700;letter-spacing:1.5px;
  text-transform:uppercase;color:#fff;
  background:linear-gradient(135deg,var(--accent),var(--accent2))}

/* Tabs */
.tabs{display:flex;gap:4px;margin-bottom:1.5rem;
  background:var(--surface);border-radius:14px;padding:4px;border:1px solid var(--border)}
.tab{flex:1;padding:.75rem;text-align:center;border-radius:11px;
  font-weight:600;font-size:.85rem;cursor:pointer;transition:all .25s;color:var(--muted)}
.tab:hover{color:var(--text)}
.tab.active{background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;box-shadow:0 4px 20px rgba(132,94,247,0.3)}
.tab-icon{font-size:1.2rem;display:block;margin-bottom:.2rem}

/* Panels */
.panel{display:none;animation:fadeIn .3s ease}
.panel.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* Card */
.card{background:var(--glass);backdrop-filter:blur(20px);
  border:1px solid var(--border);border-radius:16px;padding:1.6rem;
  margin-bottom:1rem;transition:border-color .3s}
.card:hover{border-color:rgba(132,94,247,0.2)}
.card-title{font-size:1.05rem;font-weight:700;margin-bottom:.8rem;
  display:flex;align-items:center;gap:.5rem}
.card-title .icon{font-size:1.2rem}
.card-desc{font-size:.8rem;color:var(--muted);margin-bottom:1rem;line-height:1.5}

/* Form */
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:.7rem;margin-bottom:.7rem}
.form-group{display:flex;flex-direction:column;gap:.25rem}
.form-group.full{grid-column:1/-1}
label{font-size:.7rem;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:1px}
input,select,textarea{background:var(--bg);border:1px solid var(--border);border-radius:10px;
  padding:.6rem .8rem;color:var(--text);font-family:'JetBrains Mono',monospace;font-size:.82rem;
  transition:border-color .2s;outline:none;resize:vertical}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(132,94,247,0.1)}
select{cursor:pointer}

/* Buttons */
.btn-group{display:flex;gap:.7rem;margin-top:1.2rem;flex-wrap:wrap}
.btn{flex:1;min-width:180px;padding:.8rem 1.3rem;border:none;border-radius:12px;
  font-family:'Outfit',sans-serif;font-size:.9rem;font-weight:700;
  cursor:pointer;transition:all .25s;display:flex;align-items:center;justify-content:center;gap:.5rem}
.btn-primary{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(132,94,247,0.3)}
.btn-secondary{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-secondary:hover{border-color:var(--accent)}
.btn-cloud{background:linear-gradient(135deg,var(--accent3),var(--accent));color:#fff}
.btn-cloud:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(92,124,250,0.3)}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none!important}

/* Console */
.console{background:#050509;border:1px solid var(--border);border-radius:14px;
  padding:1rem 1.2rem;margin-top:1rem;max-height:380px;overflow-y:auto;
  font-family:'JetBrains Mono',monospace;font-size:.75rem;line-height:1.7;
  scrollbar-width:thin;scrollbar-color:var(--border) transparent}
.console::-webkit-scrollbar{width:5px}
.console::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.log-line{padding:1px 0;display:flex;gap:.5rem}
.log-time{color:var(--muted);flex-shrink:0;font-size:.68rem}
.log-ok{color:var(--success)}
.log-err{color:var(--danger)}
.log-warn{color:var(--warn)}
.log-info{color:var(--accent2)}
.log-cmd{color:var(--accent3)}

/* Progress */
.progress-bar{width:100%;height:5px;background:var(--border);border-radius:3px;margin-top:.8rem;overflow:hidden}
.progress-fill{height:100%;width:0%;border-radius:3px;transition:width .4s ease;
  background:linear-gradient(90deg,var(--accent),var(--accent2))}

/* Status */
.status-row{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.8rem}
.chip{padding:.25rem .6rem;border-radius:7px;font-size:.67rem;font-weight:600;
  border:1px solid var(--border);color:var(--muted);display:flex;align-items:center;gap:.3rem}
.chip.done{border-color:var(--success);color:var(--success);background:rgba(0,229,160,0.05)}
.chip.running{border-color:var(--warn);color:var(--warn);animation:pulse 1.5s ease infinite}
.chip.error{border-color:var(--danger);color:var(--danger)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}

/* Info box */
.info-box{background:rgba(92,124,250,0.06);border:1px solid rgba(92,124,250,0.15);
  border-radius:12px;padding:1rem 1.2rem;margin-bottom:1rem;font-size:.82rem;line-height:1.6}
.info-box strong{color:var(--accent2)}
.info-box code{background:var(--bg);padding:.15rem .4rem;border-radius:5px;font-family:'JetBrains Mono',monospace;font-size:.75rem}

/* Cloud cards */
.cloud-options{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-bottom:1rem}
.cloud-card{background:var(--surface);border:2px solid var(--border);border-radius:14px;
  padding:1.2rem;cursor:pointer;transition:all .25s;text-align:center}
.cloud-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.cloud-card.selected{border-color:var(--accent);background:rgba(132,94,247,0.05);
  box-shadow:0 0 20px rgba(132,94,247,0.1)}
.cloud-card .cloud-name{font-weight:700;font-size:1rem;margin-bottom:.3rem}
.cloud-card .cloud-desc{font-size:.72rem;color:var(--muted);line-height:1.4}
.cloud-card .cloud-icon{font-size:2rem;margin-bottom:.5rem}
.cloud-card .cloud-free{display:inline-block;margin-top:.5rem;padding:.15rem .5rem;
  border-radius:6px;font-size:.6rem;font-weight:700;letter-spacing:1px;
  background:rgba(0,229,160,0.1);color:var(--success);text-transform:uppercase}

@media(max-width:600px){.form-row,.cloud-options{grid-template-columns:1fr}.btn-group{flex-direction:column}}
</style>
</head>
<body>
<div class="container">
  <!-- Header -->
  <div class="header">
    <div class="logo">🚀 Deploy Manager</div>
    <div class="subtitle">Antigravity — Work Order Management System</div>
    <span class="badge">Production Deployment</span>
  </div>

  <!-- Tabs -->
  <div class="tabs">
    <div class="tab active" onclick="switchTab('onprem')">
      <span class="tab-icon">🏢</span> On-Premise
    </div>
    <div class="tab" onclick="switchTab('cloud')">
      <span class="tab-icon">☁️</span> Cloud (Gratis)
    </div>
  </div>

  <!-- ════════════════════════════════════════ -->
  <!-- ON-PREMISE PANEL                         -->
  <!-- ════════════════════════════════════════ -->
  <div class="panel active" id="panel_onprem">

    <!-- Server Info -->
    <div class="card">
      <div class="card-title"><span class="icon">🖥️</span> Servidor Destino</div>
      <div class="card-desc">Datos del servidor Windows/Linux donde se desplegara la aplicacion.</div>
      <div class="form-row">
        <div class="form-group">
          <label>IP/Nombre del Servidor</label>
          <input id="op_server" type="text" value="localhost" placeholder="192.168.1.100">
        </div>
        <div class="form-group">
          <label>Sistema Operativo</label>
          <select id="op_os">
            <option value="windows">Windows Server</option>
            <option value="linux">Linux (Ubuntu/Debian)</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Web Server</label>
          <select id="op_webserver">
            <option value="iis">IIS (Windows)</option>
            <option value="apache">Apache + mod_proxy</option>
            <option value="direct">Uvicorn Directo (Dev)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Puerto de la App</label>
          <input id="op_app_port" type="number" value="8000">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group full">
          <label>Ruta del Proyecto en el Servidor</label>
          <input id="op_project_path" type="text" value="" placeholder="C:\inetpub\wwwroot\antigravity">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group full">
          <label>Versión a Desplegar</label>
          <select id="op_app_version">
            <option value="python">Versión Python (FastAPI / Uvicorn)</option>
            <option value="php">Versión PHP Nativa (LAMP / cPanel)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- DB Config -->
    <div class="card">
      <div class="card-title"><span class="icon">🐘</span> PostgreSQL (Produccion)</div>
      <div class="form-row">
        <div class="form-group">
          <label>Host DB</label>
          <input id="op_db_host" type="text" value="localhost">
        </div>
        <div class="form-group">
          <label>Puerto</label>
          <input id="op_db_port" type="number" value="5432">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Usuario DB</label>
          <input id="op_db_user" type="text" value="postgres">
        </div>
        <div class="form-group">
          <label>Password DB</label>
          <input id="op_db_pass" type="password" value="123456">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group full">
          <label>Nombre de Base de Datos</label>
          <input id="op_db_name" type="text" value="antigravity_prod">
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="btn-group">
      <button class="btn btn-secondary" onclick="generatePackage()">
        <span>📦</span> Generar Paquete
      </button>
      <button class="btn btn-primary" onclick="deployOnPrem()">
        <span>🚀</span> Desplegar
      </button>
    </div>

    <div class="status-row" id="opStatusRow">
      <div class="chip" id="op_s_pkg">📦 Paquete</div>
      <div class="chip" id="op_s_cfg">⚙️ Configs</div>
      <div class="chip" id="op_s_db">🐘 Base Datos</div>
      <div class="chip" id="op_s_tables">📋 Tablas</div>
      <div class="chip" id="op_s_seed">🌱 Seed</div>
      <div class="chip" id="op_s_svc">🔧 Servicio</div>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="opProgress"></div></div>
    <div class="console" id="opConsole"></div>
  </div>

  <!-- ════════════════════════════════════════ -->
  <!-- CLOUD PANEL                              -->
  <!-- ════════════════════════════════════════ -->
  <div class="panel" id="panel_cloud">

    <div class="info-box">
      <strong>💡 Despliegue Cloud Gratuito</strong><br>
      Estas plataformas ofrecen un plan gratuito ideal para demos y proyectos personales.
      Debera tener una cuenta creada previamente.
    </div>

    <!-- Provider Selection -->
    <div class="cloud-options">
      <div class="cloud-card selected" onclick="selectCloud('render')" id="cc_render">
        <div class="cloud-icon">🌐</div>
        <div class="cloud-name">Render</div>
        <div class="cloud-desc">Web Services + PostgreSQL gratuito. Ideal para FastAPI.</div>
        <span class="cloud-free">Free Tier</span>
      </div>
      <div class="cloud-card" onclick="selectCloud('railway')" id="cc_railway">
        <div class="cloud-icon">🚂</div>
        <div class="cloud-name">Railway</div>
        <div class="cloud-desc">Deploy desde GitHub. PostgreSQL integrado. $5 creditos gratis/mes.</div>
        <span class="cloud-free">Trial Free</span>
      </div>
    </div>

    <!-- Render Config -->
    <div id="cfg_render">
      <div class="card">
        <div class="card-title"><span class="icon">🌐</span> Configuracion Render</div>
        <div class="card-desc">Render detecta automaticamente FastAPI. Necesita un archivo <code>render.yaml</code> y la URL del repositorio GitHub.</div>
        <div class="form-row">
          <div class="form-group full">
            <label>URL del Repositorio GitHub</label>
            <input id="cl_render_repo" type="text" value="https://github.com/SayayinSer/AntigravityTest" placeholder="https://github.com/user/repo">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Region</label>
            <select id="cl_render_region">
              <option value="oregon">Oregon (US-West)</option>
              <option value="ohio">Ohio (US-East)</option>
              <option value="frankfurt">Frankfurt (EU)</option>
              <option value="singapore">Singapore (Asia)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Nombre del Servicio</label>
            <input id="cl_render_name" type="text" value="antigravity-app">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group full">
            <label>Nombre BD PostgreSQL (Render)</label>
            <input id="cl_render_db" type="text" value="antigravity_db">
          </div>
        </div>
      </div>
    </div>

    <!-- Railway Config -->
    <div id="cfg_railway" style="display:none">
      <div class="card">
        <div class="card-title"><span class="icon">🚂</span> Configuracion Railway</div>
        <div class="card-desc">Railway permite deploy con un click desde GitHub. Genera PostgreSQL automaticamente. Necesita un <code>Procfile</code>.</div>
        <div class="form-row">
          <div class="form-group full">
            <label>URL del Repositorio GitHub</label>
            <input id="cl_railway_repo" type="text" value="https://github.com/SayayinSer/AntigravityTest" placeholder="https://github.com/user/repo">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group full">
            <label>Nombre del Proyecto</label>
            <input id="cl_railway_name" type="text" value="antigravity-workorders">
          </div>
        </div>
      </div>
    </div>

    <!-- Cloud Actions -->
    <div class="btn-group">
      <button class="btn btn-secondary" onclick="generateCloudFiles()">
        <span>📄</span> Generar Archivos de Deploy
      </button>
      <button class="btn btn-cloud" onclick="openCloudDeploy()">
        <span>☁️</span> Abrir Plataforma
      </button>
    </div>

    <div class="status-row" id="clStatusRow">
      <div class="chip" id="cl_s_files">📄 Archivos</div>
      <div class="chip" id="cl_s_req">📦 Requirements</div>
      <div class="chip" id="cl_s_push">🔄 Git Push</div>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="clProgress"></div></div>
    <div class="console" id="clConsole"></div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
let selectedCloud = 'render';

function switchTab(tab) {
  document.querySelectorAll('.tab').forEach((t,i) => {
    t.classList.toggle('active', (tab==='onprem' && i===0)||(tab==='cloud' && i===1));
  });
  $('panel_onprem').classList.toggle('active', tab==='onprem');
  $('panel_cloud').classList.toggle('active', tab==='cloud');
}

function selectCloud(provider) {
  selectedCloud = provider;
  document.querySelectorAll('.cloud-card').forEach(c => c.classList.remove('selected'));
  $('cc_'+provider).classList.add('selected');
  $('cfg_render').style.display = provider==='render' ? 'block' : 'none';
  $('cfg_railway').style.display = provider==='railway' ? 'block' : 'none';
}

function log(consoleId, msg, type='info') {
  const c = $(consoleId);
  const t = new Date().toLocaleTimeString('es',{hour12:false});
  c.innerHTML += `<div class="log-line"><span class="log-time">${t}</span><span class="log-${type}">${msg}</span></div>`;
  c.scrollTop = c.scrollHeight;
}

function setChip(id, state) { $(id).className = 'chip ' + state; }

async function api(action, data={}) {
  const r = await fetch('/api', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({action, ...data})
  });
  return await r.json();
}

function getOnPremConfig() {
  return {
    server: $('op_server').value,
    os: $('op_os').value,
    webserver: $('op_webserver').value,
    app_port: $('op_app_port').value,
    project_path: $('op_project_path').value,
    app_version: $('op_app_version').value,
    db_host: $('op_db_host').value,
    db_port: $('op_db_port').value,
    db_user: $('op_db_user').value,
    db_pass: $('op_db_pass').value,
    db_name: $('op_db_name').value
  };
}

// ── ON-PREM: Generate Package ──
async function generatePackage() {
  log('opConsole','','info');
  log('opConsole','▶ Generando paquete de despliegue...','cmd');
  setChip('op_s_pkg','running');
  const cfg = getOnPremConfig();
  const res = await api('generate_package', cfg);
  if(res.ok){
    log('opConsole','✓ '+res.msg,'ok');
    setChip('op_s_pkg','done');
  } else {
    log('opConsole','✗ '+res.msg,'err');
    setChip('op_s_pkg','error');
  }
}

// ── ON-PREM: Full Deploy ──
async function deployOnPrem() {
  const con = 'opConsole';
  $(con).innerHTML = '';
  const cfg = getOnPremConfig();
  const steps = [
    {id:'op_s_pkg',   action:'generate_package', label:'Paquete de deploy'},
    {id:'op_s_cfg',   action:'generate_configs',  label:'Archivos de configuracion'},
    {id:'op_s_db',    action:'deploy_create_db',  label:'Crear Base de Datos'},
    {id:'op_s_tables',action:'deploy_tables',     label:'Crear Tablas'},
    {id:'op_s_seed',  action:'deploy_seed',       label:'Datos Semilla'},
    {id:'op_s_svc',   action:'deploy_service',    label:'Configurar Servicio'},
  ];
  let i=0;
  for(const step of steps){
    setChip(step.id,'running');
    log(con,`▶ ${step.label}...`,'cmd');
    const res = await api(step.action, cfg);
    if(res.ok){
      log(con,'✓ '+res.msg,'ok');
      setChip(step.id,'done');
      if(res.extra) res.extra.forEach(l => log(con,'  '+l,'info'));
    } else {
      log(con,'✗ '+res.msg,'err');
      setChip(step.id,'error');
      return;
    }
    i++;
    $('opProgress').style.width = (i/steps.length*100)+'%';
  }
  log(con,'','ok');
  log(con,'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━','ok');
  log(con,'🎉 DESPLIEGUE ON-PREMISE COMPLETADO','ok');
  log(con,'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━','ok');
  log(con,`  Servidor: ${cfg.server}:${cfg.app_port}`,'info');
  log(con,`  BD: postgresql://${cfg.db_host}:${cfg.db_port}/${cfg.db_name}`,'info');
  log(con,`  Paquete: deploy_package/`,'info');
  log(con,'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━','ok');
}

// ── CLOUD: Generate Files ──
async function generateCloudFiles() {
  const con = 'clConsole';
  $(con).innerHTML = '';
  const data = { provider: selectedCloud };
  if(selectedCloud === 'render') {
    data.repo = $('cl_render_repo').value;
    data.region = $('cl_render_region').value;
    data.name = $('cl_render_name').value;
    data.db_name = $('cl_render_db').value;
  } else {
    data.repo = $('cl_railway_repo').value;
    data.name = $('cl_railway_name').value;
  }
  const steps = [
    {id:'cl_s_files', action:'cloud_gen_files', label:'Archivos de configuracion cloud'},
    {id:'cl_s_req',   action:'cloud_gen_req',   label:'Requirements y runtime'},
    {id:'cl_s_push',  action:'cloud_git_push',  label:'Git commit & push'},
  ];
  let i=0;
  for(const step of steps){
    setChip(step.id,'running');
    log(con,`▶ ${step.label}...`,'cmd');
    const res = await api(step.action, data);
    if(res.ok){
      log(con,'✓ '+res.msg,'ok');
      setChip(step.id,'done');
      if(res.extra) res.extra.forEach(l => log(con,'  '+l,'info'));
    } else {
      log(con,'✗ '+res.msg,'err');
      setChip(step.id,'error');
      return;
    }
    i++;
    $('clProgress').style.width = (i/steps.length*100)+'%';
  }
  log(con,'','ok');
  log(con,'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━','ok');
  log(con,'🎉 ARCHIVOS CLOUD GENERADOS Y PUSHEADOS','ok');
  log(con,'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━','ok');
  log(con,`  Provider: ${selectedCloud.toUpperCase()}`,'info');
  const url = selectedCloud==='render'? 'https://dashboard.render.com' : 'https://railway.app/dashboard';
  log(con,`  Dashboard: ${url}`,'info');
  log(con,`  Paso siguiente: Conecte su repo en la plataforma.`,'warn');
  log(con,'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━','ok');
}

function openCloudDeploy() {
  const url = selectedCloud==='render'
    ? 'https://dashboard.render.com/create?type=web'
    : 'https://railway.app/new';
  window.open(url, '_blank');
}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────
#  Backend Actions
# ─────────────────────────────────────────────────

def run_cmd(cmd, cwd=PROJECT_DIR):
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
    venv_py = os.path.join(PROJECT_DIR, '.venv', 'Scripts', 'python.exe')
    if os.path.exists(venv_py):
        return venv_py
    venv_py_unix = os.path.join(PROJECT_DIR, '.venv', 'bin', 'python')
    if os.path.exists(venv_py_unix):
        return venv_py_unix
    return sys.executable


def update_database_py(cfg):
    """Rewrite app/database.py with the given config (Modern robust template)."""
    db_url = f"postgresql://{cfg['db_user']}:{cfg['db_pass']}@{cfg['db_host']}:{cfg['db_port']}/{cfg['db_name']}"
    content = f'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL connection URL (Modern robust template)
# Priority 1: Environment variable DATABASE_URL
# Priority 2: Hardcoded fallback (for local development)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "{db_url}")

# Fix for some cloud providers (Render uses postgres:// but SQLAlchemy needs postgresql://)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

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
    target = os.path.join(PROJECT_DIR, 'app', 'database.py')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)


def handle_action(data):
    action = data.get('action', '')
    python = get_python()

    # ═══════════════════════════════════════
    #  ON-PREMISE ACTIONS
    # ═══════════════════════════════════════

    if action == 'generate_package':
        try:
            pkg_dir = os.path.join(PROJECT_DIR, 'deploy_package')
            os.makedirs(pkg_dir, exist_ok=True)
            app_version = data.get('app_version', 'python')

            # Delete old content
            for item in os.listdir(pkg_dir):
                item_path = os.path.join(pkg_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

            if app_version == 'python':
                # Copy Python app files
                dirs_to_copy = ['app']
                for d in dirs_to_copy:
                    src = os.path.join(PROJECT_DIR, d)
                    dst = os.path.join(pkg_dir, d)
                    if os.path.exists(src):
                        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

                # Copy essential Python files
                for f in ['requirements.txt', 'backup_data.py']:
                    src = os.path.join(PROJECT_DIR, f)
                    if os.path.exists(src):
                        shutil.copy2(src, pkg_dir)
            else:
                # Copy PHP app files
                src = os.path.join(PROJECT_DIR, 'NucleoTallerPHP')
                if os.path.exists(src):
                    # Copy everything inside NucleoTallerPHP to the package dir
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(pkg_dir, item)
                        if os.path.isdir(s):
                            shutil.copytree(s, d)
                        else:
                            shutil.copy2(s, d)

            return {"ok": True, "msg": f"Paquete {app_version.upper()} generado en deploy_package/"}
        except Exception as e:
            return {"ok": False, "msg": str(e)}

    elif action == 'generate_configs':
        try:
            pkg_dir = os.path.join(PROJECT_DIR, 'deploy_package')
            os.makedirs(pkg_dir, exist_ok=True)
            webserver = data.get('webserver', 'direct')
            app_port = data.get('app_port', '8000')
            project_path = data.get('project_path', '')
            extras = []

            # Generate database.py for production
            db_url = f"postgresql://{data['db_user']}:{data['db_pass']}@{data['db_host']}:{data['db_port']}/{data['db_name']}"
            db_py = f'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Production PostgreSQL (Modern robust template)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "{db_url}")

# Fix for some cloud providers (Render uses postgres:// but SQLAlchemy needs postgresql://)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

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
            with open(os.path.join(pkg_dir, 'app', 'database.py'), 'w', encoding='utf-8') as f:
                f.write(db_py)
            extras.append("database.py actualizado con credenciales de produccion")

            # Generate web.config for IIS
            if webserver == 'iis':
                web_config = f'''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="httpPlatformHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified" />
        </handlers>
        <httpPlatform processPath="python.exe"
                      arguments="-m uvicorn app.main:app --port %HTTP_PLATFORM_PORT% --host 0.0.0.0"
                      stdoutLogEnabled="true"
                      stdoutLogFile=".\\logs\\stdout.log"
                      startupTimeLimit="60">
            <environmentVariables>
                <environmentVariable name="PYTHONPATH" value="{project_path if project_path else '.'}" />
            </environmentVariables>
        </httpPlatform>
    </system.webServer>
</configuration>
'''
                with open(os.path.join(pkg_dir, 'web.config'), 'w', encoding='utf-8') as f:
                    f.write(web_config)
                extras.append("web.config generado para IIS")

            # Generate Apache VirtualHost
            elif webserver == 'apache':
                apache_conf = f'''# Antigravity - Apache VirtualHost
# Copiar a /etc/apache2/sites-available/antigravity.conf
# Luego: sudo a2ensite antigravity && sudo systemctl reload apache2

<VirtualHost *:80>
    ServerName {data.get('server','localhost')}

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:{app_port}/
    ProxyPassReverse / http://127.0.0.1:{app_port}/

    ErrorLog ${{APACHE_LOG_DIR}}/antigravity_error.log
    CustomLog ${{APACHE_LOG_DIR}}/antigravity_access.log combined
</VirtualHost>
'''
                with open(os.path.join(pkg_dir, 'antigravity.conf'), 'w', encoding='utf-8') as f:
                    f.write(apache_conf)
                extras.append("antigravity.conf generado para Apache")

                # Systemd service file
                systemd_svc = f'''[Unit]
Description=Antigravity FastAPI App
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory={project_path if project_path else '/opt/antigravity'}
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 127.0.0.1 --port {app_port}
Restart=always
RestartSec=3
Environment="DATABASE_URL={db_url}"

[Install]
WantedBy=multi-user.target
'''
                with open(os.path.join(pkg_dir, 'antigravity.service'), 'w', encoding='utf-8') as f:
                    f.write(systemd_svc)
                extras.append("antigravity.service generado para systemd")

            # Generate startup script
            if data.get('os') == 'windows':
                bat = f'''@echo off
echo ======================================
echo   Antigravity - Inicio de Servicio
echo ======================================
cd /d "%~dp0"
if not exist .venv (
    echo Creando entorno virtual...
    python -m venv .venv
)
call .venv\\Scripts\\activate
pip install -r requirements.txt
echo Iniciando servidor en puerto {app_port}...
python -m uvicorn app.main:app --host 0.0.0.0 --port {app_port}
pause
'''
                with open(os.path.join(pkg_dir, 'start_server.bat'), 'w', encoding='utf-8') as f:
                    f.write(bat)
                extras.append("start_server.bat generado")
            else:
                sh = f'''#!/bin/bash
echo "======================================"
echo "  Antigravity - Inicio de Servicio"
echo "======================================"
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
echo "Iniciando servidor en puerto {app_port}..."
python -m uvicorn app.main:app --host 0.0.0.0 --port {app_port}
'''
                sh_path = os.path.join(pkg_dir, 'start_server.sh')
                with open(sh_path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(sh)
                extras.append("start_server.sh generado")

            return {"ok": True, "msg": f"Archivos de configuracion generados.", "extra": extras}
        except Exception as e:
            return {"ok": False, "msg": str(e)}

    elif action == 'deploy_create_db':
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
                msg = f"BD '{data['db_name']}' ya existe."
            else:
                cur.execute(f"CREATE DATABASE {data['db_name']} ENCODING 'UTF8'")
                msg = f"BD '{data['db_name']}' creada."
            cur.close()
            conn.close()

            # Update local database.py temporarily for table creation
            update_database_py(data)
            return {"ok": True, "msg": msg}
        except Exception as e:
            return {"ok": False, "msg": f"Error PostgreSQL: {str(e)[:250]}"}

    elif action == 'deploy_tables':
        update_database_py(data)
        ok, out = run_cmd(f'"{python}" -m app.initialize_db')
        if ok:
            return {"ok": True, "msg": "Tablas creadas en la BD de produccion."}
        return {"ok": False, "msg": f"Error: {out[:300]}"}

    elif action == 'deploy_seed':
        ok, out = run_cmd(f'"{python}" -m app.seed')
        if ok:
            return {"ok": True, "msg": "Datos semilla cargados (usuarios, roles, marcas, tecnicos)."}
        return {"ok": False, "msg": f"Error: {out[:300]}"}

    elif action == 'deploy_service':
        webserver = data.get('webserver', 'direct')
        extras = []
        if webserver == 'iis':
            extras.append("Copie deploy_package/ al directorio del sitio IIS")
            extras.append("Asegurese de tener HttpPlatformHandler instalado")
            extras.append("Configure el Application Pool sin Managed Code")
        elif webserver == 'apache':
            extras.append("Copie antigravity.conf a /etc/apache2/sites-available/")
            extras.append("Ejecute: sudo a2enmod proxy proxy_http")
            extras.append("Ejecute: sudo a2ensite antigravity && sudo systemctl reload apache2")
            extras.append("Copie antigravity.service a /etc/systemd/system/")
            extras.append("Ejecute: sudo systemctl enable --now antigravity")
        else:
            extras.append(f"Ejecute: start_server.bat (o .sh en Linux)")
        return {"ok": True, "msg": "Instrucciones de servicio generadas.", "extra": extras}

    # ═══════════════════════════════════════
    #  CLOUD ACTIONS
    # ═══════════════════════════════════════

    elif action == 'cloud_gen_files':
        provider = data.get('provider', 'render')
        try:
            extras = []

            # Update database.py to use DATABASE_URL env var
            db_py_cloud = '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Cloud deployment: reads DATABASE_URL from environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost/antigravity_test")

# Fix for Render (provides postgres:// but SQLAlchemy needs postgresql://)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

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
                f.write(db_py_cloud)
            extras.append("database.py actualizado con DATABASE_URL dinamic")

            # Create startup script that initializes DB on first run
            startup = '''#!/usr/bin/env python3
"""Cloud startup: creates tables and seeds data if empty."""
import sys
import os

def startup():
    try:
        from app.database import engine, Base
        from app import models
        from sqlalchemy import inspect, text

        print("[STARTUP] Checking database...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if 'users' not in tables:
            print("[STARTUP] Creating tables...")
            Base.metadata.create_all(bind=engine)
            print("[STARTUP] Tables created. Seeding data...")
            # Import and run seed
            from app.seed import seed_data
            seed_data()
            print("[STARTUP] Seed complete!")
        else:
            print("[STARTUP] Tables already exist. Skipping.")
    except Exception as e:
        print(f"[STARTUP] Warning: {e}")

if __name__ == "__main__":
    startup()
'''
            with open(os.path.join(PROJECT_DIR, 'cloud_startup.py'), 'w', encoding='utf-8') as f:
                f.write(startup)
            extras.append("cloud_startup.py creado (auto-init en primer deploy)")

            if provider == 'render':
                # render.yaml (Blueprint)
                render_yaml = f'''# Render Blueprint - Antigravity Work Order Management
# https://render.com/docs/blueprint-spec

services:
  - type: web
    name: {data.get('name', 'antigravity-app')}
    runtime: python
    region: {data.get('region', 'oregon')}
    buildCommand: pip install -r requirements.txt
    startCommand: python cloud_startup.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: {data.get('db_name', 'antigravity_db')}
          property: connectionURI
      - key: PYTHON_VERSION
        value: "3.11.0"

databases:
  - name: {data.get('db_name', 'antigravity_db')}
    plan: free
    databaseName: antigravity_prod
'''
                with open(os.path.join(PROJECT_DIR, 'render.yaml'), 'w', encoding='utf-8') as f:
                    f.write(render_yaml)
                extras.append("render.yaml creado (Blueprint)")

                # Build script for Render
                build_sh = '''#!/usr/bin/env bash
pip install -r requirements.txt
python cloud_startup.py
'''
                with open(os.path.join(PROJECT_DIR, 'build.sh'), 'w', encoding='utf-8', newline='\n') as f:
                    f.write(build_sh)
                extras.append("build.sh creado")

            elif provider == 'railway':
                # Procfile
                procfile = 'web: python cloud_startup.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}\n'
                with open(os.path.join(PROJECT_DIR, 'Procfile'), 'w', encoding='utf-8') as f:
                    f.write(procfile)
                extras.append("Procfile creado para Railway")

                # railway.toml
                railway_toml = f'''[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python cloud_startup.py && uvicorn app.main:app --host 0.0.0.0 --port ${{PORT:-8000}}"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
'''
                with open(os.path.join(PROJECT_DIR, 'railway.toml'), 'w', encoding='utf-8') as f:
                    f.write(railway_toml)
                extras.append("railway.toml creado")

            # .python-version (for cloud runtimes)
            with open(os.path.join(PROJECT_DIR, '.python-version'), 'w') as f:
                f.write('3.11.0\n')
            extras.append(".python-version = 3.11.0")

            return {"ok": True, "msg": f"Archivos para {provider.upper()} generados.", "extra": extras}
        except Exception as e:
            return {"ok": False, "msg": str(e)}

    elif action == 'cloud_gen_req':
        try:
            req_file = os.path.join(PROJECT_DIR, 'requirements.txt')
            if os.path.exists(req_file):
                with open(req_file, 'r') as f:
                    deps = [l.strip() for l in f if l.strip()]
                # Ensure gunicorn is present for cloud
                if not any('gunicorn' in d for d in deps):
                    deps.append('gunicorn==22.0.0')
                with open(req_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(deps) + '\n')
                return {"ok": True, "msg": f"requirements.txt verificado ({len(deps)} paquetes).",
                        "extra": [f"Incluido: {', '.join(d.split('==')[0] for d in deps[:6])}..."]}
            return {"ok": False, "msg": "requirements.txt no encontrado"}
        except Exception as e:
            return {"ok": False, "msg": str(e)}

    elif action == 'cloud_git_push':
        try:
            ok1, out1 = run_cmd('git add -A')
            provider = data.get('provider', 'render')
            ok2, out2 = run_cmd(f'git commit -m "deploy: configuracion para {provider.upper()} cloud deployment"')
            if not ok2 and 'nothing to commit' in out2:
                pass  # Already committed
            ok3, out3 = run_cmd('git push origin main')
            if ok3 or 'Everything up-to-date' in out3:
                return {"ok": True, "msg": "Cambios pusheados a GitHub.",
                        "extra": ["Repositorio sincronizado con archivos de deploy."]}
            return {"ok": False, "msg": f"Error en push: {out3[:250]}"}
        except Exception as e:
            return {"ok": False, "msg": str(e)}

    return {"ok": False, "msg": f"Accion desconocida: {action}"}


# ─────────────────────────────────────────────────
#  HTTP Server
# ─────────────────────────────────────────────────

class DeployHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

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
    print(f"\n  ANTIGRAVITY - Deploy Manager")
    print(f"  Interfaz: http://localhost:{PORT}")
    print(f"  Presione Ctrl+C para cerrar\n")
    webbrowser.open(f'http://localhost:{PORT}')
    with socketserver.TCPServer(("", PORT), DeployHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[✓] Deploy Manager detenido.")
            httpd.shutdown()


if __name__ == "__main__":
    main()
