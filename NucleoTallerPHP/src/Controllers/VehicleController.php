<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;
use PDO;

class VehicleController {
    public function index() {
        $db = Database::getConnection();
        
        $query = "
            SELECT v.*, b.name as brand_name, t.name as type_name 
            FROM vehicles v 
            LEFT JOIN brands b ON v.brand_id = b.id 
            LEFT JOIN vehicle_types t ON v.type_id = t.id 
            ORDER BY v.plate ASC
        ";
        $vehicles = $db->query($query)->fetchAll(PDO::FETCH_OBJ);
        
        foreach ($vehicles as $v) {
            $v->brand = (object)['name' => $v->brand_name ?? 'Genérico'];
            $v->vehicle_type = (object)['name' => $v->type_name ?? 'Vehículo'];
            if ($v->last_service_date) {
                $v->last_service_date = date('d/m/Y', strtotime($v->last_service_date));
            } else {
                $v->last_service_date = 'No registrado';
            }
        }

        $brands = $db->query("SELECT * FROM brands ORDER BY name ASC")->fetchAll(PDO::FETCH_OBJ);
        $types = $db->query("SELECT * FROM vehicle_types ORDER BY name ASC")->fetchAll(PDO::FETCH_OBJ);
        
        $active_page = "vehicles";
        require BASE_PATH . 'src/Views/vehicles.view.php';
    }

    public function history($id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT v.*, b.name as brand_name FROM vehicles v JOIN brands b ON v.brand_id = b.id WHERE v.id = ?");
        $stmt->execute([$id]);
        $vehicle = $stmt->fetch(PDO::FETCH_OBJ);

        if (!$vehicle) { echo "Móvil no encontrado"; return; }

        $stmt = $db->prepare("SELECT * FROM work_orders WHERE vehicle_id = ? ORDER BY entry_date DESC");
        $stmt->execute([$id]);
        $orders = $stmt->fetchAll(PDO::FETCH_OBJ);

        foreach ($orders as $o) {
            $stmt = $db->prepare("SELECT * FROM wo_tasks WHERE work_order_id = ?");
            $stmt->execute([$o->id]);
            $o->tasks = $stmt->fetchAll(PDO::FETCH_OBJ);

            $stmt = $db->prepare("SELECT * FROM wo_parts WHERE work_order_id = ?");
            $stmt->execute([$o->id]);
            $o->parts = $stmt->fetchAll(PDO::FETCH_OBJ);
        }

        require BASE_PATH . 'src/Views/vehicle_history.view.php';
    }

    public function save() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        
        $plate = strtoupper($_POST['plate'] ?? '');
        $brand_id = $_POST['brand_id'] ?? null;
        $type_id = $_POST['type_id'] ?? null;
        $model = $_POST['model'] ?? '';
        $year = $_POST['year'] ?? '';
        $mileage = $_POST['current_mileage'] ?? 0;
        $owner_id = $_POST['owner_id'] ?: null;
        
        try {
            $stmt = $db->prepare("SELECT MAX(internal_code) FROM vehicles");
            $stmt->execute();
            $max = $stmt->fetchColumn();
            $new_code = $max ? (int)$max + 1 : 1001;
            
            $db->prepare("INSERT INTO vehicles (internal_code, plate, brand_id, type_id, model, year, current_mileage, owner_id, photo_url, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '/static/img/default_vehicle.png', NOW())")
               ->execute([$new_code, $plate, $brand_id, $type_id, $model, $year, $mileage, $owner_id]);
               
            echo '<script>window.location.reload();</script>';
        } catch (\PDOException $e) {
            http_response_code(400);
            echo '<div id="notification-area" hx-swap-oob="true" class="bg-red-50 text-red-600 border border-red-200 p-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-2xl">Error: ' . $e->getMessage() . '</div>';
        }
    }
}
