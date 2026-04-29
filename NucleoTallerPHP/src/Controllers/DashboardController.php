<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;
use PDO;

class DashboardController {
    public function index() {
        // Obtenemos ordenes recientes (simulacion rapida de la logica de main.py)
        $db = Database::getConnection();
        
        $stmt = $db->query("
            SELECT w.*, v.plate, v.brand_id, b.name as brand_name
            FROM work_orders w
            LEFT JOIN vehicles v ON w.vehicle_id = v.id
            LEFT JOIN brands b ON v.brand_id = b.id
            ORDER BY w.entry_date DESC
            LIMIT 50
        ");
        
        $orders = $stmt->fetchAll();
        
        // Calcular costo y duracion para cada orden
        foreach ($orders as &$ot) {
            // Repuestos
            $p_stmt = $db->prepare("SELECT SUM(quantity * unit_price) as total FROM wo_parts WHERE work_order_id = ?");
            $p_stmt->execute([$ot['id']]);
            $parts_total = $p_stmt->fetchColumn() ?: 0;
            
            // Terceros
            $t_stmt = $db->prepare("SELECT SUM(price) as total FROM wo_third_parties WHERE work_order_id = ?");
            $t_stmt->execute([$ot['id']]);
            $third_total = $t_stmt->fetchColumn() ?: 0;
            
            $ot['total_cost'] = $parts_total + $third_total;
            
            // Tareas
            $tk_stmt = $db->prepare("SELECT SUM(duration_minutes) as total FROM wo_tasks WHERE work_order_id = ?");
            $tk_stmt->execute([$ot['id']]);
            $minutes = $tk_stmt->fetchColumn() ?: 0;
            
            $ot['formatted_time'] = $this->format_duration($minutes);
            
            // Simular objeto para la vista
            $ot = (object) $ot;
            $ot->vehicle = (object)['plate' => $ot->plate, 'brand' => (object)['name' => $ot->brand_name]];
        }
        
        $user = isset($_SESSION['user']) ? (object)$_SESSION['user'] : null;
        $active_page = "dashboard";
        
        require BASE_PATH . 'src/Views/index.view.php';
    }
    
    private function format_duration($minutes) {
        if (!$minutes) return "00:00:00";
        $hours = floor($minutes / 60);
        $mins = $minutes % 60;
        return sprintf("00:%02d:%02d", $hours, $mins);
    }
}
