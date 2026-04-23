<?php
try {
    $pdo = new PDO("mysql:host=127.0.0.1;port=3306", "root", "root");
    echo "Root success\n";
} catch (Exception $e) {
    echo "Root fail: " . $e->getMessage() . "\n";
}

try {
    $pdo = new PDO("mysql:host=127.0.0.1;port=3306", "db", "db");
    echo "DB success\n";
} catch (Exception $e) {
    echo "DB fail: " . $e->getMessage() . "\n";
}
