import json
import machine
import ntptime
import time
import uasyncio as asyncio

from pzem import PZEM
import web
import static_pages

from settings import Config


TIME_OFFSET = 946684800  # 2000-01-01T02:00:00  (New epoch in EET)


app = web.App(host='0.0.0.0', port=80)
dev = None

async def static_handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    # write page body
    w.write(static_pages.html.get(r.path, b"Not Found"))
    await w.drain()

for path in static_pages.html.keys():
    app.handlers.append((path, ['GET'], static_handler))


@app.route('/data')
async def read_data(r, w):
    dev.read()
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: application/json\r\n')
    w.write(b'\r\n')

    data = {
            'time': time.time() + TIME_OFFSET,
            'u': dev.getVoltage(),
            'i': dev.getCurrent(),
            'p': dev.getActivePower(),
            'pf': dev.getPowerFactor(),
            'e': dev.getActiveEnergy()
            }
    w.write(json.dumps(data).encode('utf8'))

    await w.drain()

@app.route('/metrics')
async def prometheus_data(r, w):
    dev.read()
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: application/json\r\n')
    w.write(b'\r\n')

    data = f'''powermeter_voltage {dev.getVoltage()}
powermeter_current {dev.getCurrent()}
powermeter_power {dev.getActivePower()}
powermeter_pf {dev.getPowerFactor()}
powermeter_energy {dev.getActiveEnergy()}
'''.encode()
    
    w.write(data)
    await w.drain()


def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():
        print('network config:', wlan.ifconfig())
        return

    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(Config.ssid, Config.wifi_pass)
        for _ in range(30):
            if wlan.isconnected():
                print('network config:', wlan.ifconfig())
                return
            time.sleep(1)
            print("Waiting to connect ...")
        machine.reset()


def main():
    global dev

    do_connect()
    ntptime.settime()
    
    # define hardware uart
    uart = machine.UART(1, baudrate=9600, rx=11, tx=12)

    # define PZEM device [UART, ADDR = 0xF8 (default)]
    dev = PZEM(uart=uart)

    # Set new address
    if dev.setAddress(0x05):
        print("New device address is {}".format(dev.getAddress()))


    loop = asyncio.get_event_loop()
    loop.create_task(app.serve())
    loop.run_forever()


main()

