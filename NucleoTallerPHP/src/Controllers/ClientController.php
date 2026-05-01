<?php
declare(strict_types=1);

namespace Controllers;

use Config\Database;
use PDO;

class ClientController {
    public function index() {
        $db = Database::getConnection();
        
        $query = "
            SELECT o.*, c.name as country_name, p.name as province_name 
            FROM owners o 
            LEFT JOIN countries c ON o.country_id = c.id 
            LEFT JOIN provinces p ON o.province_id = p.id 
            ORDER BY o.owner_number DESC
        ";
        $clients = $db->query($query)->fetchAll(PDO::FETCH_OBJ);
        
        foreach ($clients as $client) {
            $client->country = (object)['name' => $client->country_name ?? 'Argentina'];
            $client->province = (object)['name' => $client->province_name ?? 'S/D'];
        }

        $countries = $db->query("SELECT * FROM countries ORDER BY name ASC")->fetchAll(PDO::FETCH_OBJ);
        $provinces = $db->query("SELECT * FROM provinces ORDER BY name ASC")->fetchAll(PDO::FETCH_OBJ);
        
        $active_page = "clients";
        require BASE_PATH . 'src/Views/clients.view.php';
    }
}
