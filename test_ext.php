<?php
echo "MBSTRING: " . (extension_loaded('mbstring') ? 'YES' : 'NO') . "\n";
echo "OPENSSL: " . (extension_loaded('openssl') ? 'YES' : 'NO') . "\n";
echo "PDO: " . (extension_loaded('pdo') ? 'YES' : 'NO') . "\n";
echo "VERSION: " . PHP_VERSION . "\n";
