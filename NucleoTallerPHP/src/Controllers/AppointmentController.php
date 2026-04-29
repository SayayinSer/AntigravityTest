<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;

class AppointmentController {
    public function index() {
        $db = Database::getConnection();
        
        $today = date('Y-m-d');
        $today_start = $today . ' 00:00:00';
        $today_end = date('Y-m-d', strtotime('+1 day')) . ' 00:00:00';
        
        $stmt_today = $db->prepare("SELECT * FROM appointments WHERE scheduled_date >= ? AND scheduled_date < ? ORDER BY scheduled_date ASC");
        $stmt_today->execute([$today_start, $today_end]);
        $today_appointments = $stmt_today->fetchAll();
        
        $stmt_upc = $db->prepare("SELECT * FROM appointments WHERE scheduled_date >= ? ORDER BY scheduled_date ASC LIMIT 50");
        $stmt_upc->execute([$today_end]);
        $upcoming_appointments = $stmt_upc->fetchAll();
        
        $vehicles = $db->query("SELECT * FROM vehicles")->fetchAll();
        
        foreach ($today_appointments as &$a) { $a = (object)$a; }
        foreach ($upcoming_appointments as &$a) { $a = (object)$a; }
        foreach ($vehicles as &$v) { $v = (object)$v; }
        
        $user = isset($_SESSION['user']) ? (object)$_SESSION['user'] : null;
        $active_page = "appointments";
        $today_date = $today;
        
        require BASE_PATH . 'src/Views/appointments.view.php';
    }
}
