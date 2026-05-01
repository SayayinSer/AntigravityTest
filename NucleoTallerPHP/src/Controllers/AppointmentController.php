<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;
use PDO;

class AppointmentController {
    public function index() {
        $db = Database::getConnection();
        $today = date('Y-m-d');
        
        $stmt = $db->prepare("SELECT * FROM appointments WHERE scheduled_date::date = ? ORDER BY scheduled_date ASC");
        $stmt->execute([$today]);
        $appointments = $stmt->fetchAll(PDO::FETCH_OBJ);
        
        foreach ($appointments as $app) {
            $dt = new \DateTime($app->scheduled_date);
            $app->scheduled_time = $dt->format('H:i');
            $app->scheduled_date_fmt = $dt->format('d/m/Y');
        }

        $vehicles_query = "
            SELECT v.id, v.plate, b.name as brand_name 
            FROM vehicles v 
            LEFT JOIN brands b ON v.brand_id = b.id 
            ORDER BY v.plate ASC
        ";
        $vehicles = $db->query($vehicles_query)->fetchAll(PDO::FETCH_OBJ);
        foreach ($vehicles as $v) {
            $v->brand = (object)['name' => $v->brand_name ?? 'Genérico'];
        }
        $today_date = $today;

        require BASE_PATH . 'src/Views/appointments.view.php';
    }

    public function save() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        
        $email = $_POST['client_email'] ?? '';
        $name = $_POST['client_name'] ?? '';
        $phone = $_POST['client_phone'] ?? '';
        $date = $_POST['scheduled_date'] ?? '';
        $time = $_POST['scheduled_time'] ?? '';
        $vehicle_id = $_POST['vehicle_id'] ?: null;
        $plate = $_POST['plate'] ?? '';
        $reason = $_POST['reason'] ?? '';
        
        $full_datetime = $date . ' ' . $time;

        // Alta oculta de cliente si no existe
        $stmt_check = $db->prepare("SELECT id FROM owners WHERE email = ?");
        $stmt_check->execute([$email]);
        $owner_id = $stmt_check->fetchColumn();

        if (!$owner_id && $email) {
            $stmt_max = $db->query("SELECT MAX(owner_number) FROM owners");
            $max_num = $stmt_max->fetchColumn();
            $new_num = $max_num ? (int)$max_num + 1 : 10001;

            $stmt_owner = $db->prepare("INSERT INTO owners (owner_number, full_name, email, phone, owner_type, created_at) VALUES (?, ?, ?, ?, 'Persona Física', NOW())");
            $stmt_owner->execute([$new_num, $name, $email, $phone]);
            $owner_id = $db->lastInsertId();
        }

        $stmt = $db->prepare("INSERT INTO appointments (client_email, client_name, client_phone, scheduled_date, vehicle_id, plate, reason, status, owner_id) VALUES (?, ?, ?, ?, ?, ?, ?, 'Confirmado', ?)");
        $stmt->execute([$email, $name, $phone, $full_datetime, $vehicle_id, $plate, $reason, $owner_id]);

        // Link vehicle to owner if not already linked
        if ($vehicle_id && $owner_id) {
            $db->prepare("UPDATE vehicles SET owner_id = ? WHERE id = ? AND owner_id IS NULL")->execute([$owner_id, $vehicle_id]);
        }

        echo '<div class="bg-indigo-50 p-8 rounded-2xl text-center">
                <h3 class="text-xl font-black text-indigo-800 mb-2">✓ Turno Confirmado</h3>
                <p class="text-indigo-600 mb-6">El turno ha sido programado exitosamente' . (!$stmt_check->fetchColumn() ? ' y el cliente fue enrolado' : '') . '.</p>
                <button class="btn-primary bg-indigo-600" onclick="window.location.reload()">ENTENDIDO</button>
              </div>';
    }

    public function report() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        $start = $_POST['start_date'] ?? '';
        $end = $_POST['end_date'] ?? '';

        $stmt = $db->prepare("SELECT * FROM appointments WHERE scheduled_date::date BETWEEN ? AND ? ORDER BY scheduled_date ASC");
        $stmt->execute([$start, $end]);
        $results = $stmt->fetchAll(PDO::FETCH_OBJ);

        require BASE_PATH . 'src/Views/components/appointment_report_results.view.php';
    }
    public function checkClient() {
        $email = $_GET['client_email'] ?? '';
        if (!$email) {
            echo json_encode(['found' => false]);
            return;
        }

        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT id, full_name, phone FROM owners WHERE email = ?");
        $stmt->execute([$email]);
        $owner = $stmt->fetch(PDO::FETCH_OBJ);

        if ($owner) {
            // Buscar vehículos asociados por owner_id O por historial de turnos
            $stmt_v = $db->prepare("
                SELECT DISTINCT v.id, v.plate, b.name as brand_name 
                FROM vehicles v
                LEFT JOIN brands b ON v.brand_id = b.id
                LEFT JOIN appointments a ON a.vehicle_id = v.id
                WHERE v.owner_id = ? OR a.owner_id = ?
                ORDER BY v.plate ASC
            ");
            $stmt_v->execute([$owner->id, $owner->id]);
            $vehicles = $stmt_v->fetchAll(PDO::FETCH_OBJ);

            echo json_encode([
                'found' => true,
                'name' => $owner->full_name,
                'phone' => $owner->phone,
                'vehicles' => $vehicles
            ]);
        } else {
            echo json_encode(['found' => false]);
        }
    }
}
