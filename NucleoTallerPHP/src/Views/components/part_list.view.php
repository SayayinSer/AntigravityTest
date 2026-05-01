<div class="overflow-x-auto">
    <table class="w-full text-left">
        <thead>
            <tr class="text-[10px] font-black text-slate-400 uppercase tracking-widest border-b border-slate-50">
                <th class="pb-4 px-2">Material / Repuesto</th>
                <th class="pb-4 px-2 text-center">Cant.</th>
                <th class="pb-4 px-2 text-center">UOM</th>
                <th class="pb-4 px-2 text-right">Precio Unit.</th>
                <th class="pb-4 px-2 text-right">Subtotal</th>
                <th class="pb-4 px-2 text-right"></th>
            </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
            <?php foreach ($parts ?? [] as $part): ?>
            <tr class="group hover:bg-slate-50/50 transition-colors">
                <td class="py-5 px-2">
                    <div class="font-bold text-slate-700 text-sm"><?= htmlspecialchars(strval($part->description ?? "")) ?></div>
                </td>
                <td class="py-5 px-2 text-center font-mono font-black text-slate-600">
                    <?= htmlspecialchars(strval($part->quantity ?? "")) ?>
                </td>
                <td class="py-5 px-2 text-center text-[10px] font-black text-slate-400 uppercase">
                    <?= htmlspecialchars(strval($part->uom || '-' ?? "")) ?>
                </td>
                <td class="py-5 px-2 text-right font-mono text-xs text-slate-500">
                    $<?= htmlspecialchars(strval(number_format($part->unit_price, 2) ?? "")) ?>
                </td>
                <td class="py-5 px-2 text-right font-mono font-black text-slate-900">
                    $<?= htmlspecialchars(strval(number_format($part->quantity * $part->unit_price, 2) ?? "")) ?>
                </td>
                <td class="py-5 px-2 text-right">
                    <?php if (!$is_closed): ?>
                    <button hx-delete="/part/<?= htmlspecialchars(strval($part->id ?? "")) ?>" 
                            hx-confirm="¿Desea dar de baja este insumo?"
                            hx-target="closest tr" 
                            hx-swap="outerHTML"
                            class="opacity-0 group-hover:opacity-100 $p-2 text-slate-300 hover:text-red-500 transition-all active:scale-90">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                    <?php endif; ?>
                </td>
            </tr>
            <?php endforeach; ?>
            <?php 
                $total_parts = 0;
                foreach ($parts ?? [] as $part) { $total_parts += ((float)$part->quantity * (float)$part->unit_price); }
            ?>
            <?php if ($parts): ?>
            <tr class="bg-slate-50/30">
                <td colspan="4" class="py-4 px-2 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Subtotal Materiales:</td>
                <td class="py-4 px-2 text-right font-mono text-sm font-black text-sky-600">$<?= number_format($total_parts, 2) ?></td>
                <td></td>
            </tr>
            <?php else: ?>
            <tr>
                <td colspan="6" class="py-12 text-center text-slate-300 italic font-medium text-sm">Sin materiales registrados en esta orden.</td>
            </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

