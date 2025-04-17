<?php

header('Content-Type: application/json');

$pythonScript = escapeshellcmd('python3 /var/www/html/tempsensor.py');
$output = shell_exec($pythonScript);
$output = trim($output);

$data = json_decode($output, true);

if ($data === null) {
    echo json_encode(["error" => "Failed to get sensor data. Raw output: $output"]);
} else {
    echo json_encode($data);
}
?>
