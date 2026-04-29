<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;

class ClientController {
    public function index() {
        $db = Database::getConnection();
        $clients = $db->query("SELECT * FROM owners ORDER BY owner_number DESC")->fetchAll();
        $countries = $db->query("SELECT * FROM countries")->fetchAll();
        $provinces = $db->query("SELECT * FROM provinces")->fetchAll();
        
        foreach ($clients as &$c) { $c = (object)$c; }
        foreach ($countries as &$c) { $c = (object)$c; }
        foreach ($provinces as &$p) { $p = (object)$p; }
        
        $user = isset($_SESSION['user']) ? (object)$_SESSION['user'] : null;
        $active_page = "clients";
        
        require BASE_PATH . 'src/Views/clients.view.php';
    }
}
