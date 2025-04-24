import pygame
import paramiko
import time

# Raspberry Pi SSH Info
pi_ip = '10.0.0.116'
pi_user = 'salgadoe'
pi_pass = 'Jumping@Turtles6211'

# Setup SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(pi_ip, username=pi_user, password=pi_pass)

# Setup controller
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise Exception("No controller detected.")

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller connected: {joystick.get_name()}")

DEADZONE = 0.2
last_command = None
last_snapshot_time = 0
last_led_time = 0

def send_command(cmd):
    global last_command
    if cmd != last_command:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(pi_ip, username=pi_user, password=pi_pass)

            # Kill all other scripts first
            ssh.exec_command("pkill -f forward.py; pkill -f backward.py; pkill -f left.py; pkill -f right.py; pkill -f dive.py; pkill -f surface.py; pkill -f stop.py")
            time.sleep(0.3)
            ssh.exec_command(f"python3 /var/www/html/{cmd}.py")

            ssh.close()
            last_command = cmd
            print(f"Sent command: {cmd}")

        except Exception as e:
            print(f"SSH command failed: {e}")

try:
    while True:
        pygame.event.pump()

        # X button (button 0) triggers snapshot
        if joystick.get_button(0):
            current_time = time.time()
            if current_time - last_snapshot_time > 0.5:  # debounce
                send_command("snapshot")
                last_snapshot_time = current_time

        # O button (button 1) turns LED ON
        if joystick.get_button(1):
            current_time = time.time()
            if current_time - last_led_time > 0.5:  # debounce
                send_command("LEDON")
                last_led_time = current_time

        # LEFT Stick Y-axis → up/down
        left_y = -joystick.get_axis(1)

        # RIGHT Stick Y and X
        right_y = -joystick.get_axis(3)
        right_x = joystick.get_axis(2)

        if abs(left_y) > DEADZONE:
            if left_y > 0:
                send_command("dive")
            else:
                send_command("surface")
        elif abs(right_y) > DEADZONE:
            if right_y > 0:
                send_command("forward")
        elif abs(right_x) > DEADZONE:
            if right_x > 0:
                send_command("turn_right")
            else:
                send_command("turn_left")
        else:
            send_command("stop")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("Exiting...")
    ssh.close()
    pygame.quit()
