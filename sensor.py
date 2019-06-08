"""
AUTHOR: Roman Belaire
Green Thumb
6/8/19
########
Sensor to track humidity, temperature, and light exposure
and insert to a csv. Eventually, want to upload to database
########
"""
import RPi.GPIO as gpio
import smbus
import time
import csv

gpio.setmode(gpio.BOARD)

LDR = 40 
"""
Pin setup: 
LDR output (S) = pin 40
SI7021 SDA = pin 3
SI7021 SCL = pin 5
"""
gpio.setup(LDR, gpio.IN)

bus = smbus.SMBus(1)
with open('log' + str(time.time()%10) + '.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    while True:
        light = gpio.input(LDR)
        bus.write_byte(0x40,0xF5)

        time.sleep(0.3)

        #SI7021 Address, 0x40 read 2 bytes humidity
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)

        #convert Data
        humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
        time.sleep(0.3)
        bus.write_byte(0x40, 0xF3)
        time.sleep(0.3)

        #SI7021 Address, 0x40 read 2 bytes temp
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)

        #convert data and output it
        cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
        fTemp = cTemp * 1.8 + 32

        print("Relative humidity : " + str(humidity))
        print("Temp: " + str(fTemp))
        print("Light: " + str(light))
        writer.writerow([fTemp, humidity, light])
