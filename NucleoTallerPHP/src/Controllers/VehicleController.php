<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;

class VehicleController {
    public function index() {
        $db = Database::getConnection();
        $vehicles = $db->query("SELECT * FROM vehicles")->fetchAll();
        $brands = $db->query("SELECT * FROM brands")->fetchAll();
        $types = $db->query("SELECT * FROM vehicle_types")->fetchAll();
        
        // Simular objetos
        foreach ($vehicles as &$v) { $v = (object)$v; }
        foreach ($brands as &$b) { $b = (object)$b; }
        foreach ($types as &$t) { $t = (object)$t; }
        
        $user = isset($_SESSION['user']) ? (object)$_SESSION['user'] : null;
        $active_page = "vehicles";
        
        require BASE_PATH . 'src/Views/vehicles.view.php';
    }

    public function save() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        
        $db = Database::getConnection();
        $plate = strtoupper($_POST['plate'] ?? '');
        $brand_id = $_POST['brand_id'] ?? null;
        $type_id = $_POST['type_id'] ?? null;
        $model = $_POST['model'] ?? null;
        $year = $_POST['year'] ?? null;
        $mileage = $_POST['current_mileage'] ?? 0;
        
        try {
            $stmt = $db->prepare("SELECT MAX(internal_code) FROM vehicles");
            $stmt->execute();
            $max = $stmt->fetchColumn();
            $new_code = $max ? $max + 1 : 1001;
            
            $db->prepare("INSERT INTO vehicles (internal_code, plate, brand_id, type_id, model, year, current_mileage, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, '/static/img/default_vehicle.png')")
               ->execute([$new_code, $plate, $brand_id, $type_id, $model, $year, $mileage]);
               
            echo '<script>window.location.reload();</script>';
        } catch (\PDOException $e) {
            http_response_code(400);
            echo '<div id="notification-area" hx-swap-oob="true" class="bg-red-50 text-red-600 border border-red-200 p-4 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-2xl">Error al guardar vehículo: Puede que la patente ya exista.</div>';
        }
    }
}
