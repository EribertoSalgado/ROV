<?php
// Handle motor commands
if (isset($_POST['command'])) {
    file_put_contents("/var/www/html/motor_command.txt", $_POST['command']);
}

// Fetch sensor data using Python script
$pythonScript = escapeshellcmd('python3 /var/www/html/tempsensor.py');
$output = shell_exec($pythonScript);
$data = json_decode($output, true);

$temperature = isset($data['temperature']) ? $data['temperature'] : "Error";
$depth = isset($data['depth']) ? $data['depth'] : "Error";
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Title of the tab!-->
    <title>ROV Dashboard</title> 

    <!-- Title -->
    <style> 
        h1 {
            text-align: center;
        }
        body {
            background-color: purple;
        }
    </style>

    <script>
        function takeSnapshot() {
            var img = document.getElementById("snapshot");
            img.src = "http://10.0.0.116:5000/snapshot?" + new Date().getTime();  // Adding timestamp to prevent caching
        }

        function updateSensorData() {
            fetch("sensor_data.php")
                .then(response => response.json())
                .then(data => {
                    document.getElementById("temperature").innerText = data.temperature + " °C";
                    document.getElementById("depth").innerText = data.depth + " m";
                })
                .catch(error => console.error("Error fetching sensor data:", error));
        }

        setInterval(updateSensorData, 5000); // Update every 5 seconds
    </script>
</head>
<body>
    <!-- Title -->
    <h1>ROV Senior Design Spring 2025</h1>

    <!-- Video Feed Section -->
    <h2>ROV Video Stream</h2>
    <iframe src="http://10.0.0.116:5000/video_feed" width="640" height="480" frameborder="0" allowfullscreen></iframe>

    <!-- Snapshot Section -->
    <h2>Snapshot</h2>
    <button onclick="takeSnapshot()">Take Snapshot</button>
    <br>
    <img id="snapshot" src="" alt="Snapshot will appear here" width="640" height="480" />

    <!-- Sensor Data Section -->
    <h2>Sensor Readings</h2>
    <p><strong>Temperature:</strong> <span id="temperature"><?php echo htmlspecialchars($temperature); ?> °C</span></p>
    <p><strong>Depth:</strong> <span id="depth"><?php echo htmlspecialchars($depth); ?> m</span></p>

    <!-- Motor Control Section -->
    <h2>Motor Control Panel</h2>
    <form method="post">
        <button name="command" value="F">Forward</button>
        <button name="command" value="R">Reverse</button>
        <button name="command" value="Q">Stop</button>
    </form>
</body>
</html>
