<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;
use PDO;

class OrderController {
    public function new() {
        $db = Database::getConnection();
        $stmt = $db->query("SELECT v.*, b.name as brand_name FROM vehicles v LEFT JOIN brands b ON v.brand_id = b.id ORDER BY v.plate ASC");
        $vehicles = $stmt->fetchAll();
        foreach ($vehicles as &$v) {
            $v = (object)$v;
            $v->brand = (object)['name' => $v->brand_name ?? 'Genérico'];
        }
        require BASE_PATH . 'src/Views/components/new_order_modal.view.php';
    }

    public function save() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        $vehicle_id = $_POST['vehicle_id'] ?? null;
        $diagnosis = $_POST['diagnosis'] ?? '';
        if ($vehicle_id) {
            $stmt = $db->prepare("INSERT INTO work_orders (vehicle_id, diagnosis, entry_date, status) VALUES (?, ?, NOW(), 'Pendiente')");
            $stmt->execute([$vehicle_id, $diagnosis]);
            $order_id = $db->lastInsertId();
            echo '<div class="bg-emerald-50 border border-emerald-200 text-emerald-800 p-8 rounded-2xl">
                    <h3 class="font-black text-xl mb-2">✓ Orden #' . $order_id . ' Abierta</h3>
                    <p>La unidad ha sido ingresada correctamente al sistema.</p>
                    <button class="btn-primary mt-6" onclick="window.location.reload()">VOLVER AL PANEL</button>
                  </div>';
        }
    }

    private function ensureInExecution(int $id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT status FROM work_orders WHERE id = ?");
        $stmt->execute([$id]);
        $status = $stmt->fetchColumn();
        if ($status === 'Pendiente') {
            $stmt = $db->prepare("UPDATE work_orders SET status = 'En Ejecución', updated_at = NOW() WHERE id = ?");
            $stmt->execute([$id]);
        }
    }

    private function isOrderLocked(int $id): bool {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT status FROM work_orders WHERE id = ?");
        $stmt->execute([$id]);
        $status = $stmt->fetchColumn();
        return ($status === 'Terminada' || $status === 'Anulada');
    }

    public function show($id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("
            SELECT o.*, v.plate, v.model, v.internal_code, b.name as brand_name 
            FROM work_orders o 
            JOIN vehicles v ON o.vehicle_id = v.id 
            LEFT JOIN brands b ON v.brand_id = b.id 
            WHERE o.id = ?
        ");
        $stmt->execute([$id]);
        $order_data = $stmt->fetch();

        if (!$order_data) {
            echo "Orden no encontrada";
            return;
        }

        $order = (object)$order_data;
        $order->vehicle = (object)[
            'plate' => $order_data['plate'],
            'model' => $order_data['model'],
            'internal_code' => $order_data['internal_code'],
            'brand' => (object)['name' => $order_data['brand_name'] ?? 'Genérico']
        ];
        $order->entry_date = new \DateTime($order->entry_date);

        // Fetch Tasks
        $stmt = $db->prepare("SELECT t.*, tech.name as technician_name FROM wo_tasks t JOIN technicians tech ON t.technician_id = tech.id WHERE t.work_order_id = ?");
        $stmt->execute([$id]);
        $order->tasks = $stmt->fetchAll(PDO::FETCH_OBJ);

        // Fetch Parts
        $stmt = $db->prepare("SELECT * FROM wo_parts WHERE work_order_id = ?");
        $stmt->execute([$id]);
        $order->parts = $stmt->fetchAll(PDO::FETCH_OBJ);

        // Fetch Third Parties
        $stmt = $db->prepare("SELECT * FROM wo_third_parties WHERE work_order_id = ?");
        $stmt->execute([$id]);
        $order->third_parties = $stmt->fetchAll(PDO::FETCH_OBJ);

        // Fetch Technicians
        $stmt = $db->query("SELECT id, name FROM technicians ORDER BY name ASC");
        $technicians = $stmt->fetchAll(PDO::FETCH_OBJ);

        require BASE_PATH . 'src/Views/order_detail.view.php';
    }

    public function addTask($id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST' || $this->isOrderLocked((int)$id)) return;
        $db = Database::getConnection();
        $desc = $_POST['description'] ?? '';
        $dur = $_POST['duration'] ?? 0;
        $tech_id = $_POST['tech_id'] ?? null;
        $stmt = $db->prepare("INSERT INTO wo_tasks (work_order_id, description, duration_minutes, technician_id) VALUES (?, ?, ?, ?)");
        $stmt->execute([$id, $desc, $dur, $tech_id]);
        $this->ensureInExecution((int)$id);
        $this->loadTasks((int)$id);
    }

    private function loadTasks(int $id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT t.*, tech.name as technician_name FROM wo_tasks t JOIN technicians tech ON t.technician_id = tech.id WHERE t.work_order_id = ?");
        $stmt->execute([$id]);
        $tasks = $stmt->fetchAll(PDO::FETCH_OBJ);
        $is_closed = $this->isOrderLocked($id);
        require BASE_PATH . 'src/Views/components/task_list.view.php';
    }

    public function addPart($id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST' || $this->isOrderLocked((int)$id)) return;
        $db = Database::getConnection();
        $desc = $_POST['description'] ?? '';
        $qty = $_POST['qty'] ?? 0;
        $price = $_POST['price'] ?? 0;
        $uom = $_POST['uom'] ?? 'Un';
        $stmt = $db->prepare("INSERT INTO wo_parts (work_order_id, description, quantity, unit_price, uom) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$id, $desc, $qty, $price, $uom]);
        $this->ensureInExecution((int)$id);
        header('HX-Trigger: refreshSummary');
        $this->loadParts((int)$id);
    }

    private function loadParts(int $id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT * FROM wo_parts WHERE work_order_id = ?");
        $stmt->execute([$id]);
        $parts = $stmt->fetchAll(PDO::FETCH_OBJ);
        $is_closed = $this->isOrderLocked($id);
        require BASE_PATH . 'src/Views/components/part_list.view.php';
    }

    public function addThirdParty($id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST' || $this->isOrderLocked((int)$id)) return;
        $db = Database::getConnection();
        $provider = $_POST['provider'] ?? '';
        $desc = $_POST['description'] ?? '';
        $price = $_POST['price'] ?? 0;
        $stmt = $db->prepare("INSERT INTO wo_third_parties (work_order_id, provider_name, description, price) VALUES (?, ?, ?, ?)");
        $stmt->execute([$id, $provider, $desc, $price]);
        $this->ensureInExecution((int)$id);
        header('HX-Trigger: refreshSummary');
        $this->loadThirdParties((int)$id);
    }

    private function loadThirdParties(int $id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT * FROM wo_third_parties WHERE work_order_id = ?");
        $stmt->execute([$id]);
        $third_parties = $stmt->fetchAll(PDO::FETCH_OBJ);
        $is_closed = $this->isOrderLocked($id);
        require BASE_PATH . 'src/Views/components/third_party_list.view.php';
    }

    public function header($id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT status FROM work_orders WHERE id = ?");
        $stmt->execute([$id]);
        $status = $stmt->fetchColumn();
        echo '<div class="card-premium p-8 bg-slate-900 text-white flex justify-between items-center animate-in slide-in-from-top-4">
                <div>
                    <h1 class="text-3xl font-black">Orden de Trabajo #'.$id.'</h1>
                    <p class="text-sky-400 font-bold uppercase text-[10px] tracking-widest mt-1">Detalle Operativo y Seguimiento</p>
                </div>
                <div class="flex items-center gap-3 bg-white/10 px-6 py-3 rounded-2xl border border-white/5">
                    <span class="text-[9px] font-black uppercase tracking-widest text-slate-400">Estado:</span>
                    <span class="text-xs font-black uppercase tracking-widest text-white">'.$status.'</span>
                </div>
              </div>';
    }

    public function summary($id) {
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT SUM(quantity * unit_price) as total FROM wo_parts WHERE work_order_id = ?");
        $stmt->execute([$id]);
        $parts_total = $stmt->fetch()['total'] ?? 0;

        $stmt = $db->prepare("SELECT SUM(price) as total FROM wo_third_parties WHERE work_order_id = ?");
        $stmt->execute([$id]);
        $third_total = $stmt->fetch()['total'] ?? 0;

        $total = (float)$parts_total + (float)$third_total;

        echo '<div class="card-premium p-8 bg-white border-slate-100 animate-in fade-in zoom-in duration-300">
                <h3 class="text-xs font-black text-slate-400 uppercase tracking-widest mb-4">Resumen de Inversión</h3>
                <div class="text-4xl font-black text-slate-800">$'.number_format((float)$total, 2).'</div>
              </div>';
    }

    public function status($id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        $status = $_POST['status'] ?? 'Pendiente';
        $stmt = $db->prepare("UPDATE work_orders SET status = ?, updated_at = NOW() WHERE id = ?");
        $stmt->execute([$status, $id]);
        header('HX-Refresh: true'); // Refresh entire page on status change to lock components
    }

    public function delete($id) {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') return;
        $db = Database::getConnection();
        $stmt = $db->prepare("SELECT status FROM work_orders WHERE id = ?");
        $stmt->execute([$id]);
        $status = $stmt->fetchColumn();

        if ($status !== 'Pendiente') {
            http_response_code(400);
            echo "Solo se pueden borrar órdenes en estado PENDIENTE";
            return;
        }

        // Borrado en cascada manual (si no hay FK CASCADE)
        $db->prepare("DELETE FROM wo_tasks WHERE work_order_id = ?")->execute([$id]);
        $db->prepare("DELETE FROM wo_parts WHERE work_order_id = ?")->execute([$id]);
        $db->prepare("DELETE FROM wo_third_parties WHERE work_order_id = ?")->execute([$id]);
        $db->prepare("DELETE FROM work_orders WHERE id = ?")->execute([$id]);

        header('Location: /');
    }
}
