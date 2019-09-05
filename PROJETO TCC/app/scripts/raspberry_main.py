#imports
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO

import Adafruit_DHT
from pigredients.ics import hmc5883l

#GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH) #luz da camera

camera = cv2.VideoCapture(0)

kernel = np.ones((3,3), np.uint8)

# CONFIGURAÇÃO PORTAS
us1 = 17
echo_us1 = 16
us2 = 18
echo_us2 = 15
us3 = 19
echo_us3 = 14
tempumid = 13
#
#
bussola = hmc5883l.HMC5883L(debug=False)

def distancia(us, echo):
    GPIO.output(us, True)
    time.sleep(0.00001)
    GPIO.output(us, False)
    tempo0 = time.time()
    tempoT = time.time()
    while GPIO.input(echo) == 0:
        tempo0 = time.time()
    while GPIO.input(echo) == 1:
        tempoT = time.time()
    tempo = tempoT - tempo0
    distancia = (tempo * 34300 * 0.5)
    return distancia

while(True):
    ret, frame = camera.read()

    distNorte = distancia(us1,echo_us1)
    distLeste = distancia(us2,echo_us2)
    distOeste = distancia(us3,echo_us3)

    direcao_bussola = bussola.get_value()

    umidade, temperatura = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, tempumid)
GPIO.cleanup()