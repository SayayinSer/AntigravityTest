<!-- new_order_modal.view.php -->
<div id="order-modal" x-data="{ open: true }" x-show="open" x-cloak class="fixed inset-0 z-[150] flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-md" @click="open = false; setTimeout(() => $el.remove(), 300)" x-transition.opacity></div>
    <div class="bg-white rounded-[2.5rem] shadow-2xl relative w-full max-w-lg overflow-hidden ring-1 ring-white/20" 
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0 scale-90 translate-y-12"
         x-transition:enter-end="opacity-100 scale-100 translate-y-0">
        
        <div class="bg-slate-900 text-white p-8 flex justify-between items-center">
            <div>
                <h2 class="text-2xl font-black tracking-tight">Nueva Orden de Trabajo</h2>
                <p class="text-sky-400 text-[10px] font-bold uppercase tracking-widest mt-1">Apertura de Incidente Técnico</p>
            </div>
            <button @click="open = false; setTimeout(() => document.getElementById('order-modal').remove(), 300)" class="text-slate-400 hover:text-white transition-colors p-2 bg-white/5 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
        </div>

        <form hx-post="/order/save" class="p-10 space-y-8">
            <div>
                <label class="label-premium">Seleccionar Móvil en Recinto <span class="text-sky-500">*</span></label>
                <select name="vehicle_id" required class="input-premium">
                    <option value="">Seleccione una unidad...</option>
                    <?php foreach ($vehicles ?? [] as $v): ?>
                        <option value="<?= $v->id ?>"><?= $v->plate ?> - <?= $v->brand->name ?> <?= $v->model ?></option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div>
                <label class="label-premium">Diagnóstico / Motivo de Ingreso <span class="text-sky-500">*</span></label>
                <textarea name="diagnosis" required placeholder="Describa la falla o trabajo solicitado..." class="input-premium h-32 focus:ring-sky-500"></textarea>
            </div>

            <div class="flex justify-end gap-4 pt-4 border-t border-slate-50">
                <button type="button" @click="open = false; setTimeout(() => $el.remove(), 300)" class="btn-secondary">DESCARTAR</button>
                <button type="submit" class="btn-primary">ABRIR ORDEN DE TRABAJO</button>
            </div>
        </form>
    </div>
</div>
