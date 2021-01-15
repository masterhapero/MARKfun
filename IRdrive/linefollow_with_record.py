from maix_motor import Maix_motor
from gpio import *
import utime
import sensor, image, lcd, video

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_hmirror(1)
sensor.set_vflip(1)

sensor.run(1)
sensor.skip_frames(30)

gpio_init()

Maix_motor.servo_angle(2, 30)
Maix_motor.motor_run(0, 0, 0)

speaker(3, 8, 1)
utime.sleep_ms(2000)

# Line sensor inputs
value5 = Line_Finder(5, 1)
value6 = Line_Finder(6, 1)

v = video.open("/sd/capture.avi", audio = False, record=1, interval=40000, quality=50)
#okay_to_record = False

while value5 or value6:
    img = sensor.snapshot()
    lcd.display(img)
    if value5 and value6:
        Maix_motor.motor_run(25,25,0)
        #if okay_to_record:
        #    # This takes longer, try do it in clear
        #    v.record(img)
        #else:
        #    utime.sleep_ms(40)
        # okay_to_record = True
        #Maix_motor.motor_motion(1, 1, 0)
    else:
        okay_to_record = False
        if value5:
            Maix_motor.motor_run(0,25,0)
        if value6:
            Maix_motor.motor_run(25,0,0)
        # utime.sleep_ms(40)

    v.record(img)
    value5 = Line_Finder(5, 1)
    value6 = Line_Finder(6, 1)

Maix_motor.motor_run(0, 0, 0)
speaker(3, 8, 1)

v.record_finish()
v.__del__()

while True:
    utime.sleep_ms(40)
