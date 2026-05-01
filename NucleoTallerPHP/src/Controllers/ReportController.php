<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;
use PDO;

class ReportController {
    public function index() {
        $db = Database::getConnection();
        $technicians = $db->query("SELECT id, name FROM technicians ORDER BY name ASC")->fetchAll(PDO::FETCH_OBJ);
        require BASE_PATH . 'src/Views/reports.view.php';
    }

    public function generate() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        $start = $_POST['start_date'] ?? '';
        $end = $_POST['end_date'] ?? '';
        $tech_id = $_POST['tech_id'] ?? '';
        $status = $_POST['status'] ?? '';

        $query = "
            SELECT o.id, o.entry_date, o.status, v.plate, v.model as vehicle_model,
            (SELECT COALESCE(SUM(quantity * unit_price), 0) FROM wo_parts WHERE work_order_id = o.id) as total_parts_price,
            (SELECT COALESCE(SUM(price), 0) FROM wo_third_parties WHERE work_order_id = o.id) as total_third_party_price,
            (SELECT COALESCE(SUM(duration_minutes), 0) / 60 FROM wo_tasks WHERE work_order_id = o.id) as work_duration
            FROM work_orders o
            JOIN vehicles v ON o.vehicle_id = v.id
            WHERE o.entry_date::date BETWEEN ? AND ?
        ";
        
        $params = [$start, $end];
        
        if ($tech_id) {
            $query .= " AND EXISTS (SELECT 1 FROM wo_tasks WHERE work_order_id = o.id AND technician_id = ?)";
            $params[] = $tech_id;
        }

        if ($status && $status !== 'all') {
            $query .= " AND o.status = ?";
            $params[] = $status;
        }

        $stmt = $db->prepare($query);
        $stmt->execute($params);
        $orders = $stmt->fetchAll(PDO::FETCH_OBJ);

        // Calcular totales para el consolidado
        $parts_total = 0;
        $third_total = 0;
        $parts_count = 0;
        $third_count = 0;

        foreach ($orders as $o) {
            $parts_total += (float)$o->total_parts_price;
            $third_total += (float)$o->total_third_party_price;
            
            // Contar ítems reales
            $stmt_count = $db->prepare("SELECT COUNT(*) FROM wo_parts WHERE work_order_id = ?");
            $stmt_count->execute([$o->id]);
            $parts_count += $stmt_count->fetchColumn();

            $stmt_count = $db->prepare("SELECT COUNT(*) FROM wo_third_parties WHERE work_order_id = ?");
            $stmt_count->execute([$o->id]);
            $third_count += $stmt_count->fetchColumn();
        }

        require BASE_PATH . 'src/Views/components/report_results.view.php';
    }
}
