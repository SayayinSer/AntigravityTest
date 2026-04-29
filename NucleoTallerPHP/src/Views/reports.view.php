{% extends "base.html" %}

{% block title %}Reportes de Gestión - Aliso Workflow{% endblock %}

{% block head %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
{% endblock %}

{% block content %}
<div class="space-y-10">
    
    <div class="flex flex-col md:flex-row justify-between items-center gap-6 mb-10">
        <div>
            <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                <span class="w-2 h-10 bg-sky-600 rounded-full shadow-lg shadow-sky-100"></span>
                Inteligencia de Negocio
            </h2>
            <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Análisis de costos, productividad y desempeño operativo</p>
        </div>
    </div>

    <!-- Panel de Filtros -->
    <div class="card-premium">
        <h3 class="text-xl font-black text-slate-800 mb-8 flex items-center gap-3">
            <span class="w-1.5 h-6 bg-slate-800 rounded-full"></span> 
            Parámetros del Reporte
        </h3>
        
        <form hx-post="<?= htmlspecialchars(strval($base ?? "")) ?>/reports/generate" hx-target="#report-results" hx-indicator="#loading-report" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div>
                <label class="label-premium">Fecha Inicio</label>
                <input type="date" name="start_date" required class="input-premium">
            </div>
            <div>
                <label class="label-premium">Fecha Fin</label>
                <input type="date" name="end_date" required class="input-premium">
            </div>
            <div>
                <label class="label-premium">Estado de OT</label>
                <select name="status" class="input-premium">
                    <option value="all">Todas las órdenes</option>
                    <option value="Pendiente">Pendientes</option>
                    <option value="En Ejecución">En Ejecución</option>
                    <option value="Terminada">Terminadas</option>
                    <option value="Anulada">Anuladas</option>
                </select>
            </div>
            <div>
                <label class="label-premium">Especialidad / Técnico</label>
                <select name="tech_id" class="input-premium">
                    <option value="">Todos los técnicos</option>
                    <?php foreach ($technicians ?? [] as $tech): ?>
                    <option value="<?= htmlspecialchars(strval($tech->id ?? "")) ?>"><?= htmlspecialchars(strval($tech->name ?? "")) ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="lg:col-span-4 flex justify-end items-center gap-6">
                <div id="loading-report" class="htmx-indicator flex items-center gap-3 text-sky-600 font-bold text-xs">
                    <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    PROCESANDO DATOS...
                </div>
                <button type="submit" class="btn-success bg-emerald-600 hover:bg-emerald-700 text-white py-4 px-12 shadow-emerald-200 group">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 group-hover:rotate-12 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                    <span class="tracking-widest font-black uppercase text-xs">Generar Reporte Maestro</span>
                </button>
            </div>
        </form>
    </div>

    <!-- Resultados (Cargados vía HTMX) -->
    <div id="report-results" class="min-h-[400px] transition-all bg-white/30 rounded-[3rem] border-2 border-dashed border-slate-100 flex items-center justify-center">
        <div class="flex flex-col items-center justify-center py-20 text-slate-300">
            <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" /></svg>
            </div>
            <p class="font-black uppercase tracking-[0.3em] text-[10px] text-slate-400">A la espera de parámetros para procesar datos</p>
            <p class="text-[9px] text-slate-300 mt-2">Seleccione rango de fechas y ejecute el análisis maestro</p>
        </div>
    </div>

</div>
{% endblock %}
