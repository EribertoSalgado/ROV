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
$pressure = isset($data['pressure']) ? $data['pressure'] : "Error";

// Get the most recent snapshot
$latestImage = '';
$galleryDir = '/var/www/html/Gallery';
$images = glob($galleryDir . "/*.jpg");

if (!empty($images)) {
    rsort($images); // Sort by newest first
    $latestImage = basename($images[0]); // Just the file name
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROV Dashboard</title> 

    <style> 
        h1 {
            text-align: center;
        }
        body {
            background-color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        img {
            border: 1px solid #ccc;
            margin-top: 10px;
        }
        .section {
            margin-bottom: 40px;
        }
    </style>

    <script>
        function updateSensorData() {
            fetch("sensor_data.php")
                .then(response => response.json())
                .then(data => {
                    document.getElementById("temperature").innerText = data.temperature + " °C";
                    document.getElementById("depth").innerText = data.depth + " m";
                    document.getElementById("pressure").innerText = data.pressure + " mbar";
                })
                .catch(error => console.error("Error fetching sensor data:", error));
        }

        setInterval(updateSensorData, 30000); // Update every 5 seconds
    </script>
</head>
<body>

    <h1>ROV Senior Design Spring 2025</h1>

    <!-- Video Feed Section -->
    <div class="section">
        <h2>ROV Video Stream</h2>
        <iframe src="http://10.0.0.116:5000/video_feed" width="640" height="480" frameborder="0" allowfullscreen></iframe>
    </div>

    <!-- Sensor Data Section -->
    <div class="section">
        <h2>Sensor Readings</h2>
        <p><strong>Temperature:</strong> <span id="temperature"><?php echo htmlspecialchars($temperature); ?> °C</span></p>
        <p><strong>Depth:</strong> <span id="depth"><?php echo htmlspecialchars($depth); ?> m</span></p>
        <p><strong>Pressure:</strong> <span id="pressure"><?php echo htmlspecialchars($pressure); ?> mbar</span></p>

    </div>

    <!-- Latest Snapshot Section -->
    <div class="section">
        <h2>Latest Snapshot</h2>
        <?php if ($latestImage): ?>
            <img src="Gallery/<?php echo $latestImage; ?>" alt="Latest Snapshot" width="640" height="480">
            <p><strong>File:</strong> <?php echo htmlspecialchars($latestImage); ?></p>
        <?php else: ?>
            <p>No snapshot available.</p>
        <?php endif; ?>
        <div class="gallery-button">
            <a href="http://10.0.0.116/Gallery.php" target="_blank">View Full Gallery</a>
        </div>
    </div>

    <!-- Motor Control Section -->
    <div class="section">
        <h2>Motor Control</h2>
        <form method="post">
            <button name="command" value="Q">Stop</button>
        </form>
    </div>

</body>
</html>


