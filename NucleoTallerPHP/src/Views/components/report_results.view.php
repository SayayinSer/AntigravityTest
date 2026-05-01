<!-- report_results.html -->
<div class="space-y-8 animate-in fade-in duration-500">
    
    <!-- Resumen Consolidado -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card-premium !bg-slate-900 text-white">
            <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Total Insumos</h4>
            <div class="text-3xl font-black font-mono tracking-tighter text-sky-400">$<?= htmlspecialchars(strval($parts_total ?? "0.00")) ?></div>
            <p class="text-[9px] font-bold text-slate-400 mt-1 uppercase"><?= htmlspecialchars(strval($parts_count ?? "0")) ?> ítems proyectados</p>
        </div>
        <div class="card-premium !bg-white border-slate-100">
            <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Total Tercerizados</h4>
            <div class="text-3xl font-black font-mono tracking-tighter text-slate-800">$<?= htmlspecialchars(strval($third_total ?? "0.00")) ?></div>
            <p class="text-[9px] font-bold text-slate-400 mt-1 uppercase"><?= htmlspecialchars(strval($third_count ?? "0")) ?> servicios externos</p>
        </div>
        <div class="card-premium !bg-sky-50 border-sky-100">
            <h4 class="text-[10px] font-black text-sky-400 uppercase tracking-widest mb-2">Total Órdenes</h4>
            <div class="text-4xl font-black font-mono tracking-tighter text-sky-600"><?= htmlspecialchars(strval(count($orders ?? []))) ?></div>
            <p class="text-[9px] font-bold text-sky-400 mt-1 uppercase tracking-widest">En período seleccionado</p>
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
                    <?php if (empty($orders)): ?>
                    <tr>
                        <td colspan="6" class="py-20 text-center">
                            <div class="flex flex-col items-center opacity-30">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                                <p class="text-xs font-black uppercase tracking-widest">No se encontraron órdenes en este rango</p>
                            </div>
                        </td>
                    </tr>
                    <?php endif; ?>
                    <?php foreach ($orders ?? [] as $order): 
                        $order = (object)$order;
                    ?>
                    <tr class="hover:bg-slate-50/80 transition-colors">
                        <td class="py-6 px-6">
                            <div class="font-black text-slate-800">#<?= $order->id ?></div>
                        </td>
                        <td class="py-6 px-6">
                            <div class="font-bold text-slate-700"><?= $order->vehicle_model ?? 'Móvil' ?></div>
                        </td>
                        <td class="py-6 px-6 text-sm font-bold text-slate-600">$<?= number_format($order->total_parts_price ?? 0, 2) ?></td>
                        <td class="py-6 px-6 text-sm font-bold text-slate-600">$<?= number_format($order->total_third_party_price ?? 0, 2) ?></td>
                        <td class="py-6 px-6 text-center">
                            <span class="font-mono text-[11px] font-black text-sky-600"><?= $order->work_duration ?? '0' ?>hs</span>
                        </td>
                        <td class="py-6 px-6 text-center">
                            <span class="px-2.5 py-1 rounded-md text-[9px] font-black uppercase tracking-widest bg-sky-100 text-sky-700">
                                <?= $order->status ?? 'Pendiente' ?>
                            </span>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>


