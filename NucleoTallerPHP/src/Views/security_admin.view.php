<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>


Seguridad Central - Aliso Workflow


<div class="space-y-12">
    
    <div class="flex flex-col md:flex-row justify-between items-center gap-6 mb-10">
        <div>
            <h2 class="text-3xl font-black text-slate-800 flex items-center gap-4">
                <span class="w-2 h-10 bg-slate-900 rounded-full shadow-lg"></span>
                Control de Accesos (GAM)
            </h2>
            <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-2 ml-6">Gestión de identidades, roles y políticas de seguridad</p>
        </div>
        
        <div class="flex gap-3">
             <a href="/admin/audit" class="btn-secondary border-amber-200 text-amber-700 bg-amber-50/30">
                <span class="text-sm">ðŸ“‹</span> VER AUDITORÃA
            </a>
        </div>
    </div>

    <!-- Gestión de Usuarios -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        
        <!-- Formulario Alta -->
        <div class="lg:col-span-1">
            <div class="card-premium h-full">
                <h3 class="text-xl font-black text-slate-800 mb-8 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-slate-800 rounded-full"></span> 
                    Enrolar Operador
                </h3>
                
                <form hx-post="/admin/security/$user" class="space-y-6">
                    <div>
                        <label class="label-premium">Username <span class="text-sky-500">*</span></label>
                        <input type="text" name="username" required class="input-premium">
                    </div>
                    <div>
                        <label class="label-premium">Nombre Completo <span class="text-sky-500">*</span></label>
                        <input type="text" name="full_name" required class="input-premium">
                    </div>
                    <div>
                        <label class="label-premium">Email</label>
                        <input type="email" name="email" class="input-premium">
                    </div>
                    <div>
                        <label class="label-premium">Password Provisoria <span class="text-sky-500">*</span></label>
                        <input type="password" name="password" required class="input-premium">
                    </div>
                    <div>
                        <label class="label-premium">Rol Principal</label>
                        <select name="role_id" class="input-premium">
                            <?php foreach ($roles ?? [] as $role): ?><option value="<?= htmlspecialchars(strval($role->id ?? "")) ?>"><?= htmlspecialchars(strval($role->name ?? "")) ?></option><?php endforeach; ?>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary w-full justify-center py-4 bg-slate-900">CREAR CUENTA</button>
                </form>
            </div>
        </div>

        <!-- Lista de Usuarios -->
        <div class="lg:col-span-2">
            <div class="card-premium h-full">
                <h3 class="text-xl font-black text-slate-800 mb-8 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-slate-800 rounded-full"></span> 
                    Directorio de Cuentas
                </h3>
                
                <div class="overflow-x-auto">
                    <table class="w-full text-left">
                        <thead>
                            <tr class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] border-b border-slate-100">
                                <th class="pb-6 px-4">Usuario / Email</th>
                                <th class="pb-6 px-4">Nombre Real</th>
                                <th class="pb-6 px-4">Estado</th>
                                <th class="pb-6 px-4">Roles</th>
                                <th class="pb-6 px-4 text-right">Gestión</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-50">
                            <?php foreach ($users ?? [] as $u): ?>
                            <tr class="hover:bg-slate-50/50 transition-all group">
                                <td class="py-6 px-4">
                                    <div class="font-black text-slate-700"><?= htmlspecialchars(strval($u->username ?? "")) ?></div>
                                    <div class="text-[10px] text-slate-400 font-bold mt-0.5"><?= htmlspecialchars(strval($u->email || 'sin email' ?? "")) ?></div>
                                </td>
                                <td class="py-6 px-4 text-xs font-bold text-slate-600"><?= htmlspecialchars(strval($u->full_name ?? "")) ?></td>
                                <td class="py-6 px-4">
                                    <?php if ($u->status == 'Activo'): ?>
                                        <span class="px-2.5 py-1 bg-emerald-100 text-emerald-700 rounded-full text-[9px] font-black uppercase tracking-widest">ACTIVO</span>
                                    <?php else: ?>
                                        <span class="px-2.5 py-1 bg-red-100 text-red-700 rounded-full text-[9px] font-black uppercase tracking-widest">SUSPENDIDO</span>
                                    <?php endif; ?>
                                </td>
                                <td class="py-6 px-4">
                                    <div class="flex flex-wrap gap-1">
                                        <?php foreach ($u->roles ?? [] as $role): ?>
                                        <span class="text-[8px] bg-slate-100 text-slate-500 font-black px-2 py-0.5 border border-slate-200 rounded-md"><?= htmlspecialchars(strval($role->name ?? "")) ?></span>
                                        <?php endforeach; ?>
                                    </div>
                                </td>
                                <td class="py-6 px-4 text-right">
                                    <form hx-post="/admin/$user/<?= htmlspecialchars(strval($u->id ?? "")) ?>/toggle-status" class="inline">
                                        <button type="submit" class="text-[10px] font-black uppercase <?php if ($u->status == 'Activo'): ?>text-red-400 hover:text-red-600 hover:bg-red-50<?php else: ?>text-emerald-400 hover:text-emerald-600 hover:bg-emerald-50<?php endif; ?> px-3 py-2 rounded-xl transition-all">
                                            <?php if ($u->status == 'Activo'): ?>Suspender<?php else: ?>Re-Activar<?php endif; ?>
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>
</div>


<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
