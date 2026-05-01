<!-- appointment_report_results.html -->
<div class="card-premium !bg-white p-0 overflow-hidden border-indigo-100 ring-1 ring-indigo-50 animate-in slide-in-from-top-4">
    <div class="overflow-x-auto">
        <table class="w-full text-left">
            <thead>
                <tr class="text-[10px] font-black text-slate-400 uppercase tracking-widest border-b border-slate-50 bg-slate-50/50">
                    <th class="py-4 px-6">Programación</th>
                    <th class="py-4 px-6">Cliente / Contacto</th>
                    <th class="py-4 px-6">Móvil</th>
                    <th class="py-4 px-6">Motivo</th>
                    <th class="py-4 px-6 text-center">Estado</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
                <?php if (empty($results)): ?>
                <tr><td colspan="5" class="py-16 text-center text-slate-300 font-medium text-sm">No se hallaron turnos en el rango seleccionado.</td></tr>
                <?php endif; ?>
                <?php foreach ($results ?? [] as $apt): 
                    $dt = new \DateTime($apt->scheduled_date);
                ?>
                <tr class="hover:bg-indigo-50/30 transition-colors">
                    <td class="py-5 px-6">
                        <div class="font-black text-slate-800 text-sm"><?= $dt->format('d/m/Y') ?></div>
                        <div class="text-[10px] font-black text-indigo-500 font-mono"><?= $dt->format('H:i') ?>hs</div>
                    </td>
                    <td class="py-5 px-6">
                        <div class="font-bold text-slate-700"><?= htmlspecialchars(strval($apt->client_name ?? "")) ?></div>
                        <div class="text-[10px] text-slate-400 font-bold"><?= htmlspecialchars(strval($apt->client_email ?? "")) ?></div>
                    </td>
                    <td class="py-5 px-6">
                        <span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-lg font-mono font-black text-[10px] border border-slate-200">
                             <?= htmlspecialchars(strval($apt->plate ?? "---")) ?>
                        </span>
                    </td>
                    <td class="py-5 px-6">
                        <p class="text-[11px] text-slate-500 max-w-[200px] truncate" title="<?= htmlspecialchars(strval($apt->reason ?? "")) ?>"><?= htmlspecialchars(strval($apt->reason ?? "")) ?></p>
                    </td>
                    <td class="py-5 px-6 text-center">
                        <span class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest <?php if ($apt->status == 'Atendido'): ?>bg-emerald-100 text-emerald-700<?php elseif ($apt->status == 'Cancelado'): ?>bg-red-100 text-red-700<?php else: ?>bg-amber-100 text-amber-700<?php endif; ?>">
                            <?= htmlspecialchars(strval($apt->status ?? "")) ?>
                        </span>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <div class="p-4 bg-slate-900 flex justify-end">
        <button onclick="window.print()" class="btn-primary !py-2 !px-6 !text-[10px] !bg-white !text-slate-900 border-none flex items-center gap-2">
            <span>🖨️</span> IMPRIMIR REPORTE
        </button>
    </div>
</div>
