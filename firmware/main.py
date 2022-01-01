import network
import credentials
from machine import Pin
from time import sleep
from microdot import Microdot, Response

HOSTNAME = "twilight"

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
def index(request):
  return Response(body="hi")


motor = Pin(32, Pin.OUT)
wlan = get_wlan()
app.run(debug=True, port=80)
print("hi from after the run")

