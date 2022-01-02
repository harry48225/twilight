import network
import credentials
from machine import Pin, freq
from time import sleep
from microdot_asyncio import Microdot, Response, send_file
import uasyncio

HOSTNAME = "twilight"

motor = Pin(32, Pin.OUT)
motor_on = False

async def motor_loop():
  global motor_on
  while True:
    print(motor_on)
    while (motor_on):
      motor.on()
      motor.off()
      await uasyncio.sleep(0.0005)

    await uasyncio.sleep_ms(100)

def get_wlan():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.config(dhcp_hostname=HOSTNAME)
  wlan.connect(credentials.SSID, credentials.PASSWORD)

  print(f"connecting to wlan {credentials.SSID}, with password: {credentials.PASSWORD}")
  while not wlan.isconnected():
    pass
  print("connected!")
  return wlan

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

freq(240_000_000) # Set the clock speed to maximum
wlan = get_wlan()
uasyncio.create_task(app.start_server(debug=True, port=80))
#uasyncio.create_task(motor_loop())
print("after server")
uasyncio.get_event_loop().run_forever()
