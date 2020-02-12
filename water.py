import RPi.GPIO as gpio
import time

motors = [1,1,1,1]
exit = False
fillTime = 0
gpio.setmode(gpio.BOARD)


for motor in motors:
    gpio.setup(motor, gpio.OUT)

try:
    while not exit:
        hour, minute = map(int, time.strftime("%H %M").split())
        if hour in [6, 10, 14, 18, 22]:
            for motor in motors:
                gpio.output(motor, True)
            time.sleep(fillTime)
            for motor in motors:
                gpio.output(motor, False)
        time.sleep(3600)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
except:
    print("Other error occurred")
finally:
    gpio.cleanup()
