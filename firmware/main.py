import network
import credentials
from machine import Pin, freq
from time import sleep, localtime
from microdot_asyncio import Microdot, Response, send_file
import uasyncio
import ntptime

HOSTNAME = "twilight"

class Motor_Contoller():
  def __init__(self):
    self.step = Pin(32, Pin.OUT)
    self.direction = Pin(33, Pin.OUT) # on is up, off is down
    self.motor = Pin(25, Pin.OUT) # Connected to the sleep pin
    self.motor.off()
    self.motor_position: int = self.load_saved_position()

  def load_saved_position(self)->int:
    motor_position = 0
    try:
      with open("motor_position.txt", "r") as f:
        motor_position = int(f.read())  

      print(f"Loaded motor position of {motor_position}")
    except OSError:
      print("Motor position file doesn't exist :(, creating it!")
      with open("motor_position.txt", "w") as f:
        f.write(str(motor_position))
      
    return motor_position


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

@app.route('api/on')
async def on(request):
  global motor_on
  motor_on = True
  return Response(body="motor turned on")

@app.route('api/off')
async def off(request):
  global motor_on
  motor_on = False
  return Response(body="motor turned off")

@app.route('api/current_time')
async def current_time(request):
  return str(localtime())

motor = Motor_Contoller()

freq(240_000_000) # Set the clock speed to maximum
wlan = get_wlan()
uasyncio.create_task(set_clock())
uasyncio.create_task(app.start_server(debug=True, port=80))
print("server started")
uasyncio.get_event_loop().run_forever()
