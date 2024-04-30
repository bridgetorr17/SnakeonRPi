import smbus
import time
import RPi.GPIO as GPIO
from sense_hat import SenseHat

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

sense = SenseHat()

Z_Pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(Z_Pin, GPIO.IN, GPIO.PUD_UP)

def analogRead(chn):
    bus.write_byte(address, cmd+chn)
    value = bus.read_byte(address)
    return value

def analogWrite(value):
    bus.write_byte_data(address, cmd, value)
    
while True:
    val_Z = GPIO.input(Z_Pin)
    val_Y = analogRead(0)
    val_X = analogRead(1)
    print("Click: %d, Y: %d, X: %d" % (val_Z, val_Y, val_X))
    #sense.show_message("hi")
    time.sleep(1)
