<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;

class ReportController {
    public function index() {
        $db = Database::getConnection();
        
        $user = isset($_SESSION['user']) ? (object)$_SESSION['user'] : null;
        $active_page = "reports";
        
        $technicians = $db->query("SELECT * FROM technicians")->fetchAll();
        foreach ($technicians as &$t) { $t = (object)$t; }
        
        require BASE_PATH . 'src/Views/reports.view.php';
    }
}
