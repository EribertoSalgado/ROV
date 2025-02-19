<?php
if (isset($_POST['command'])) {
    // Write the motor command to the motor_command.txt file
    file_put_contents("/var/www/html/motor_command.txt", $_POST['command']);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROV Control Panel</title>
    <script>
        function takeSnapshot() {
            var img = document.getElementById("snapshot");
            img.src = "http://10.0.0.116:5000/snapshot?" + new Date().getTime();  // Adding timestamp to prevent caching
        }
    </script>
</head>
<body>
    <h1>ROV Control Panel</h1>

    <!-- Video Feed Section -->
    <h2>ROV Video Stream</h2>
    <!-- Embed the video feed in an iframe (use your own URL for the video feed) -->
    <iframe src="http://10.0.0.116:5000/video_feed" width="640" height="480" frameborder="0" allowfullscreen></iframe>

    <!-- Snapshot Section -->
    <h2>Snapshot</h2>
    <button onclick="takeSnapshot()">Take Snapshot</button>
    <br>
    <img id="snapshot" src="" alt="Snapshot will appear here" width="640" height="480" />

    <!-- Motor Control Section -->
    <h2>Motor Control Panel</h2>
    <form method="post">
        <button name="command" value="F">Forward</button>
        <button name="command" value="R">Reverse</button>
        <button name="command" value="Q">Stop</button>
    </form>
</body>
</html>

