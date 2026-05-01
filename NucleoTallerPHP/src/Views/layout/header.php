<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? 'Aliso - Gestión Profesional' ?></title>
    
    <!-- Scripts Base -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <style type="text/tailwindcss">
        [x-cloak] { display: none !important; }
        :root {
            --brand-primary: #0ea5e9;
            --brand-dark: #0f172a;
            --brand-slate: #64748b;
        }
        .glass { 
            background: rgba(255, 255, 255, 0.85); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255, 255, 255, 0.4); 
        }
        .btn-primary { @apply bg-slate-900 text-white px-6 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:bg-sky-600 active:scale-95 flex items-center gap-2; }
        .btn-secondary { @apply bg-white text-slate-700 border border-slate-200 px-6 py-2.5 rounded-xl font-bold transition-all hover:bg-slate-50 active:scale-95 flex items-center gap-2; }
        .card-premium { @apply glass p-8 rounded-[2rem] shadow-xl border-white/50; }
        .input-premium { @apply w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-all; }
        .label-premium { @apply block text-[10px] font-black text-slate-400 uppercase tracking-[0.15em] mb-1.5 ml-1; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen text-slate-800 font-sans flex flex-col">
    <nav class="bg-slate-900 text-white p-4 shadow-2xl sticky top-0 z-[100]">
        <div class="container mx-auto flex flex-col lg:flex-row justify-between items-center gap-4">
            <a href="/" class="flex items-center gap-3 group">
                <div class="bg-white p-1.5 rounded-xl shadow-inner group-hover:scale-105 transition-transform">
                    <img src="/static/img/logo_aliso.png" alt="ALISO" class="h-8 w-auto">
                </div>
                <div class="flex flex-col">
                    <span class="text-xl font-black tracking-tighter leading-none">ALISO</span>
                    <span class="text-[9px] font-bold text-sky-400 tracking-[0.2em] uppercase">Workflow Engine</span>
                </div>
            </a>
            <div class="flex flex-wrap items-center justify-center gap-2">
                <a href="/appointments" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?= ($active_page ?? '') == 'appointments' ? 'bg-sky-500 text-white' : 'hover:bg-white/10 text-slate-300' ?>">📆 AGENDA</a>
                <a href="/clients" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?= ($active_page ?? '') == 'clients' ? 'bg-sky-500 text-white' : 'hover:bg-white/10 text-slate-300' ?>">👥 CLIENTES</a>
                <a href="/vehicles" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?= ($active_page ?? '') == 'vehicles' ? 'bg-sky-500 text-white' : 'hover:bg-white/10 text-slate-300' ?>">🚗 MÓVILES</a>
                <a href="/reports" class="px-4 py-2 rounded-xl text-xs font-bold transition-all <?= ($active_page ?? '') == 'reports' ? 'bg-sky-500 text-white' : 'hover:bg-white/10 text-slate-300' ?>">📊 REPORTES</a>
                
                <?php if (isset($user)): ?>
                <div class="flex items-center gap-3 bg-white/5 pl-2 pr-4 py-1 rounded-full border border-white/10 ml-4">
                    <div class="w-8 h-8 bg-sky-500 text-white rounded-full flex items-center justify-center text-xs font-black"><?= strtoupper($user->username[0]) ?></div>
                    <span class="text-[11px] font-bold"><?= $user->username ?></span>
                    <a href="/logout" class="ml-2 text-slate-400 hover:text-red-400">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                    </a>
                </div>
                <?php endif; ?>
            </div>
        </div>
    </nav>
    <main class="container mx-auto py-8 px-4 flex-grow">
