import RPi.GPIO as GPIO
import serial

arduino = serial.Serial('/dev/ttyUSB0', 9600)

GPIO.setmode(GPIO.BOARD)

while(True):
    lido = arduino.readline()
    lido = lido.decode("utf-8")