# windows ssh script
import pygame
import paramiko
import time

# Raspberry Pi SSH Info
pi_ip = '10.0.0.116'
pi_user = 'salgadoe'
pi_pass = 'Jumping@Turtles6211'

# Connect to RPi over SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(pi_ip, username=pi_user, password=pi_pass)

# Setup pygame and controller
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise Exception("No PS5 controller detected. Connect via USB or Bluetooth.")

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Controller connected: {joystick.get_name()}")

DEADZONE = 0.1

def send_command(cmd):
    ssh.exec_command(cmd)

try:
    while True:
        pygame.event.pump()
        y_axis = -joystick.get_axis(1)

        if abs(y_axis) < DEADZONE:
            y_axis = 0

        if y_axis > 0.5:
            print("Forward")
            send_command("python3 /var/www/html/forward.py")
        elif y_axis < -0.5:
            print("Backward")
            send_command("python3 /var/www/html/backward.py")
        else:
            print("Stop")
            send_command("python3 /var/www/html/stop.py")

        # Optional: update watchdog heartbeat
        try:
            with open("heartbeat.txt", "w") as hb:
                hb.write(str(time.time()))
        except:
            pass  # skip if fails (e.g., permissions issue)

        time.sleep(0.2)

except KeyboardInterrupt:
    print("Exiting...")
    ssh.close()
    pygame.quit()
