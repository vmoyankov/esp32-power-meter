import machine
import time

from pzem import PZEM
from settings import Config

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
    do_connect()
    
    sleep = 60 * 1000 
    # define hardware uart
    uart = machine.UART(1, baudrate=9600, rx=11, tx=12)

    # define PZEM device [UART, ADDR = 0xF8 (default)]
    dev = PZEM(uart=uart)

    # Set new address
    if dev.setAddress(0x05):
        print("New device address is {}".format(dev.getAddress()))


    while True:

        # Read the new values
        if dev.read():

            # print the reading value (public filed)
            print(dev.toString())
            #print(dev.getCurrent())

        # wait for the next reading
        time.sleep_ms(sleep - dev.getReadingTime())


main()


