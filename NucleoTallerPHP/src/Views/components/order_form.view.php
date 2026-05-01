<div class="glass p-8 rounded-2xl shadow-2xl max-w-2xl mx-auto">
    <h2 class="text-2xl font-bold mb-6 text-sky-900">Nueva Orden de Trabajo</h2>
    
    <form hx-post="/order/save" class="space-y-6">
        <div>
            <label class="block text-sm font-bold text-slate-600 mb-2 uppercase tracking-wide">Seleccionar Vehículo</label>
            <select name="vehicle_id" required class="w-full $p-3 border-2 border-slate-100 rounded-xl focus:border-sky-500 transition-colors outline-none bg-white">
                <option value="">-- Seleccione un móvil registrado --</option>
                <?php foreach ($vehicles ?? [] as $v): ?>
                <option value="<?= htmlspecialchars(strval($v->id ?? "")) ?>"><?= htmlspecialchars(strval($v->brand->name ?? "")) ?> <?= htmlspecialchars(strval($v->model ?? "")) ?> (<?= htmlspecialchars(strval($v->plate ?? "")) ?>)</option>
                <?php endforeach; ?>
            </select>
        </div>

        <div>
            <label class="block text-sm font-bold text-slate-600 mb-2 uppercase tracking-wide">Diagnóstico Inicial</label>
            <textarea name="diagnosis" rows="4" placeholder="Describa el problema o motivo del ingreso..." class="w-full $p-3 border-2 border-slate-100 rounded-xl focus:border-sky-500 transition-colors outline-none bg-white"></textarea>
        </div>

        <div class="flex gap-4 pt-4">
            <button type="submit" class="flex-1 bg-sky-600 text-white font-bold py-3 rounded-xl shadow-lg hover:bg-sky-700 hover:-translate-y-0.5 transition-all">
                Crear Orden
            </button>
            <a href="/" class="flex-1 bg-slate-100 text-slate-600 font-bold py-3 rounded-xl border border-slate-200 text-center hover:bg-slate-200 transition-all">
                Cancelar
            </a>
        </div>
    </form>
</div>

