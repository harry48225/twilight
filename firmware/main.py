import network
import credentials
from machine import Pin, freq
from time import sleep, localtime
from microdot_asyncio import Microdot, Response, send_file
import uasyncio
import ntptime
import suncalc

LAT = 53.576866
LONG = -2.428219

HOSTNAME = "twilight"

class Motor_Contoller():
  DIRECTION_UP = 1
  DIRECTION_DOWN = 0
  MOTOR_DELAY = 0.000025
  LOWERED_POSITION = 170_000/2 #170_000 is for 1/32 step  Good for highest microstepping resolution
  MOTOR_FILE = "motor_position.txt"
  def __init__(self):
    self.stepPin = Pin(32, Pin.OUT)
    self.direction = Pin(33, Pin.OUT) # on is up, off is down
    self.motor = Pin(25, Pin.OUT) # Connected to the sleep pin
    self.motor.off()
    self.motor_position: int = self.load_saved_position()
    self.running = False

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

  async def step(self):
    '''steps the motor in the current direction, note: the motor must be turned on'''
    self.stepPin.on()
    self.stepPin.off()
    if self.direction.value() == self.DIRECTION_UP:
      self.motor_position -= 1
    else:
      self.motor_position += 1

  def save_position(self):
    '''saves the current motor position to file'''
    with open(self.MOTOR_FILE, 'w') as f:
      f.write(str(self.motor_position))

  async def lower_blind(self):
    self.direction.value(self.DIRECTION_DOWN)
    self.motor.on()
    print("lowering blind")
    self.running = True
    while self.motor_position < self.LOWERED_POSITION:
      await self.step()
      await uasyncio.sleep(self.MOTOR_DELAY)
    self.motor.off()
    self.save_position()
    print("blind lowered!")
    self.running = False

  async def raise_blind(self):
    self.direction.value(self.DIRECTION_UP)
    self.motor.on()
    self.running = True
    print("raising blind")
    while self.motor_position > 0:
      await self.step()
      await uasyncio.sleep(self.MOTOR_DELAY)
    self.motor.off()
    self.save_position()
    print("blind raised!")
    self.running = False

def get_wlan():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.config(dhcp_hostname=HOSTNAME)
  wlan.connect(credentials.SSID, credentials.PASSWORD)

  print(f"connecting to wlan {credentials.SSID}, with password: {credentials.PASSWORD}")
  while not wlan.isconnected():
    print(".", end="")
    sleep(1)
    pass
  print("connected!")
  return wlan

async def set_clock():
  print("trying to get ntp time")
  while True:
    try:
      ntptime.settime()
      print("successfully synced with ntp time")
      break
    except:
      print("error aquiring time, retrying")
      await uasyncio.sleep(1)



app = Microdot()

@app.route('/')
async def index(request):
  return send_file("public/index.html")

@app.route('/<re:([^a]|a[^p]|ap[^i]).*:path>')
async def not_api(request, path):
  # not an api endpoint so serve the public file
  try:
    # Kinda a big security risk... should probably sanitise these
    response = send_file(f"public/{path}")
  except:
    response = send_file("public/index.html")

  return response


@app.route('api/lower_blind')
async def lower_blind(request):
  if (motor.running):
    return Response(status_code=503) # Service unavailable code
  else:
    uasyncio.create_task(motor.lower_blind())
    return Response()

@app.route('api/raise_blind')
async def raise_blind(request):
  if (motor.running):
    return Response(status_code=503) # Service unavailable code
  else:
    uasyncio.create_task(motor.raise_blind())
    return Response()

@app.route('api/current_time')
async def current_time(request):
  return str(localtime())

@app.route('api/normalised_height')
async def normalised_height(request):
  print(motor.get_normalised_height())
  return Response(body={'height': motor.get_normalised_height()})

@app.route('api/sun_times')
async def sun_times(request):
  times = suncalc.getTimes(localtime(), LAT, LONG)
  return Response(body=times)

motor = Motor_Contoller()

freq(240_000_000) # Set the clock speed to maximum
wlan = get_wlan()
uasyncio.create_task(set_clock())
uasyncio.create_task(app.start_server(debug=True, port=80))
print("server started")
uasyncio.get_event_loop().run_forever()
