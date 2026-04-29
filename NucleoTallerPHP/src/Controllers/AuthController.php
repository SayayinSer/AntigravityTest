<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;

class AuthController {
    public function login() {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $username = $_POST['username'] ?? '';
            $password = $_POST['password'] ?? '';
            
            $db = Database::getConnection();
            $stmt = $db->prepare("SELECT * FROM users WHERE username = ?");
            $stmt->execute([$username]);
            $user = $stmt->fetch();
            
            if (!$user) {
                http_response_code(401);
                echo '<div id="error-msg" class="text-red-500 font-black text-[10px] uppercase tracking-widest bg-red-50 p-4 rounded-2xl border border-red-100 mb-6 shadow-sm">Usuario no registrado</div>';
                return;
            }
            
            if ($user['status'] === 'Suspendido') {
                http_response_code(403);
                echo '<div id="error-msg" class="text-white font-black text-[10px] uppercase tracking-[0.2em] bg-red-600 p-4 rounded-2xl border border-red-700 mb-6 shadow-xl shadow-red-900/20">CUENTA SUSPENDIDA. Contacte soporte.</div>';
                return;
            }
            
            if (!password_verify($password, $user['hashed_password'])) {
                // Incrementar failed_attempts
                $attempts = $user['failed_attempts'] + 1;
                $status = $attempts >= 3 ? 'Suspendido' : 'Activo';
                $db->prepare("UPDATE users SET failed_attempts = ?, status = ? WHERE id = ?")->execute([$attempts, $status, $user['id']]);
                
                $msg = "Clave incorrecta. Intentos: $attempts/3";
                if ($status === 'Suspendido') {
                    $msg = "CUENTA SUSPENDIDA POR INTENTOS FALLIDOS.";
                }
                http_response_code(401);
                echo '<div id="error-msg" class="text-red-500 font-black text-[10px] uppercase tracking-widest bg-red-50 p-4 rounded-2xl border border-red-100 mb-6 shadow-sm">' . $msg . '</div>';
                return;
            }
            
            // Exito
            $db->prepare("UPDATE users SET failed_attempts = 0 WHERE id = ?")->execute([$user['id']]);
            $_SESSION['user'] = $user;
            
            // Audit log
            $db->prepare("INSERT INTO audit_logs (user_id, action, entity_name, entity_id, details) VALUES (?, 'LOGIN', 'Usuario', ?, 'Inicio de sesión exitoso')")
               ->execute([$user['id'], $user['id']]);
               
            // Redireccion HTMX
            header("HX-Redirect: /NucleoTallerPHP/public/");
            http_response_code(204);
            return;
        }
        
        require BASE_PATH . 'src/Views/login.view.php';
    }
    
    public function logout() {
        session_destroy();
        header("Location: /NucleoTallerPHP/public/login");
        exit;
    }
}
