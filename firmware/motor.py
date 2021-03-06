from machine import Pin
import uasyncio
from time import sleep

class Motor_Controller():
  DIRECTION_UP = 1
  DIRECTION_DOWN = 0
  MOTOR_DELAY = 0.0005 # In seconds
  LOWERED_POSITION = 170_000 #170_000 is for 1/32 step  Good for highest microstepping resolution
  MOTOR_FILE = "motor_position.txt"
  WATCHDOG_THRESHOLD = 2 / MOTOR_DELAY
  
  def __init__(self, wdt):
    self.stepPin = Pin(14, Pin.OUT)
    self.direction = Pin(12, Pin.OUT) # on is up, off is down
    self.motor = Pin(27, Pin.OUT) # Connected to the sleep pin
    self.motor.off()
    self.motor_position: int = self.load_saved_position()
    self.running = False
    self.wdt = wdt
    
  def get_normalised_height(self):
    return float(self.motor_position) / float(self.LOWERED_POSITION)

  def load_saved_position(self)->int:
    motor_position = 0
    try:
      with open(self.MOTOR_FILE, "r") as f:
        motor_position = int(f.read())  

      print(f"Loaded motor position of {motor_position}")
    except:
      print("Motor position file doesn't exist / is corrupted :(, creating it!")
      with open(self.MOTOR_FILE, "w") as f:
        f.write(str(motor_position))
      
    return motor_position

  def set_direction_up(self):
    self.direction.on()

  def set_direction_down(self):
    self.direction.off()

  def step(self):
    '''steps the motor in the current direction, note: the motor must be turned on'''
    self.stepPin.on()
    sleep(self.MOTOR_DELAY)
    self.stepPin.off()
    if self.direction.value() == self.DIRECTION_UP:
      self.motor_position -= 1
    else:
      self.motor_position += 1

  def save_position(self):
    '''saves the current motor position to file'''
    with open(self.MOTOR_FILE, 'w') as f:
      f.write(str(self.motor_position))

  def lower_blind(self):
    self.direction.value(self.DIRECTION_DOWN)
    self.motor.on()
    print("lowering blind")
    self.running = True
    watchdog_counter = 0
    while self.motor_position < self.LOWERED_POSITION:
      self.step()
      sleep(self.MOTOR_DELAY)
      # This async so we should feed the watchdog
      if watchdog_counter > self.WATCHDOG_THRESHOLD:
        self.wdt.feed()
        watchdog_counter = 0
      watchdog_counter+=1

    self.motor.off()
    self.save_position()
    print("blind lowered!")
    self.running = False

  def raise_blind(self):
    self.direction.value(self.DIRECTION_UP)
    self.motor.on()
    self.running = True
    print("raising blind")
    watchdog_counter = 0
    while self.motor_position > 0:
      self.step()
      sleep(self.MOTOR_DELAY)
      if watchdog_counter > self.WATCHDOG_THRESHOLD:
        self.wdt.feed()
        watchdog_counter = 0
      watchdog_counter+=1

    self.motor.off()
    self.save_position()
    print("blind raised!")
    self.running = False
