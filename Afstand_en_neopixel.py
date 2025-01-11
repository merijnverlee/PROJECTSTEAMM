# Import the necessary libraries
from pico_i2c_lcd import I2cLcd
from lcd_api import LcdApi
from machine import Pin, I2C
import neopixel
import time

# Pin configuration for HC-SR04
Trig = Pin(2, Pin.OUT)
Echo = Pin(3, Pin.IN)

# I2C configuration for the LCD
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
I2C_ADDR = i2c.scan()[0]  
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# NeoPixel configuration
LED_PIN = 6  # Data pin for WS2812
LED_COUNT = 8  # 8 leds
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)


def distance():
    Trig.value(0)
    time.sleep_us(4)
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)
    
    # Meet de echo duration
    try:
        while Echo.value() == 0:
            low = time.ticks_us()
        while Echo.value() == 1:
            high = time.ticks_us()
    except:
        return None  # Return None if no signal is received
    
    duration = high - low
    return duration


def control_leds(distance_cm):
    if distance_cm <= 30:  # als de afstand gelijk of minder is dan 30 cm gaat het knipperen.
        for i in range(LED_COUNT):
            np[i] = (255, 0, 0)  # rood
        np.write()
        time.sleep(0.2)  # voor het kniperende effect
        for i in range(LED_COUNT):
            np[i] = (0, 0, 0)  # uit
        np.write()
        time.sleep(0.2)
    else:  
        for i in range(LED_COUNT):
            np[i] = (0, 255, 0)  # groen
        np.write()

# Het scherm is aan het starten
def startText():
    lcd.move_to(0, 0)  
    lcd.putstr("Scherm start op")
    for i in range(0, 15):
        lcd.move_to(i, 1)
        lcd.putstr(".")
        time.sleep(0.3)
        
# Initialiseren van het scherm
startText()
lcd.clear()

# Main loop
while True:
    dis = distance()  # Meet de afstand
    if dis is None:
        lcd.move_to(0, 0)
        lcd.putstr("No signal     ")  
        lcd.move_to(0, 1)
        lcd.putstr("Try again     ")
    else:
        cm = dis / 29 / 2  # Het wordt berekend in centimeters
        cm = int(cm)
        inch = dis / 74 / 2  # Ook in inch
        inch = int(inch)
        
        # Update LCD
        lcd.move_to(0, 0)
        lcd.putstr("Afstand - ")
        lcd.putstr("{:3.0f}cm ".format(cm))
        
        lcd.move_to(0, 1)
        lcd.putstr("Afstand - ")
        lcd.putstr("{:3.0f}inch ".format(inch))
        
        # Met deze functie bestuur je de leds
        control_leds(cm)
    
    time.sleep(0.5)  
