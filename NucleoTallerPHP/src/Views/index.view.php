<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>

<div id="main-panel" class="grid gap-8">
    <div class="card-premium">
        <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
            <div>
                <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                    <span class="w-2 h-10 bg-sky-500 rounded-full shadow-lg shadow-sky-200"></span>
                    Panel de Operaciones
                </h2>
                <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Gestión de Órdenes de Trabajo en Tiempo Real</p>
            </div>
            
            <button hx-get="/order/new" hx-target="#main-panel" class="btn-primary py-4 px-8 shadow-sky-200 group">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:rotate-90 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                <span class="tracking-widest">NUEVA ORDEN</span>
            </button>
        </div>
        
        <div class="overflow-x-auto -mx-4 md:mx-0">
            <table class="w-full text-left">
                <thead>
                    <tr class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] border-b border-slate-100">
                        <th class="pb-6 px-4">Orden</th>
                        <th class="pb-6 px-4">Móvil / Vehículo</th>
                        <th class="pb-6 px-4 text-center">Estado</th>
                        <th class="pb-6 px-6 text-center">Producción</th>
                        <th class="pb-6 px-6 text-right">Inversión</th>
                        <th class="pb-6 px-4 text-right">Gestión</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                    <?php if (empty($orders)): ?>
                        <tr>
                            <td colspan="6" class="py-24 text-center">
                                <div class="flex flex-col items-center gap-4 text-slate-300">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                    </svg>
                                    <p class="text-sm italic font-medium">No hay órdenes registradas en este período.</p>
                                </div>
                            </td>
                        </tr>
                    <?php endif; ?>
                    <?php foreach ($orders ?? [] as $order): 
                        $order = (object)$order;
                        $status_class = 'bg-sky-100 text-sky-700';
                        if (($order->status ?? '') == 'Terminada') $status_class = 'bg-slate-200 text-slate-600 font-medium';
                        elseif (($order->status ?? '') == 'Anulada') $status_class = 'bg-red-100 text-red-700';
                        elseif (($order->status ?? '') == 'En Ejecución') $status_class = 'bg-amber-100 text-amber-700 animate-pulse';
                    ?>
                    <tr class="hover:bg-slate-50/80 transition-all group">
                        <td class="py-8 px-4">
                            <span class="text-xl font-black text-slate-400 group-hover:text-sky-600 transition-colors">#<?= $order->id ?></span>
                        </td>
                        <td class="py-8 px-4">
                            <div class="flex flex-col">
                                <span class="font-bold text-slate-700 text-lg"><?= $order->vehicle->brand->name ?? 'Móvil' ?> <span class="font-normal text-slate-400"><?= $order->vehicle->model ?? '' ?></span></span>
                                <div class="flex items-center gap-2 mt-1">
                                    <span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md font-mono border border-slate-200"><?= $order->vehicle->plate ?? '' ?></span>
                                </div>
                            </div>
                        </td>
                        <td class="py-8 px-4 text-center">
                            <span class="px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-wider <?= $status_class ?>">
                                <?= $order->status ?? 'Pendiente' ?>
                            </span>
                        </td>
                        <td class="py-8 px-6 text-center">
                            <div class="flex flex-col items-center gap-1">
                                <span class="font-mono font-black text-slate-700"><?= $order->formatted_time ?? '00:00:00' ?></span>
                                <span class="text-[8px] text-slate-400 font-black uppercase tracking-widest">Hs de Trabajo</span>
                            </div>
                        </td>
                        <td class="py-8 px-6 text-right">
                            <span class="text-xl font-black text-slate-900 font-mono tracking-tighter">$<?= number_format((float)($order->total_cost ?? 0), 2) ?></span>
                        </td>
                        <td class="py-8 px-4 text-right">
                            <div class="flex items-center justify-end gap-3">
                                <a href="/order/<?= $order->id ?>" class="bg-slate-800 text-white px-5 py-2.5 rounded-xl text-[10px] font-black hover:bg-sky-600 transition-all shadow-md active:scale-95 inline-flex items-center gap-2">
                                    GESTIONAR OT
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                                </a>
                                <?php if (($order->status ?? '') == 'Pendiente'): ?>
                                <form hx-post="/order/<?= $order->id ?>/delete" class="inline">
                                    <button type="submit" hx-confirm="¿Seguro desea ELIMINAR esta orden PENDIENTE?" class="p-2.5 bg-slate-100 text-red-400 hover:bg-red-500 hover:text-white rounded-xl transition-all active:scale-90" title="Eliminar Orden">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12" /></svg>
                                    </button>
                                </form>
                                <?php endif; ?>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>

