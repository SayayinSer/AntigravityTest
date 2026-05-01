<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>


Tablas Maestras - Aliso Workflow


<div class="space-y-12">
    
    <div class="flex flex-col md:flex-row justify-between items-center gap-6 mb-10">
        <div>
            <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                <span class="w-2 h-10 bg-slate-400 rounded-full shadow-lg"></span>
                Configuración del Sistema
            </h2>
            <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Gestión de catálogos y entidades transversales</p>
        </div>
    </div>

    <!-- Grilla de Tablas -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
        
        <!-- Marcas y Tipos -->
        <div class="space-y-10">
            <!-- TABLA: Marcas -->
            <div class="card-premium">
                <h3 class="text-xl font-black text-slate-800 mb-6 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-sky-500 rounded-full"></span> 
                    Marcas de Vehículos
                </h3>
                <form hx-post="/admin/brand" class="flex gap-4 mb-8">
                    <input type="text" name="name" placeholder="Nueva Marca..." required class="input-premium">
                    <button type="submit" class="btn-primary !px-4"><span class="text-xl">+</span></button>
                </form>
                <div class="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                    <?php foreach ($brands ?? [] as $b): ?>
                    <div class="flex justify-between items-center p-4 bg-slate-50/50 rounded-2xl border border-slate-100 group transition-all hover:bg-white hover:shadow-sm">
                        <span class="font-bold text-slate-700"><?= htmlspecialchars(strval($b->name ?? "")) ?></span>
                        <form hx-post="/admin/brand/<?= htmlspecialchars(strval($b->id ?? "")) ?>/delete" class="opacity-0 group-hover:opacity-100 transition-opacity">
                            <button type="submit" class="text-red-400 hover:text-red-600 transition-colors" hx-confirm="¿Eliminar esta marca?">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                            </button>
                        </form>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>

            <!-- TABLA: Tipos -->
            <div class="card-premium">
                <h3 class="text-xl font-black text-slate-800 mb-6 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-sky-500 rounded-full"></span> 
                    Tipos de Unidades
                </h3>
                <form hx-post="/admin/type" class="flex gap-4 mb-8">
                    <input type="text" name="name" placeholder="Nuevo Tipo (Bus, Camión, Auto)..." required class="input-premium">
                    <button type="submit" class="btn-primary !px-4"><span class="text-xl">+</span></button>
                </form>
                <div class="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                    <?php foreach ($types ?? [] as $t): ?>
                    <div class="flex justify-between items-center p-4 bg-slate-50/50 rounded-2xl border border-slate-100 group transition-all hover:bg-white hover:shadow-sm">
                        <span class="font-bold text-slate-700"><?= htmlspecialchars(strval($t->name ?? "")) ?></span>
                        <form hx-post="/admin/type/<?= htmlspecialchars(strval($t->id ?? "")) ?>/delete" class="opacity-0 group-hover:opacity-100 transition-opacity">
                            <button type="submit" class="text-red-400 hover:text-red-600 transition-colors" hx-confirm="¿Eliminar este tipo?">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                            </button>
                        </form>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>

        <!-- Técnicos y Geografía -->
        <div class="space-y-10">
            <!-- TABLA: Técnicos -->
            <div class="card-premium">
                <h3 class="text-xl font-black text-slate-800 mb-6 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-emerald-500 rounded-full"></span> 
                    Staff Técnico
                </h3>
                <form hx-post="/admin/tech" class="flex gap-4 mb-8">
                    <input type="text" name="name" placeholder="Nombre Operador..." required class="input-premium">
                    <button type="submit" class="btn-primary bg-emerald-600 shadow-emerald-100 !px-4"><span class="text-xl">+</span></button>
                </form>
                <div class="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                    <?php foreach ($technicians ?? [] as $tech): ?>
                    <div class="flex justify-between items-center p-4 bg-slate-50/50 rounded-2xl border border-slate-100 group transition-all hover:bg-white hover:shadow-sm">
                        <span class="font-bold text-slate-700"><?= htmlspecialchars(strval($tech->name ?? "")) ?></span>
                        <form hx-post="/admin/tech/<?= htmlspecialchars(strval($tech->id ?? "")) ?>/delete" class="opacity-0 group-hover:opacity-100 transition-opacity">
                            <button type="submit" class="text-red-400 hover:text-red-600 transition-colors" hx-confirm="¿Eliminar este técnico?">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                            </button>
                        </form>
                    </div>
                    <?php endforeach; ?>
                </div>
            </div>

            <!-- Geografía -->
            <div class="card-premium">
                <h3 class="text-xl font-black text-slate-800 mb-6 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-slate-800 rounded-full"></span> 
                    Ubicaciones Geográficas
                </h3>
                
                <!-- Países -->
                <div class="mb-8">
                    <p class="label-premium !text-slate-400">Países</p>
                    <form hx-post="/admin/country" class="flex gap-3 mb-4">
                        <input type="text" name="name" placeholder="Nuevo País..." class="input-premium py-2 text-sm">
                        <button type="submit" class="btn-primary !py-2 !px-4 text-xs">AÑADIR</button>
                    </form>
                    <div class="flex flex-wrap gap-2">
                        <?php foreach ($countries ?? [] as $c): ?>
                        <div class="bg-slate-100 px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 flex items-center gap-2 group">
                            <?= htmlspecialchars(strval($c->name ?? "")) ?>
                            <form hx-post="/admin/country/<?= htmlspecialchars(strval($c->id ?? "")) ?>/delete" class="inline">
                                <button type="submit" class="text-slate-300 hover:text-red-500 transition-colors" hx-confirm="¿Eliminar país?">âœ–</button>
                            </form>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </div>

                <!-- Provincias -->
                <div>
                    <p class="label-premium !text-slate-400">Provincias / Estados</p>
                    <form hx-post="/admin/province" class="grid grid-cols-3 gap-3 mb-4">
                        <select name="country_id" class="input-premium py-2 text-xs">
                            <?php foreach ($countries ?? [] as $c): ?><option value="<?= htmlspecialchars(strval($c->id ?? "")) ?>"><?= htmlspecialchars(strval($c->name ?? "")) ?></option><?php endforeach; ?>
                        </select>
                        <input type="text" name="name" placeholder="Nueva Prov..." class="input-premium py-2 text-sm">
                        <button type="submit" class="btn-primary !py-2 !px-4 text-xs">AÑADIR</button>
                    </form>
                    <div class="flex flex-wrap gap-2 max-h-40 overflow-y-auto">
                        <?php foreach ($provinces ?? [] as $p): ?>
                        <div class="bg-sky-50 px-3 py-1.5 rounded-xl border border-sky-100 text-[10px] font-black text-sky-700 flex items-center gap-2">
                            <?= htmlspecialchars(strval($p->name ?? "")) ?> <span class="text-sky-300 font-normal">(<?= htmlspecialchars(strval($p->country->name ?? "")) ?>)</span>
                             <form hx-post="/admin/province/<?= htmlspecialchars(strval($p->id ?? "")) ?>/delete" class="inline">
                                <button type="submit" class="text-sky-300 hover:text-red-500 transition-colors" hx-confirm="¿Eliminar provincia?">âœ–</button>
                            </form>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>


<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
