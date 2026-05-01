<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso - Aliso Workflow</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>
        .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .bg-login { background: radial-gradient(circle at top right, #1e293b 0%, #020617 100%); }
    </style>
</head>
<body class="bg-login min-h-screen text-slate-100 font-sans flex items-center justify-center p-6 selection:bg-sky-500/30">

    <div class="w-full max-w-md animate-in fade-in zoom-in duration-700">
        
        <!-- Logo y Marca -->
        <div class="text-center mb-10">
            <div class="inline-block bg-white $p-3 rounded-3xl shadow-2xl mb-6 ring-4 ring-white/5">
                <img src="/static/img/logo_aliso.png" alt="ALISO" class="h-16 w-auto">
            </div>
            <h1 class="text-4xl font-black tracking-tighter text-white">ALISO <span class="font-normal text-slate-500">WORKFLOW</span></h1>
            <p class="text-slate-400 text-[10px] font-black uppercase tracking-[0.4em] mt-2">Gestión Inteligente de Operaciones</p>
        </div>

        <!-- Tarjeta de Login -->
        <div class="glass p-10 rounded-[2.5rem] shadow-2xl relative overflow-hidden">
            <!-- Sutil brillo decorativo -->
            <div class="absolute -top-10 -right-10 w-24 h-24 bg-sky-500/10 rounded-full blur-3xl"></div>
            
            <div class="relative">
                <h2 class="text-xl font-bold mb-8 flex items-center gap-3">
                    <span class="w-1.5 h-6 bg-sky-500 rounded-full"></span>
                    Iniciar Sesión
                </h2>

                <div id="error-msg" class="transition-all duration-300"></div>

                <form hx-post="/login" hx-target="#error-msg" class="space-y-6">
                    <div>
                        <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Identificador de Usuario</label>
                        <div class="relative">
                            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                            </span>
                            <input type="text" name="username" required placeholder="Ej: jdoe" 
                                   class="w-full bg-white/5 border border-white/10 p-4 pl-12 rounded-2xl outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all placeholder:text-slate-600">
                        </div>
                    </div>

                    <div>
                        <label class="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2 ml-1">Clave de Acceso</label>
                        <div class="relative">
                            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                            </span>
                            <input type="password" name="password" required placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢" 
                                   class="w-full bg-white/5 border border-white/10 p-4 pl-12 rounded-2xl outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all placeholder:text-slate-600">
                        </div>
                    </div>

                    <button type="submit" class="w-full bg-sky-600 hover:bg-sky-500 text-white py-4 rounded-2xl font-black transition-all shadow-xl shadow-sky-900/40 active:scale-[0.98] mt-4 flex items-center justify-center gap-3 group">
                        ENTRAR AL SISTEMA
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                    </button>
                    
                    <div class="text-center pt-4">
                        <a href="/forgot-password" class="text-[10px] font-black text-slate-500 hover:text-sky-400 uppercase tracking-widest transition-colors">¿Olvidó su contraseña?</a>
                    </div>
                </form>
            </div>
        </div>

        <!-- Footer Footer -->
        <div class="mt-10 text-center space-y-4">
            <p class="text-[10px] text-slate-600 font-bold uppercase tracking-[0.2em]">&copy; 2026 Aliso System &bull; Operaciones Estratégicas</p>
            <div class="flex justify-center gap-6 opacity-30 grayscale hover:grayscale-0 transition-all duration-700">
                 <img src="/static/img/logo_aliso.png" alt="Logo" class="h-4">
            </div>
        </div>
    </div>

    <!-- Indicador de Carga HTMX -->
    <div class="htmx-indicator fixed inset-0 z-[200] flex items-center justify-center bg-slate-950/80 backdrop-blur-sm pointer-events-none opacity-0">
        <div class="flex flex-col items-center gap-4">
            <div class="w-12 h-12 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin"></div>
            <p class="text-[10px] font-black uppercase tracking-widest text-sky-500">Autenticando...</p>
        </div>
    </div>
    
    <style>
        .htmx-request.htmx-indicator { opacity: 1; pointer-events: auto; }
    </style>

</body>
</html>

<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>
