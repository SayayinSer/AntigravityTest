<?php
declare(strict_types=1);

session_start();

// Definir constante base
define('BASE_PATH', __DIR__ . '/../');

// Cargar Router básico o manejar la lógica aquí
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'];

// Para pruebas locales, detectamos si estamos en el root o en un subdirectorio
$base_url = (strpos($_SERVER['SCRIPT_NAME'], 'index.php') !== false) ? str_replace('/index.php', '', $_SERVER['SCRIPT_NAME']) : '';
$route = ($base_url) ? str_replace($base_url, '', $request_uri) : $request_uri;
if ($route === '' || $route === false) $route = '/';

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
        case (preg_match('/^\/vehicles\/(\d+)\/history$/', $route, $matches) ? true : false):
            $controller = new \Controllers\VehicleController();
            $controller->history($matches[1]);
            break;
        case '/clients':
            $controller = new \Controllers\ClientController();
            $controller->index();
            break;
        case '/appointments':
            $controller = new \Controllers\AppointmentController();
            $controller->index();
            break;
        case '/appointments/save':
            $controller = new \Controllers\AppointmentController();
            $controller->save();
            break;
        case '/appointments/report':
            $controller = new \Controllers\AppointmentController();
            $controller->report();
            break;
        case '/appointments/api/check-client':
            $controller = new \Controllers\AppointmentController();
            $controller->checkClient();
            break;
        case '/reports':
            $controller = new \Controllers\ReportController();
            $controller->index();
            break;
        case '/reports/generate':
            $controller = new \Controllers\ReportController();
            $controller->generate();
            break;
        case '/order/new':
            $controller = new \Controllers\OrderController();
            $controller->new();
            break;
        case '/order/save':
            $controller = new \Controllers\OrderController();
            $controller->save();
            break;
        case (preg_match('/^\/order\/(\d+)\/status$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->status($matches[1]);
            break;
        case (preg_match('/^\/order\/(\d+)\/task$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->addTask($matches[1]);
            break;
        case (preg_match('/^\/order\/(\d+)\/part$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->addPart($matches[1]);
            break;
        case (preg_match('/^\/order\/(\d+)\/third-party$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->addThirdParty($matches[1]);
            break;
        case (preg_match('/^\/order\/(\d+)\/header$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->header($matches[1]);
            break;
        case (preg_match('/^\/order\/(\d+)\/summary$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->summary($matches[1]);
            break;
        case (preg_match('/^\/order\/(\d+)$/', $route, $matches) ? true : false):
            $controller = new \Controllers\OrderController();
            $controller->show($matches[1]);
            break;
        case '/api/test-db':
            require BASE_PATH . 'src/Config/Database.php';
            $db = \Config\Database::getConnection();
            echo json_encode(['status' => 'success', 'message' => 'Conexión exitosa a la DB']);
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
