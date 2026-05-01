<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>

<div class="space-y-10">
    <div class="flex justify-between items-center bg-slate-900 text-white p-10 rounded-[3rem] shadow-2xl">
        <div>
            <div class="flex items-center gap-4 mb-2">
                <span class="px-4 py-1.5 bg-sky-500 text-white rounded-full text-[10px] font-black uppercase tracking-widest">Historia Clínica</span>
                <span class="text-slate-400 font-mono text-xs">ID: <?= $vehicle->internal_code ?></span>
            </div>
            <h1 class="text-4xl font-black"><?= $vehicle->brand_name ?> <?= $vehicle->model ?></h1>
            <p class="text-sky-400 font-bold uppercase text-xs tracking-widest mt-2"><?= $vehicle->plate ?></p>
        </div>
        <div class="text-right">
            <div class="text-xs text-slate-400 font-bold uppercase tracking-widest mb-1">Kilometraje Actual</div>
            <div class="text-3xl font-black font-mono"><?= number_format((float)$vehicle->current_mileage) ?> KM</div>
        </div>
    </div>

    <div class="space-y-8">
        <h2 class="text-2xl font-black text-slate-800 flex items-center gap-4">
            <span class="w-1.5 h-8 bg-sky-500 rounded-full"></span>
            Cronología de Intervenciones
        </h2>

        <?php if (empty($orders)): ?>
        <div class="card-premium py-20 text-center opacity-40">
            <p class="font-black uppercase tracking-widest text-sm">No se registran órdenes de trabajo previas</p>
        </div>
        <?php else: ?>
        <div class="relative space-y-8 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
            <?php foreach ($orders as $o): ?>
            <div class="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                <div class="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-slate-100 group-hover:bg-sky-500 group-hover:text-white text-slate-400 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 transition-colors">
                    <svg class="fill-current" viewBox="0 0 12 12" width="12" height="12"><path d="M12 10v2H0v-2h12zm0-4v2H0V6h12zm0-4v2H0V2h12z"/></svg>
                </div>
                <div class="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] card-premium !p-8 animate-in slide-in-from-bottom-4">
                    <div class="flex items-center justify-between space-x-2 mb-4">
                        <div class="font-black text-slate-800">Orden #<?= $o->id ?></div>
                        <time class="font-mono text-[10px] font-bold text-sky-600 bg-sky-50 px-3 py-1 rounded-lg uppercase"><?= date('d/m/Y', strtotime($o->entry_date)) ?></time>
                    </div>
                    <div class="text-slate-500 text-sm italic mb-6">"<?= $o->diagnosis ?>"</div>
                    
                    <div class="space-y-4">
                        <div class="p-4 bg-slate-50 rounded-2xl">
                            <h4 class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-2">Tareas Realizadas</h4>
                            <ul class="text-xs space-y-1">
                                <?php foreach ($o->tasks as $t): ?>
                                <li class="text-slate-700 flex items-center gap-2"><span class="w-1 h-1 bg-emerald-400 rounded-full"></span> <?= $t->description ?></li>
                                <?php endforeach; ?>
                            </ul>
                        </div>
                        <div class="p-4 bg-slate-50 rounded-2xl">
                            <h4 class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-2">Materiales Instalados</h4>
                            <ul class="text-xs space-y-1">
                                <?php foreach ($o->parts as $p): ?>
                                <li class="text-slate-700 flex items-center gap-2"><span class="w-1 h-1 bg-sky-400 rounded-full"></span> <?= $p->description ?></li>
                                <?php endforeach; ?>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="mt-6 pt-6 border-t border-slate-50 flex justify-between items-center">
                        <span class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest <?= $o->status == 'Terminada' ? 'bg-slate-100 text-slate-500' : 'bg-emerald-100 text-emerald-700' ?>">
                            <?= $o->status ?>
                        </span>
                        <a href="/order/<?= $o->id ?>" class="text-[10px] font-black text-sky-600 uppercase tracking-widest hover:underline">Ver Detalle Completo →</a>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
