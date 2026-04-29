<?php
declare(strict_types=1);

session_start();

// Definir constante base
define('BASE_PATH', __DIR__ . '/../');

// Cargar Router básico o manejar la lógica aquí
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'];

// Para pruebas locales, si ejecutamos en un subdirectorio, ajustamos:
$base_url = '/NucleoTallerPHP/public';
$route = str_replace($base_url, '', $request_uri);
if ($route === '') $route = '/';

try {
    // Autoload simplificado para Controllers
    spl_autoload_register(function ($class) {
        $file = BASE_PATH . 'src/' . str_replace('\\', '/', $class) . '.php';
        if (file_exists($file)) require $file;
    });

    // Router simple
    switch ($route) {
        case '/':
            $controller = new \Controllers\DashboardController();
            $controller->index();
            break;
        case '/login':
            $controller = new \Controllers\AuthController();
            $controller->login();
            break;
        case '/logout':
            $controller = new \Controllers\AuthController();
            $controller->logout();
            break;
        case '/vehicles':
            $controller = new \Controllers\VehicleController();
            $controller->index();
            break;
        case '/vehicles/save':
            $controller = new \Controllers\VehicleController();
            $controller->save();
            break;
        case '/clients':
            $controller = new \Controllers\ClientController();
            $controller->index();
            break;
        case '/appointments':
            $controller = new \Controllers\AppointmentController();
            $controller->index();
            break;
        case '/reports':
            $controller = new \Controllers\ReportController();
            $controller->index();
            break;
        case '/api/test-db':
            require BASE_PATH . 'src/Config/Database.php';
            $db = \Config\Database::getConnection();
            echo json_encode(['status' => 'success', 'message' => 'Conexión exitosa a MySQL']);
            break;
        default:
            http_response_code(404);
            echo "404 - Not Found";
            break;
    }
} catch (Throwable $e) {
    http_response_code(500);
    echo '<div style="color:red; font-family:sans-serif; padding:20px;">';
    echo '<h2>Error Interno Detectado</h2>';
    echo '<p>' . htmlspecialchars($e->getMessage()) . '</p>';
    echo '</div>';
}
