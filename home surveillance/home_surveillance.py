from picamera import PiCamera as pcam
import RPi.GPIO as gp
import time
import yagmail
import os

#camera setup
print('waiting for 2 secs to initailize camera')
camera = pcam()
camera.resolution = (1280, 720)
camera.rotation = 180
time.sleep(2)
print('Camera setup OK')

#email setup
password = ''
with open('/home/pi/.local/share/.email_password', 'r') as f:
    password = f.read()
yag = yagmail.SMTP('piraspberry357@gmail.com', password)
print ('EMAIL setup OK')

#GPIO setup
PIR_PIN = 4
led = 17
gp.setmode(gp.BCM)
gp.setup(led, gp.OUT)
gp.setup(PIR_PIN, gp.IN, pull_up_down = gp.PUD_DOWN)
print('GPIOs setup OK')
print('Everything has been setup')


#to take picture after detected motion and update log file
counter = 1
while True:
    time.sleep(0.0001)
    if gp.input(PIR_PIN) == 1:
        file = '/home/pi/camera_folder/pic' + str(counter) + '.jpg'
        camera.capture(file)
        time.sleep(3)
        counter = counter + 1
        yag.send(to = 'user@gmail.com',
                 subject = 'surveillance',
                 contents = 'AHA! I caught you stealing bro.',
                 attachments = file)
        print('sent')
        f = open("log_file.txt","a+")
        f.write(file)
        f.write('\n')
        f.close()