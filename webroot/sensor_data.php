<?php
// use this permissions command if issues with "bus not detected" from this php page: sudo usermod -aG i2c www-data

// Set JSON response type
header('Content-Type: application/json');

// Execute Python script
$pythonScript = escapeshellcmd('python3 /var/www/html/tempsensor.py');
$output = shell_exec($pythonScript);

// Trim extra characters (removes unexpected shell output)
$output = trim($output);

// Decode JSON
$data = json_decode($output, true);

// Handle errors
if ($data === null) {
    echo json_encode(["error" => "Failed to get sensor data. Raw output: $output"]);
} else {
    echo json_encode($data);
}
?
