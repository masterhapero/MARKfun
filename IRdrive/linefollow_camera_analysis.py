from maix_motor import Maix_motor
from gpio import *
import utime
import sensor, image, lcd, video
import time

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
#sensor.set_vflip(1)

sensor.run(1)
sensor.skip_frames(30)
sensor.set_auto_whitebal(False)

try:
    gpio_init()
    Maix_motor.servo_angle(1, 90)
    Maix_motor.servo_angle(2, 30)
    Maix_motor.motor_run(0, 0, 0)
except Exception as e:
    # Not so interested
    print("Exception")

#speaker(3, 8, 1)

amIRunning = True
bThresh = 60
clock = time.clock()

while amIRunning:
    clock.tick()
    img = sensor.snapshot()
    imgbw = img.resize(160,120)
    imgbw = imgbw.to_grayscale()
    columnB = bytearray(120)
    maxBlack = 0
    columnBlackCount = 0
    totalBlack = 0
    for i in range(120):
        bc = 0
        for k in range(160):
            if imgbw.get_pixel(k,i) < bThresh:
                bc += 1
        columnB[i] = bc
        if maxBlack < bc:
            maxBlack = bc
        totalBlack += bc
    # Draw pixels and estimate driving direction
    navPos = 0
    navC = 0
    for i in range(120):
        if columnB[i] > maxBlack/2:
            navPos += i
            navC += 1
            img.set_pixel(columnB[i], i*2, (255,255,0))

    driveDir = 0
    if navC > 10:
        driveDir = navPos / navC
        for i in range(50):
            img.set_pixel(i,int(driveDir)*2,(255,255,255))
    # print(str(img)+" "+str(imgbw))
    # print(str(totalBlack)+" "+str(imgbw.get_pixel(60,80)))
    lcd.display(img)
    lcd.draw_string(0,0,str(totalBlack),lcd.RED)
    fps=clock.fps()
    lcd.draw_string(0,20, ("%2.1ffps" %(fps)),lcd.WHITE)
    if totalBlack < 500:
        amIRunning = False
    # Line sensor inputs
    value5 = Line_Finder(5, 1)
    value6 = Line_Finder(6, 1)
    if value5 and value6:
        Maix_motor.motor_motion(1, 1, 0)
    else:
        if value5:
           Maix_motor.motor_motion(1, 3, 0)
        if value6:
           Maix_motor.motor_motion(1, 4, 0)


Maix_motor.motor_run(0, 0, 0)
speaker(3, 8, 1)

lcd.draw_string(0,20,"GAME OVER",lcd.RED)

while True:
    utime.sleep_ms(40)


