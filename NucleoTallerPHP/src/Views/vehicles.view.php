<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>


Maestro de Móviles - Aliso Workflow


<div x-data="{ showModal: false, vehicleData: {} }">
    
    <!-- Modal Registro (Rediseñado) -->
    <div x-show="showModal" x-cloak class="fixed inset-0 z-[150] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="showModal = false" x-transition.opacity></div>
        <div class="bg-white rounded-[2.5rem] shadow-2xl relative w-full max-w-xl overflow-hidden ring-1 ring-white/20" 
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0 scale-90 translate-y-12"
             x-transition:enter-end="opacity-100 scale-100 translate-y-0">
            
            <div class="bg-slate-900 text-white p-8 flex justify-between items-center">
                <div>
                    <h2 class="text-2xl font-black tracking-tight">Alta de Vehículo</h2>
                    <p class="text-sky-400 text-[10px] font-bold uppercase tracking-widest mt-1">Incorporación de Unidad al Sistema</p>
                </div>
                <button @click="showModal = false" class="text-slate-400 hover:text-white transition-colors $p-2 bg-white/5 rounded-full">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>

            <form hx-post="/vehicles/save" hx-encoding="multipart/form-data" class="p-10 space-y-6">
                <div class="grid grid-cols-2 gap-6">
                    <div class="col-span-1">
                        <label class="label-premium">Patente / Dominio <span class="text-sky-500">*</span></label>
                        <input type="text" name="plate" required placeholder="ABC-123" class="input-premium font-mono uppercase text-center text-lg">
                    </div>
                    <div class="col-span-1">
                        <label class="label-premium">Marca <span class="text-sky-500">*</span></label>
                        <select name="brand_id" required class="input-premium">
                            <?php foreach ($brands ?? [] as $b): ?><option value="<?= htmlspecialchars(strval($b->id ?? "")) ?>"><?= htmlspecialchars(strval($b->name ?? "")) ?></option><?php endforeach; ?>
                        </select>
                    </div>
                    <div class="col-span-1">
                        <label class="label-premium">Tipo de Móvil</label>
                        <select name="type_id" required class="input-premium">
                            <?php foreach ($types ?? [] as $t): ?><option value="<?= htmlspecialchars(strval($t->id ?? "")) ?>"><?= htmlspecialchars(strval($t->name ?? "")) ?></option><?php endforeach; ?>
                        </select>
                    </div>
                    <div class="col-span-1">
                        <label class="label-premium">Modelo / Año</label>
                        <div class="flex gap-2">
                            <input type="text" name="model" placeholder="Model" class="input-premium w-2/3">
                            <input type="number" name="year" placeholder="Año" class="input-premium w-1/3 text-center">
                        </div>
                    </div>
                    <div class="col-span-1">
                        <label class="label-premium">Odómetro Actual</label>
                        <input type="number" name="current_mileage" value="0" class="input-premium font-mono">
                    </div>
                    <div class="col-span-1">
                        <label class="label-premium">Último Service</label>
                        <input type="date" name="last_service_date" class="input-premium text-xs">
                    </div>
                    <div class="col-span-2">
                        <label class="label-premium">Imagen del Vehículo</label>
                        <input type="file" name="photo" accept="image/*" class="text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-[10px] file:font-black file:bg-slate-100 file:text-slate-600 hover:file:bg-sky-50 hover:file:text-sky-600 transition-all">
                    </div>
                </div>

                <div class="flex justify-end gap-4 pt-8 border-t border-slate-50">
                    <button type="button" @click="showModal = false" class="btn-secondary">DESCARTAR</button>
                    <button type="submit" class="btn-primary">DAR DE ALTA MÓVIL</button>
                </div>
            </form>
        </div>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-6">
        <div>
            <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                <span class="w-2 h-10 bg-slate-800 rounded-full shadow-lg"></span>
                Parque Automotor
            </h2>
            <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Control y trazabilidad de unidades pesadas y livianas</p>
        </div>
        
        <button @click="showModal = true" class="btn-primary py-4 px-8 shadow-slate-200 group">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span class="tracking-widest uppercase">Registrar Móvil</span>
        </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <?php if (!$vehicles): ?>
            <div class="col-span-full py-24 text-center card-premium bg-white/50 border-dashed">
                <p class="text-slate-300 font-black uppercase tracking-widest italic font-sans text-sm">No se registran unidades cargadas en el sistema.</p>
            </div>
        <?php endif; ?>
        
        <?php foreach ($vehicles ?? [] as $v): ?>
        <div class="card-premium p-0 overflow-hidden flex flex-col group hover:shadow-2xl transition-all duration-500">
            <!-- Header Imagen -->
            <div class="h-48 relative overflow-hidden bg-slate-900 group-hover:h-56 transition-all duration-500">
                <img src="<?= htmlspecialchars(strval($v->photo_url ?? "")) ?>" alt="Imagen Vehiculo" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-700">
                <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-transparent to-transparent"></div>
                <div class="absolute bottom-4 left-6">
                    <span class="text-[9px] font-black uppercase tracking-[0.2em] text-sky-400">Code: <?= htmlspecialchars(strval($v->internal_code ?? "")) ?></span>
                    <h3 class="text-white text-2xl font-black tracking-tight"><?= htmlspecialchars(strval($v->plate ?? "")) ?></h3>
                </div>
                <div class="absolute top-4 right-4">
                    <span class="bg-white/10 backdrop-blur-md border border-white/20 text-white text-[9px] font-black px-3 py-1.5 rounded-full uppercase tracking-widest">
                        <?php if ($v->vehicle_type): ?><?= htmlspecialchars(strval($v->vehicle_type->name ?? "")) ?><?php else: ?>S/T<?php endif; ?>
                    </span>
                </div>
            </div>
            
            <!-- Cuerpo Info -->
            <div class="p-8 flex-grow space-y-5">
                <div class="flex justify-between items-end border-b border-slate-50 pb-4">
                    <div>
                        <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest">Modelo / Línea</p>
                        <p class="font-black text-slate-800 text-lg leading-tight uppercase"><?= htmlspecialchars(strval($v->brand->name ?? "")) ?> <span class="font-normal text-slate-400 italic"><?= htmlspecialchars(strval($v->model || '-' ?? "")) ?></span></p>
                    </div>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1">
                        <p class="text-[8px] font-black text-slate-300 uppercase tracking-widest">Kilometraje</p>
                        <p class="font-mono font-black text-slate-600 truncate"><?= htmlspecialchars(strval($v->current_mileage ?? "")) ?> KM</p>
                    </div>
                    <div class="space-y-1 border-l border-slate-50 pl-4">
                        <p class="text-[8px] font-black text-slate-300 uppercase tracking-widest">Últ. Service</p>
                        <p class="font-mono font-black text-slate-600 truncate"><?= htmlspecialchars(strval($v->last_service_date)) ?></p>
                    </div>
                </div>
            </div>

            <!-- Footer Acciones -->
            <div class="p-6 bg-slate-50 flex gap-3 border-t border-slate-100/50">
                <a href="/vehicles/<?= htmlspecialchars(strval($v->id ?? "")) ?>/history" class="flex-1 btn-secondary !px-3 !py-2 !text-[10px] justify-center cursor-pointer group">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400 group-hover:text-sky-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                    HISTORIAL
                </a>
                <form hx-post="/vehicles/<?= htmlspecialchars(strval($v->id ?? "")) ?>/delete" class="flex-1">
                    <button type="submit" hx-confirm="CRÍTICO: ¿Desea eliminar permanentemente este móvil y toda su historia?" class="w-full btn-danger !px-3 !py-2 !text-[10px] justify-center group">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-400 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                        ELIMINAR
                    </button>
                </form>
            </div>
        </div>
        <?php endforeach; ?>
    </div>

</div>


<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
