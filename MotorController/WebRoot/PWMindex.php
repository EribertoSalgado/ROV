<?php
if (isset($_POST['command'])) {
    file_put_contents("/var/www/html/motor_command.txt", $_POST['command']);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Motor Control</title>
</head>
<body>
    <h2>Motor Control Panel</h2>
    <form method="post">
        <button name="command" value="F">Forward</button>
        <button name="command" value="R">Reverse</button>
        <button name="command" value="Q">Stop</button>
    </form>
</body>
</html>
