import time
import board
from robot import Sonar, Motors, Leds, Linesensor, Button, Buzzer

# Pins for the ultrasonic sensor. Change to match your setup

TRIGGER_PIN = board.GP16
ECHO_PIN = board.GP17
LINE_SENSOR_LEFT_PIN = board.GP27
LINE_SENSOR_RIGHT_PIN = board.GP3
BUTTON1_PIN = board.GP20
BUTTON2_PIN = board.GP21

print("startplot:","distance")   # This line will allow plotting

# Loop to measure
sonar=Sonar(TRIGGER_PIN, ECHO_PIN)

# Motors
motors = Motors()
#motors.forward(speed=0.7, duration=1.0)
#motors.backward(speed=0.7, duration=1.0)
#motors.left(duration=0.5, tankmode=False)
#motors.right(duration=0.5, tankmode=False)

# Neopixels

leds=Leds()
leds.left_color(0xff0000)
#for i in range(255):
#    leds.left_color_hue(i)
#    leds.right_color_hue(i+128)
#    time.sleep(0.005)

print(leds.brightness)
leds.brightness = 0.5
time.sleep(1.0)
leds.off()

linesensor_right = Linesensor(LINE_SENSOR_RIGHT_PIN)
linesensor_left = Linesensor(LINE_SENSOR_LEFT_PIN)

button1 = Button(BUTTON1_PIN)
button2 = Button(BUTTON2_PIN)

# Melody
MELODY_NOTE = [659, 659, 0, 659, 0, 523, 659, 0, 784]
MELODY_DURATION = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.2]

MELODY_NOTE = []
MELODY_DURATION = []

for i in range(400,700,10):
    MELODY_NOTE.append(i)
    MELODY_DURATION.append(0.02)
for i in range(700,400,-10):
    MELODY_NOTE.append(i)
    MELODY_DURATION.append(0.02)

buzzer=Buzzer()
#buzzer.beep()
#buzzer.alert()
#buzzer.play(MELODY_NOTE, MELODY_DURATION)
#buzzer.siren(repeat=3)

for i in range(50):
    print(button1.pressed, button2.pressed)
    time.sleep(0.1)

for i in range(20):
    print(f"Distance {sonar.distance:.2f}")
    time.sleep(1.0)

