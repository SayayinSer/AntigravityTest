<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

<div x-data="{ showModal: false, showReport: false }">
    
    <!-- Modales -->
    <?php include BASE_PATH . 'src/Views/components/appointment_modal.view.php'; ?>

    <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-6">
        <div>
            <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                <span class="w-2 h-10 bg-indigo-500 rounded-full shadow-lg shadow-indigo-200"></span>
                Agenda de Recepción
            </h2>
            <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Planificación y seguimiento de turnos programados</p>
        </div>
        
        <div class="flex gap-3">
            <button @click="showReport = !showReport" class="btn-secondary">
                <span class="text-lg">📊</span> REPORTE AGENDA
            </button>
            <button @click="showModal = true" class="btn-primary bg-indigo-600 shadow-indigo-200 hover:bg-indigo-700 py-4 px-8 group">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:rotate-12 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                <span class="tracking-widest uppercase">Nuevo Turno</span>
            </button>
        </div>
    </div>

    <!-- Panel de Reporte (Colapsable) -->
    <div x-show="showReport" x-collapse x-cloak class="card-premium mb-8 border-indigo-100 bg-indigo-50/10">
        <h3 class="text-lg font-black text-slate-700 mb-6 flex items-center gap-2">
            <span class="w-1.5 h-6 bg-indigo-400 rounded-full"></span> 
            Filtros de Búsqueda
        </h3>
        <form hx-post="/appointments/report" hx-target="#report-results" class="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
            <div>
                <label class="label-premium">Desde</label>
                <input type="date" name="start_date" required class="input-premium">
            </div>
            <div>
                <label class="label-premium">Hasta</label>
                <input type="date" name="end_date" required class="input-premium">
            </div>
            <button type="submit" class="btn-primary bg-slate-900 justify-center h-[52px]">GENERAR REPORTE CONSOLIDADO</button>
        </form>
        
        <div id="report-results" class="mt-8"></div>
    </div>

    <!-- Tabla Principal de Agenda -->
    <div class="card-premium overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-50/50">
                        <th class="py-6 px-8 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Horario</th>
                        <th class="py-6 px-8 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Cliente y Móvil</th>
                        <th class="py-6 px-8 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Motivo de Ingreso</th>
                        <th class="py-6 px-8 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Estado</th>
                        <th class="py-6 px-8"></th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                    <?php if (empty($appointments)): ?>
                    <tr>
                        <td colspan="5" class="py-20 text-center">
                            <div class="flex flex-col items-center opacity-30">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                                <p class="text-sm font-bold uppercase tracking-widest">No hay turnos programados para hoy</p>
                            </div>
                        </td>
                    </tr>
                    <?php else: ?>
                    <?php foreach ($appointments as $app): ?>
                    <tr class="group hover:bg-slate-50/80 transition-all">
                        <td class="py-6 px-8">
                            <div class="flex flex-col">
                                <span class="text-lg font-black text-slate-800"><?= $app->scheduled_time ?></span>
                                <span class="text-[10px] font-bold text-slate-400 uppercase"><?= $app->scheduled_date ?></span>
                            </div>
                        </td>
                        <td class="py-6 px-8">
                            <div class="flex flex-col">
                                <span class="font-bold text-slate-700 text-sm"><?= $app->client_name ?></span>
                                <span class="text-xs text-indigo-500 font-mono font-bold"><?= $app->vehicle_plate ?></span>
                            </div>
                        </td>
                        <td class="py-6 px-8">
                            <p class="text-xs text-slate-500 italic max-w-xs truncate"><?= $app->reason ?></p>
                        </td>
                        <td class="py-6 px-8">
                            <span class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest bg-emerald-100 text-emerald-700">Confirmado</span>
                        </td>
                        <td class="py-6 px-8 text-right">
                            <button class="p-2 text-slate-300 hover:text-indigo-600 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" /></svg>
                            </button>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
