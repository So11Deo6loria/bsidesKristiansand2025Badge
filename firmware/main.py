from microdot import Microdot, Response, send_file
from microdot.utemplate import Template
import gc
import json
import machine
from helpers import Helpers
from flagManager import FlagManager
from scanManager import ScanManager
from serialManager import SerialManager
from networkManager import NetworkManager
from configManager import ConfigManager
from ledManager import LEDManager
from detectManager import DetectManager
import utime as time
# import _thread
import constants
import _asyncio as asyncio

#Loading badge Configuration
helpers = Helpers()
device_id = helpers.device_name
networkSetting = 'WIFI'
bootupTime = time.ticks_ms()

configManager = ConfigManager()
password = helpers.generate_password(4)
print(f"Generating Random password: {password}")
# Generate random psk and store in database
if configManager.configData['apPassword'] == 'password':
	configManager.update_config('apPassword', password)

ledManager = LEDManager(configManager.configData['startupColor'])
ledManager.boot()
time.sleep(1)
ledManager.blink_morse(password)

#testmode = False
# print("Battery Voltage", detectManager.read_v_batt())
# print("USB Voltage", detectManager.read_v_usb())
# print("Starting Up Sensor Manager")
gc.collect()

# Removed bootPin functionality

flagManager = FlagManager(device_id)
networkManager = NetworkManager(device_id, configManager.configData['apPassword'], networkSetting) 
scanManager = ScanManager(networkManager.wlan, flagManager)
serialManager = SerialManager()
app = Microdot()
Response.default_content_type = 'text/html'
ledManager.blink_morse(116)
gc.collect()

# Page Routes
@app.route('/')
async def index(request):
	gc.collect()
	flag = flagManager.retrieve_flag('easy')
	return await Template('index.html').render_async(device_id=device_id, flag=flag)

@app.route('/admin')
async def admin(request):
	gc.collect()
	flag = flagManager.retrieve_flag('authorized')
	return await Template('admin.html').render_async(device_id=device_id, flag=flag)

@app.route('/flags')
async def flags(request):
	gc.collect()
	return await Template('flags.html').render_async(device_id=device_id)

@app.route('/test')
async def test(request):
	gc.collect()
	return await Template('test.html').render_async(device_id=device_id)

@app.route('/comms')
async def comms(request):
	gc.collect()
	return await Template('comms.html').render_async(device_id=device_id)

@app.route('/respond')
async def respond(request):
	gc.collect()
	return await Template('respond.html').render_async(device_id=device_id)

@app.route('/credits')
async def credits(request):
	return await Template('credits.html').render_async(device_id=device_id)

# Action Routes
@app.route('/trigger_interface', methods=['GET'])
async def trigger_interface(request):
	flag = flagManager.retrieve_flag('comms')
	flag_payload = f"{flag}\r\n"

	serialManager.transmit_comms(flag_payload)

	# Update the prompt after the interface action is complete.
	prompt = "Comms action completed!"
	return json.dumps({"prompt": prompt})

@app.route('/get_ap_name', methods=['GET'])
async def get_ap_name(request):
	responseText = scanManager.get_ap_name()
	return json.dumps({"response": responseText})

@app.route('/get_scan_update', methods=['GET'])
async def get_scan_update(request):
	jsonData = scanManager.get_scan_update()
	gc.collect()
	return json.dumps(jsonData)

@app.route('/contributors')
async def contributors(request):
	with open('contributors.json', 'r') as file:
		jsonData = json.load(file)
	return json.dumps(jsonData)

@app.route('/get_config')
async def get_config(request):
	return json.dumps(configManager.configData)

@app.route('/set_config', methods=['POST'])
async def set_config(request):
	jsonData = json.loads(request.body.decode('utf-8'))
	configManager.write_config(jsonData)
	return json.dumps({"success":True})

@app.route('/flags_status')
async def flags_status(request):
	gc.collect()
	flagStatus = flagManager.get_flags_status()
	return json.dumps(flagStatus)

@app.route('/capture_flag/<flag>')
async def captureFlag(request, flag):
	gc.collect()
	flag_value = request.args.get('value', 'default_value')

	flag_captured = flagManager.check_flag(flag.lower(), flag_value)

	if( True == flag_captured ):
		flagManager.set_flag_status( flag.lower(), True )
		#screenManager.updateFlagCount(flagManager.get_captured_flag_count())
		ledManager.boot()
	response_data = json.dumps({'captured': flag_captured})

	return response_data

# Static Routes
@app.route('/style.css')
async def style(request):
   return send_file('static/style.css', content_type='text/css')  # Specify content type

# Dynamic Routes
@app.route('/js/<path:path>')
async def js(request, path):
	if '..' in path and 'js' in path:
		# directory traversal is not allowed
		# This is example code from the microdot GitHub.
		# I make no claims that this will prevent path traversal. :)
		return 'Not found', 404
	return send_file('js/' + path)

@app.route('/static/<path:path>')
async def static(request, path):
	print(f"PATH: {path}")
	if '..' in path and 'png' in path:
		# directory traversal is not allowed
		# This is example code from the microdot GitHub.
		# I make no claims that this will prevent path traversal. :)
		return 'Not found', 404
	return send_file('static/' + path)

async def main():
	print( "Starting server" )
	await app.start_server(debug=True)
	print( "start_server returned, look for errors!" )

if __name__ == '__main__':
	try: 
		app.run(debug=True, port=configManager.configData['port'])
	except Exception as e:
            print(f"Error: {e}")