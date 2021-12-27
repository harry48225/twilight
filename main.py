from machine import Pin
from time import sleep
motor = Pin(32, Pin.OUT)

while True:
  motor.on()
  motor.off()
  sleep(0.001)
  print("rotate")