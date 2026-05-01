<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aliso - Gestión Profesional</title>
    
    <!-- Scripts Base -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Diseño Sistema (Tailwind Config / Estilos Globales) -->
    <style type="text/tailwindcss">
        [x-cloak] { display: none !important; }
        
        /* Definición de la Paleta Monocromática Profesional */
        :root {
            --brand-primary: #0ea5e9; /* Sky 500 */
            --brand-dark: #0f172a;    /* Slate 900 */
            --brand-slate: #64748b;   /* Slate 500 */
        }

        .glass { 
            background: rgba(255, 255, 255, 0.85); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255, 255, 255, 0.4); 
        }

        /* Botones Unificados */
        .btn-primary {
            @apply bg-slate-900 text-white px-6 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:bg-sky-600 active:scale-95 flex items-center gap-2;
        }
        
        .btn-secondary {
            @apply bg-white text-slate-700 border border-slate-200 px-6 py-2.5 rounded-xl font-bold transition-all hover:bg-slate-50 active:scale-95 flex items-center gap-2;
        }

        .btn-success {
            @apply bg-emerald-600 text-white px-6 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:bg-emerald-700 active:scale-95 flex items-center gap-2;
        }

        .btn-warning {
            @apply bg-amber-500 text-white px-6 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:bg-amber-600 active:scale-95 flex items-center gap-2;
        }

        .btn-danger {
            @apply bg-red-50 text-red-600 border border-red-100 px-4 py-2 rounded-xl font-bold transition-all hover:bg-red-100 flex items-center gap-2;
        }

        /* Cards Unificadas */
        .card-premium {
            @apply glass p-8 rounded-[2rem] shadow-xl border-white/50;
        }

        /* Inputs Unificados */
        .input-premium {
            @apply w-full $p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-all;
        }

        .label-premium {
            @apply block text-[10px] font-black text-slate-400 uppercase tracking-[0.15em] mb-1.5 ml-1;
        }

        /* Scrollbar Personalizada */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* HTMX Indicator */
        .htmx-indicator { opacity: 0; transition: opacity 200ms ease-in; pointer-events: none; }
        .htmx-request .htmx-indicator { opacity: 1; }
        .htmx-request.htmx-indicator { opacity: 1; }
    </style>
    
    
</head>
<body class="bg-slate-50 min-h-screen text-slate-800 font-sans flex flex-col">

    <!-- Navbar Unificada -->
    <nav class="bg-slate-900 text-white p-4 shadow-2xl sticky top-0 z-[100]">
        <div class="container mx-auto flex flex-col lg:flex-row justify-between items-center gap-4">
            <!-- Logo ALISO -->
            <a href="/" class="flex items-center gap-3 group">
                <div class="bg-white $p-1.5 rounded-xl shadow-inner group-hover:scale-105 transition-transform">
                    <img src="/static/img/logo_aliso.png" alt="ALISO" class="h-8 w-auto">
                </div>
                <div class="flex flex-col">
                    <span class="text-xl font-black tracking-tighter leading-none">ALISO</span>
                    <span class="text-[9px] font-bold text-sky-400 tracking-[0.2em] uppercase">Workflow Engine</span>
                </div>
            </a>

            <!-- Navegación -->
            <div class="flex flex-wrap items-center justify-center gap-2">
                <a href="/appointments" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?php if ($active_page == 'appointments'): ?>bg-sky-500 text-white<?php else: ?>hover:bg-white/10 text-slate-300<?php endif; ?> flex items-center gap-2">
                    <span class="text-lg">ðŸ“†</span> AGENDA
                </a>
                <a href="/clients" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?php if ($active_page == '$clients'): ?>bg-sky-500 text-white<?php else: ?>hover:bg-white/10 text-slate-300<?php endif; ?> flex items-center gap-2">
                    <span class="text-lg">ðŸ‘¥</span> CLIENTES
                </a>
                <a href="/vehicles" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?php if ($active_page == '$vehicles'): ?>bg-sky-500 text-white<?php else: ?>hover:bg-white/10 text-slate-300<?php endif; ?> flex items-center gap-2">
                    <span class="text-lg">ðŸš—</span> MÓVILES
                </a>
                <a href="/reports" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?php if ($active_page == 'reports'): ?>bg-sky-500 text-white<?php else: ?>hover:bg-white/10 text-slate-300<?php endif; ?> flex items-center gap-2">
                    <span class="text-lg">ðŸ“Š</span> REPORTES
                </a>
                <a href="/admin" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?php if ($active_page == 'admin'): ?>bg-sky-500 text-white<?php else: ?>hover:bg-white/10 text-slate-300<?php endif; ?> flex items-center gap-2 text-slate-400">
                    <span class="text-lg">ðŸ› ï¸</span> TABLAS
                </a>

                <?php if (in_array('OficialSeguridad', $user->roles ?? [])): ?>
                <a href="/admin/security" class="px-4 py-2 rounded-xl text-xs font-black shadow-lg transition-all flex items-center gap-2 <?php if ($active_page == 'security'): ?>bg-amber-500 text-amber-950 scale-105 ring-2 ring-amber-300<?php else: ?>bg-amber-600/20 text-amber-500 hover:bg-amber-500 hover:text-amber-950<?php endif; ?>">
                    ðŸ”’ SEGURIDAD
                </a>
                <?php endif; ?>

                <div class="w-px h-6 bg-white/20 mx-2 hidden lg:block"></div>

                <!-- Perfil / Salir -->
                <?php if ($user): ?>
                <div class="flex items-center gap-3 bg-white/5 pl-2 pr-4 py-1 rounded-full border border-white/10">
                    <div class="w-8 h-8 bg-sky-500 text-white rounded-full flex items-center justify-center text-xs font-black shadow-lg"><?= htmlspecialchars(strval($user->username[0] ?? "")) ?></div>
                    <div class="flex flex-col">
                        <span class="text-[9px] font-black uppercase tracking-wider text-slate-400">Operador</span>
                        <span class="text-[11px] font-bold"><?= htmlspecialchars(strval($user->username ?? "")) ?></span>
                    </div>
                    <a href="/logout" class="ml-2 text-slate-400 hover:text-red-400 transition-colors" title="Cerrar Sesión">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                    </a>
                </div>
                <?php endif; ?>
            </div>
        </div>
    </nav>

    <!-- Notificaciones Globales -->
    <div id="notification-area" class="fixed top-20 right-4 z-[200]"></div>

    <!-- Contenido Principal -->
    <main class="container mx-auto py-8 px-4 flex-grow">
        
    </main>

    <!-- Footer Unificado -->
    <footer class="py-12 border-t border-slate-200 bg-white">
        <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-3 opacity-50">
                <img src="/static/img/logo_aliso.png" alt="ALISO" class="h-6 grayscale">
                <span class="text-[10px] font-bold tracking-[0.3em] uppercase">Aliso Workflow Engine</span>
            </div>
            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
                &copy; 2026 Aliso System &bull; Argentina &bull; Gestión Inteligente de Operaciones
            </div>
            <div class="flex gap-4">
                <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse" title="Sistema Online"></div>
            </div>
        </div>
    </footer>

    

</body>
</html>

<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
