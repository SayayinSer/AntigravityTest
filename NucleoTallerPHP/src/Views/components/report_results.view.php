<!-- report_results.html -->
<div class="space-y-8 animate-in fade-in duration-500">
    
    <!-- Resumen Consolidado -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card-premium !bg-slate-900 text-white">
            <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Total Insumos</h4>
            <div class="text-3xl font-black font-mono tracking-tighter text-sky-400">$<?= htmlspecialchars(strval($parts_total ?? "")) ?></div>
            <p class="text-[9px] font-bold text-slate-400 mt-1 uppercase"><?= htmlspecialchars(strval($parts_count ?? "")) ?> ítems proyectados</p>
        </div>
        <div class="card-premium !bg-white border-slate-100">
            <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Total Tercerizados</h4>
            <div class="text-3xl font-black font-mono tracking-tighter text-slate-800">$<?= htmlspecialchars(strval($third_total ?? "")) ?></div>
            <p class="text-[9px] font-bold text-slate-400 mt-1 uppercase"><?= htmlspecialchars(strval($third_count ?? "")) ?> servicios externos</p>
        </div>
        <div class="card-premium !bg-sky-50 border-sky-100">
            <h4 class="text-[10px] font-black text-sky-400 uppercase tracking-widest mb-2">Total Órdenes</h4>
            <div class="text-4xl font-black font-mono tracking-tighter text-sky-600"><?= htmlspecialchars(strval(count($orders ?? []) ?? "")) ?></div>
            <p class="text-[9px] font-bold text-sky-400 mt-1 uppercase tracking-widest">En período seleccionado</p>
        </div>
    </div>

    <!-- Desempeño por Técnico -->
    <div class="card-premium">
        <h3 class="text-sm font-black text-slate-800 uppercase tracking-widest mb-6 flex items-center gap-3">
             <span class="w-1.5 h-6 bg-emerald-500 rounded-full"></span> 
             Productividad del Personal Técnico
        </h3>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            <?php foreach ($tech_stats ?? [] as $tech): ?>
            <div class="p-5 bg-slate-50 rounded-[1.5rem] border border-slate-100 text-center">
                <div class="text-[10px] font-black text-slate-400 uppercase mb-2 truncate"><?= htmlspecialchars(strval($tech->name ?? "")) ?></div>
                <div class="text-lg font-black text-emerald-600 font-mono"><?= htmlspecialchars(strval($tech->formatted ?? "")) ?></div>
                <div class="text-[8px] font-black text-slate-300 uppercase mt-1">Hs Laboradas</div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>

    <!-- Listado de Órdenes -->
    <div class="card-premium p-0 overflow-hidden ring-1 ring-slate-100">
        <div class="overflow-x-auto">
            <table class="w-full text-left">
                <thead>
                    <tr class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] border-b border-slate-50 bg-slate-50/50">
                        <th class="py-4 px-6">ID / Fecha</th>
                        <th class="py-4 px-6">Marca / Modelo</th>
                        <th class="py-4 px-6">Insumos</th>
                        <th class="py-4 px-6">Terceros</th>
                        <th class="py-4 px-6 text-center">Labor</th>
                        <th class="py-4 px-6 text-center">Estado</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                    <?php foreach ($orders ?? [] as $order): ?>
                    <tr class="hover:bg-slate-50/80 transition-colors">
                        <td class="py-6 px-6">
                            <div class="font-black text-slate-800">#<?= htmlspecialchars(strval($order->id ?? "")) ?></div>
                            <div class="text-[10px] text-slate-400 font-bold"><?= htmlspecialchars(strval($order->entry_date->strftime('%d/%m/%y') ?? "")) ?></div>
                        </td>
                        <td class="py-6 px-6">
                            <div class="font-bold text-slate-700"><?= htmlspecialchars(strval($order->vehicle->brand->name ?? "")) ?></div>
                            <div class="text-[10px] font-mono text-slate-400 uppercase tracking-tighter"><?= htmlspecialchars(strval($order->vehicle->model ?? "")) ?> &bull; <?= htmlspecialchars(strval($order->vehicle->plate ?? "")) ?></div>
                        </td>
                        <td class="py-6 px-6 text-sm font-bold text-slate-600">$<?= htmlspecialchars(strval($"{:,->2f}"->format(order->total_parts_price) ?? "")) ?></td>
                        <td class="py-6 px-6 text-sm font-bold text-slate-600">$<?= htmlspecialchars(strval($"{:,->2f}"->format(order->total_third_party_price) ?? "")) ?></td>
                        <td class="py-6 px-6 text-center">
                            <span class="font-mono text-[11px] font-black text-sky-600"><?= htmlspecialchars(strval($order->work_duration ?? "")) ?>hs</span>
                        </td>
                        <td class="py-6 px-6 text-center">
                            <span class="px-2.5 py-1 rounded-md text-[9px] font-black uppercase tracking-widest <?php if (order.status == 'Terminada'): ?>bg-slate-200 text-slate-600<?php elseif (order.status == 'Anulada'): ?>bg-red-100 text-red-700<?php else: ?>bg-sky-100 text-sky-700<?php endif; ?>">
                                <?= htmlspecialchars(strval($order->status ?? "")) ?>
                            </span>
                        </td>
                    </tr>
                    <?php else: ?>
                    <tr>
                        <td colspan="6" class="py-20 text-center">
                            <div class="flex flex-col items-center opacity-30">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                                <p class="text-xs font-black uppercase tracking-widest">No se encontraron órdenes en este rango</p>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <div class="p-6 bg-slate-900 flex justify-between items-center">
            <div class="text-white text-[10px] font-black uppercase tracking-widest opacity-40 italic">Generado por Aliso Workflow Engine &bull; Argentina</div>
            <button onclick="window.print()" class="btn-primary !py-2.5 !px-8 !bg-white !text-slate-900 shadow-none border-none">
                EXPEDIR DOCUMENTO PDF
            </button>
        </div>
    </div>
</div>
