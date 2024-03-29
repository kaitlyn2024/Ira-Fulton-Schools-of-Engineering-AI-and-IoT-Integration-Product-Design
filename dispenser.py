#Spencer
#theoretical code for dispenser
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

FEED_SERVO_CONTROL_PIN = 18
GPIO.setup(FEED_SERVO_CONTROL_PIN, GPIO.OUT)

PWM_FREQUENCY = 100
FULL_SPEED_FORWARD_DC = 20
FULL_SPEED_BACKWARD_DC = 10

pwm = GPIO.PWM(FEED_SERVO_CONTROL_PIN, PWM_FREQUENCY)
pwm.start(FULL_SPEED_FORWARD_DC)

time.sleep(3)

pwm.ChangeDutyCycle(FULL_SPEED_BACKWARD_DC)time.sleep(3)

pwm.stop()
time.sleep(0.5)
GPIO.cleanup()
