<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>

<?php
    $is_closed = ($order->status == 'Terminada' || $order->status == 'Anulada');
    $status_color = 'bg-sky-500';
    if ($order->status == 'Terminada') $status_color = 'bg-slate-500';
    elseif ($order->status == 'Anulada') $status_color = 'bg-red-500';
?>

<div x-data="{ state: '<?= $order->status ?>' }">
    <?php include BASE_PATH . 'src/Views/components/confirm_modal.view.php'; ?>
    
    <div id="order-header" hx-get="/order/<?= $order->id ?>/header" hx-trigger="load, refresh-header from:body" class="mb-10">
        <div class="animate-pulse bg-white h-32 rounded-[2.5rem] shadow-sm"></div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div class="lg:col-span-1 space-y-8">
            <div class="card-premium p-8">
                <div class="flex justify-between items-start mb-6">
                    <h2 class="text-xl font-black text-slate-800">Vehículo</h2>
                    <span class="text-[9px] font-black bg-slate-900 text-white px-3 py-1 rounded-full uppercase tracking-widest">ID: <?= $order->vehicle->internal_code ?></span>
                </div>
                <div class="space-y-4">
                    <div class="flex justify-between items-center py-3 border-b border-slate-50">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Marca</span>
                        <span class="font-bold text-slate-700"><?= $order->vehicle->brand->name ?></span>
                    </div>
                    <div class="flex justify-between items-center py-3 border-b border-slate-50">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Modelo</span>
                        <span class="font-bold text-slate-700"><?= $order->vehicle->model ?></span>
                    </div>
                    <div class="flex justify-between items-center py-3">
                        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Patente</span>
                        <span class="font-mono bg-amber-50 text-amber-800 px-3 py-1 rounded-lg border border-amber-100 font-bold"><?= $order->vehicle->plate ?></span>
                    </div>
                </div>
            </div>

            <div id="order-summary" hx-get="/order/<?= $order->id ?>/summary" hx-trigger="load, refreshSummary from:body">
                <div class="animate-pulse bg-slate-200 h-48 rounded-[2rem]"></div>
            </div>

            <div class="card-premium p-8">
                <h2 class="text-xl font-black text-slate-800 mb-6">Estado Operativo</h2>
                <div id="status-display" class="mb-8">
                    <div class="flex items-center gap-3">
                        <span class="w-3 h-3 rounded-full <?= $status_color ?> shadow-lg"></span>
                        <span class="font-black text-slate-700 uppercase tracking-widest text-sm"><?= $order->status ?></span>
                    </div>
                </div>
                <?php if (!$is_closed): ?>
                <div class="space-y-6" x-data="{ currentStatus: '<?= $order->status ?>' }">
                    <select x-model="currentStatus" name="status" class="input-premium font-bold text-sm">
                        <option value="Pendiente">Pendiente</option>
                        <option value="En Ejecución">En Ejecución</option>
                        <option value="Terminada">Terminada (Cerrar)</option>
                        <option value="Anulada">Anulada</option>
                    </select>
                    <button type="button" @click="htmx.ajax('POST', '/order/<?= $order->id ?>/status', { values: { status: currentStatus } })" class="btn-primary w-full justify-center py-4">ACTUALIZAR ESTADO</button>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <div class="lg:col-span-2 space-y-8">
            <!-- Tareas -->
            <div class="bg-white rounded-[2.5rem] shadow-xl border border-slate-100 overflow-hidden" x-data="{ expanded: true }">
                <div class="p-8 bg-white border-b border-slate-50 flex justify-between items-center cursor-pointer" @click="expanded = !expanded">
                    <h2 class="text-2xl font-black flex items-center gap-4 text-slate-800"><span class="w-2 h-8 bg-emerald-500 rounded-full"></span> Tareas Realizadas</h2>
                </div>
                <div x-show="expanded" x-collapse class="p-8">
                    <?php if (!$is_closed): ?>
                    <div class="mb-10 p-8 bg-emerald-50/20 border border-emerald-100/50 rounded-[2rem]">
                        <form hx-post="/order/<?= $order->id ?>/task" hx-target="#task-list" @htmx:after-request="this.reset()" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div class="md:col-span-2">
                                <label class="label-premium !text-emerald-700/50">Descripción del Trabajo</label>
                                <input type="text" name="description" placeholder="Ej: Cambio de filtros" required class="input-premium">
                            </div>
                            <div>
                                <label class="label-premium !text-emerald-700/50">Minutos</label>
                                <input type="number" name="duration" placeholder="Min" required class="input-premium font-mono">
                            </div>
                            <div>
                                <label class="label-premium !text-emerald-700/50">Técnico</label>
                                <select name="tech_id" class="input-premium">
                                    <?php foreach ($technicians ?? [] as $tech): ?><option value="<?= $tech->id ?>"><?= $tech->name ?></option><?php endforeach; ?>
                                </select>
                            </div>
                            <button type="submit" class="md:col-span-4 btn-primary bg-emerald-600 justify-center py-4">REGISTRAR LABOR TÉCNICA</button>
                        </form>
                    </div>
                    <?php endif; ?>
                    <div id="task-list"><?php $tasks = $order->tasks ?? []; include BASE_PATH . 'src/Views/components/task_list.view.php'; ?></div>
                </div>
            </div>

            <!-- Materiales -->
            <div class="bg-white rounded-[2.5rem] shadow-xl border border-slate-100 overflow-hidden" x-data="{ expanded: true }">
                <div class="p-8 bg-white border-b border-slate-50 flex justify-between items-center cursor-pointer" @click="expanded = !expanded">
                    <h2 class="text-2xl font-black flex items-center gap-4 text-slate-800"><span class="w-2 h-8 bg-sky-500 rounded-full"></span> Insumos y Materiales</h2>
                </div>
                <div x-show="expanded" x-collapse class="p-8">
                    <?php if (!$is_closed): ?>
                    <div class="mb-10 p-8 bg-sky-50/20 border border-sky-100/50 rounded-[2rem]">
                        <form hx-post="/order/<?= $order->id ?>/part" hx-target="#part-list" @htmx:after-request="this.reset()" class="grid grid-cols-1 md:grid-cols-5 gap-4">
                            <div class="md:col-span-1">
                                <label class="label-premium !text-sky-700/50">Artículo</label>
                                <input type="text" name="description" placeholder="Repuesto" required class="input-premium">
                            </div>
                            <div>
                                <label class="label-premium !text-sky-700/50">Cant.</label>
                                <input type="number" step="0.01" name="qty" placeholder="0" required class="input-premium">
                            </div>
                            <div>
                                <label class="label-premium !text-sky-700/50">UOM</label>
                                <input type="text" name="uom" placeholder="Un/Lt" class="input-premium">
                            </div>
                            <div>
                                <label class="label-premium !text-sky-700/50">P. Unitario</label>
                                <input type="number" step="0.01" name="price" placeholder="$" required class="input-premium">
                            </div>
                            <button type="submit" class="btn-primary justify-center py-4 self-end">AÑADIR</button>
                        </form>
                    </div>
                    <?php endif; ?>
                    <div id="part-list"><?php $parts = $order->parts ?? []; include BASE_PATH . 'src/Views/components/part_list.view.php'; ?></div>
                </div>
            </div>

            <!-- Terceros -->
            <div class="bg-white rounded-[2.5rem] shadow-xl border border-slate-100 overflow-hidden" x-data="{ expanded: true }">
                <div class="p-8 bg-white border-b border-slate-50 flex justify-between items-center cursor-pointer" @click="expanded = !expanded">
                    <h2 class="text-2xl font-black flex items-center gap-4 text-slate-800"><span class="w-2 h-8 bg-amber-500 rounded-full"></span> Servicios de Terceros</h2>
                </div>
                <div x-show="expanded" x-collapse class="p-8">
                    <?php if (!$is_closed): ?>
                    <div class="mb-10 p-8 bg-amber-50/20 border border-amber-100/50 rounded-[2rem]">
                        <form hx-post="/order/<?= $order->id ?>/third-party" hx-target="#third-party-list" @htmx:after-request="this.reset()" class="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div>
                                <label class="label-premium !text-amber-700/50">Proveedor</label>
                                <input type="text" name="provider" placeholder="Nombre" required class="input-premium">
                            </div>
                            <div class="md:col-span-1">
                                <label class="label-premium !text-amber-700/50">Servicio</label>
                                <input type="text" name="description" placeholder="Ej: Rectificación" required class="input-premium">
                            </div>
                            <div>
                                <label class="label-premium !text-amber-700/50">Costo ($)</label>
                                <input type="number" step="0.01" name="price" placeholder="0.00" required class="input-premium">
                            </div>
                            <button type="submit" class="btn-primary bg-amber-600 justify-center py-4 self-end">REGISTRAR</button>
                        </form>
                    </div>
                    <?php endif; ?>
                    <div id="third-party-list"><?php $third_parties = $order->third_parties ?? []; include BASE_PATH . 'src/Views/components/third_party_list.view.php'; ?></div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
