import network
import credentials
from machine import freq, Pin
from time import sleep, localtime
from microdot_asyncio import Microdot, Response, send_file
import uasyncio
import ntptime
import suncalc
from motor import Motor_Controller
from machine import WDT

LAT = 53.576866
LONG = -2.428219

HOSTNAME = "twilight"

def get_wlan():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.config(dhcp_hostname=HOSTNAME)
  wlan.ifconfig(('192.168.0.201', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
  wlan.connect(credentials.SSID, credentials.PASSWORD)

  print(f"connecting to wlan {credentials.SSID}, with password: {credentials.PASSWORD}")
  status_LED.off()
  while not wlan.isconnected():
    print(".", end="")
    status_LED.on()
    sleep(0.5)
    status_LED.off()
    sleep(0.5)
  print("connected!")
  status_LED.on()
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

async def feed_watchdog():
  while True:
    status_LED.off()
    if wlan.isconnected():
      wdt.feed()
      await uasyncio.sleep_ms(100)
      status_LED.on()
      
    await uasyncio.sleep(2)

    

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

@app.route('api/ha/switch', methods=['GET','POST'])
def home_assistant_switch(request):
  global motor
  if request.method == 'POST':
    state = request.body.decode('utf-8')
    print(state)
    if state == "ON":
      motor.lower_blind()
      print("LOWERING BLIND")
    elif state == "OFF":
      motor.raise_blind()
    return Response(status_code=200)
  elif request.method == 'GET':
    height = motor.get_normalised_height()
    if height >= 1:
      state = 'ON'
    else:
      state = 'OFF'
    print(f'current state: {state}')
    return Response(status_code=200, body=state)

@app.route('api/lower_blind')
def lower_blind(request):
  if (motor.running):
    return Response(status_code=503) # Service unavailable code
  else:
    motor.lower_blind()
    return Response(body={'height': motor.get_normalised_height()})

@app.route('api/raise_blind')
def raise_blind(request):
  if (motor.running):
    return Response(status_code=503) # Service unavailable code
  else:
    motor.raise_blind()
    return Response(body={'height': motor.get_normalised_height()})

@app.route('api/current_time')
async def current_time(request):
  return str(localtime())

@app.route('api/normalised_height')
async def normalised_height(request):
  return Response(body={'height': motor.get_normalised_height()})

@app.route('api/sun_times')
async def sun_times(request):
  times = suncalc.getTimes(localtime(), LAT, LONG)
  return Response(body=times)

wdt = WDT(timeout=5000) # Watchdog with timeout of 5 seconds
motor = Motor_Controller(wdt)

status_LED = Pin(26, Pin.OUT)

freq(240_000_000) # Set the clock speed to maximum
wlan = get_wlan()
uasyncio.create_task(set_clock())
uasyncio.create_task(feed_watchdog())
uasyncio.create_task(app.start_server(debug=True, port=80))
uasyncio.get_event_loop().run_forever()
