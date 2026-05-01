<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>


Auditoría de Sistema - Aliso Workflow


<div class="space-y-10">
    
    <div class="flex flex-col md:flex-row justify-between items-center gap-6 mb-10">
        <div>
            <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                <span class="w-2 h-10 bg-amber-500 rounded-full shadow-lg shadow-amber-100"></span>
                Trazabilidad / Auditoría
            </h2>
            <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Registro detallado de transacciones y accesos</p>
        </div>
        
        <div class="flex gap-3">
             <a href="/admin/security" class="btn-secondary">
                <span class="text-sm">ðŸ”’</span> VOLVER A SEGURIDAD
            </a>
        </div>
    </div>

    <!-- Filtros -->
    <div class="card-premium mb-8">
        <form hx-get="/admin/audit/filter" hx-target="#audit-results" class="flex flex-wrap items-end gap-6">
            <div class="flex-grow max-w-xs">
                <label class="label-premium">Desde</label>
                <input type="date" name="start_date" value="<?= htmlspecialchars(strval($today ?? "")) ?>" class="input-premium">
            </div>
            <div class="flex-grow max-w-xs">
                <label class="label-premium">Hasta</label>
                <input type="date" name="end_date" value="<?= htmlspecialchars(strval($today ?? "")) ?>" class="input-premium">
            </div>
            <button type="submit" class="btn-primary bg-slate-800 h-[52px] !px-10">FILTRAR LOGS</button>
        </form>
    </div>

    <!-- Tabla de Logs -->
    <div class="card-premium">
        
        <div id="audit-results" class="overflow-x-auto">
            <table class="w-full text-left">
                <thead>
                    <tr class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] border-b border-slate-50">
                        <th class="pb-6 px-4">Estampa Temporal</th>
                        <th class="pb-6 px-4">Usuario</th>
                        <th class="pb-6 px-4">Acción</th>
                        <th class="pb-6 px-4">Entidad</th>
                        <th class="pb-6 px-4 text-center">ID Obj.</th>
                        <th class="pb-6 px-4">Observaciones</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                    <?php foreach ($logs ?? [] as $log): ?>
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="py-6 px-4 font-mono text-[11px] text-slate-500"><?= htmlspecialchars(strval($log->timestamp->format('%d/%m/%Y %H:%M:%S') ?? "")) ?></td>
                        <td class="py-6 px-4">
                            <span class="font-bold text-slate-700"><?= htmlspecialchars(strval($log->$user->username ?? "")) ?></span>
                        </td>
                        <td class="py-6 px-4">
                            {% set action_class = 'bg-slate-100 text-slate-600' %}
                            <?php if (log.action == 'CREAR'): ?>{% set action_class = 'bg-emerald-100 text-emerald-700' %}
                            <?php elseif (log.action == 'BORRAR'): ?>{% set action_class = 'bg-red-100 text-red-700' %}
                            <?php elseif (log.action == 'LOGIN'): ?>{% set action_class = 'bg-sky-100 text-sky-700' %}
                            <?php endif; ?>
                            <span class="px-2.5 py-1 rounded-md text-[9px] font-black uppercase tracking-wider <?= htmlspecialchars(strval($action_class ?? "")) ?>">
                                <?= htmlspecialchars(strval($log->action ?? "")) ?>
                            </span>
                        </td>
                        <td class="py-6 px-4 text-[11px] font-bold text-slate-500 uppercase"><?= htmlspecialchars(strval($log->entity_name ?? "")) ?></td>
                        <td class="py-6 px-4 text-center font-mono text-xs text-slate-400">#<?= htmlspecialchars(strval($log->entity_id || '-' ?? "")) ?></td>
                        <td class="py-6 px-4 text-xs italic text-slate-500"><?= htmlspecialchars(strval($log->details || '-' ?? "")) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        
    </div>

</div>


<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
