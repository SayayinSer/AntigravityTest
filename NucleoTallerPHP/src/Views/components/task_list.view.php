<div class="overflow-x-auto">
    <table class="w-full text-left">
        <thead>
            <tr class="text-[10px] font-black text-slate-400 uppercase tracking-widest border-b border-slate-50">
                <th class="pb-4 px-2">Descripción del Trabajo</th>
                <th class="pb-4 px-2">Operador Responsable</th>
                <th class="pb-4 px-2 text-center">Tiempo Estimado</th>
                <th class="pb-4 px-2 text-right"></th>
            </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
            <?php foreach ($tasks ?? [] as $task): ?>
            <tr class="group hover:bg-slate-50/50 transition-colors">
                <td class="py-5 px-2">
                    <div class="font-bold text-slate-700 text-sm"><?= htmlspecialchars(strval($task->description ?? "")) ?></div>
                </td>
                <td class="py-5 px-2 font-medium text-slate-500 text-xs">
                    <div class="flex items-center gap-2">
                         <?= htmlspecialchars(strval($task->technician_name ?? "Sin asignar")) ?>
                    </div>
                </td>
                <td class="py-5 px-2 text-center font-mono text-xs font-black text-slate-400">
                    <?= htmlspecialchars(strval($task->duration_minutes ?? "")) ?> MIN
                </td>
                <td class="py-5 px-2 text-right">
                    <?php if (!$is_closed): ?>
                    <button hx-delete="/task/<?= htmlspecialchars(strval($task->id ?? "")) ?>" 
                            hx-confirm="¿Eliminar esta tarea permanente?"
                            hx-target="closest tr" 
                            hx-swap="outerHTML"
                            class="opacity-0 group-hover:opacity-100 $p-2 text-slate-300 hover:text-red-500 transition-all active:scale-90">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                    <?php endif; ?>
                </td>
            </tr>
            <?php endforeach; ?>
            <?php 
                $total_min = 0;
                foreach ($tasks ?? [] as $task) { $total_min += (int)$task->duration_minutes; }
            ?>
            <?php if ($tasks): ?>
            <tr class="bg-slate-50/30">
                <td colspan="2" class="py-4 px-2 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Tiempo Total Acumulado:</td>
                <td class="py-4 px-2 text-center font-mono text-sm font-black text-emerald-600"><?= $total_min ?> MIN</td>
                <td></td>
            </tr>
            <?php else: ?>
            <tr>
                <td colspan="4" class="py-12 text-center text-slate-300 italic font-medium text-sm">No se registran tareas técnicas aún.</td>
            </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

