<?php
if (isset($_GET['brightness'])) {
    $brightness = intval($_GET['brightness']);
    $command = escapeshellcmd("python3 /var/www/html/control_led.py " . $brightness);
    shell_exec($command);
}
?>
