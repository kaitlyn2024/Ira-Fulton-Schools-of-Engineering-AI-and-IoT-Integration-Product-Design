#Spencer

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.OUT)
servo1 = GPIO.PWM(16, 25)  # Lower frequency for better torque (50 Hz)

servo1.start(0)
print('Waiting for 2 seconds')
time.sleep(2)

print('Rotating to the maximum torque position')

duty = 2

# Simulate gear reduction by slowing down the movement
while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(0.2)  # Slower movement for more torque
    duty += 1

# Give the servo more time to exert force
time.sleep(1)


# Return to neutral position slowly
print('Turning back to neutral position')
for _ in range(7, 2, -1):
    servo1.ChangeDutyCycle(_)  # Decreasing duty cycle for slower return
    time.sleep(0.2)

time.sleep(2)

print('Returning to the starting position')
# Return to the starting position slowly
for _ in range(2, 0, -1):
    servo1.ChangeDutyCycle(_)  # Decreasing duty cycle for slower return
    time.sleep(0.2)

servo1.ChangeDutyCycle(0)

servo1.stop()
GPIO.cleanup()

