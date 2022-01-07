import network
import credentials
from machine import freq
from time import sleep, localtime
from microdot_asyncio import Microdot, Response, send_file
import uasyncio
import ntptime
import suncalc
from motor import Motor_Controller

LAT = 53.576866
LONG = -2.428219

HOSTNAME = "twilight"

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
  return Response(body={'height': motor.get_normalised_height()})

@app.route('api/sun_times')
async def sun_times(request):
  times = suncalc.getTimes(localtime(), LAT, LONG)
  return Response(body=times)

motor = Motor_Controller()

freq(240_000_000) # Set the clock speed to maximum
wlan = get_wlan()
uasyncio.create_task(set_clock())
uasyncio.create_task(app.start_server(debug=True, port=80))
uasyncio.get_event_loop().run_forever()
