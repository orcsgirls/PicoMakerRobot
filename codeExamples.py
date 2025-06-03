import time
import board
from robot import Sonar, Motors, Leds, Linesensor, Button, Buzzer

# Pins for the various sensors. Change to match your setup

TRIGGER_PIN = board.GP16
ECHO_PIN = board.GP17
LINE_SENSOR_LEFT_PIN = board.GP27
LINE_SENSOR_RIGHT_PIN = board.GP3

#-------------------------------------------------------------------
# Color LEDs
#-------------------------------------------------------------------

# Make Leds Object
leds=Leds()

# Turn both LEDs red
leds.color(0xff0000)

# Cycle through the rainbow (hue is the angle on the colorwheel)
for i in range(255):
    leds.hue(i)
    time.sleep(0.005)

# Flashing lights
for i in range(10):
    leds.left_color(0xff0000)
    leds.right_color(0x0000ff)
    time.sleep(0.5)
    leds.left_color(0x0000ff)
    leds.right_color(0xff0000)
    time.sleep(0.5)
    
# Turn off
leds.off()

#-------------------------------------------------------------------
# Ultrasonic Sensor
#-------------------------------------------------------------------

# Make the object
sonar=Sonar(TRIGGER_PIN, ECHO_PIN)

# Measure distance
distance = sonar.distance
print(distance)

# Check until distance is less than 5cm, thet turn leds red and stop
leds.color(0x00ff00)

while distance > 5.0:
    distance = sonar.distance
    print(distance)
    time.sleep(0.1)

leds.color(0xff0000)

#-------------------------------------------------------------------
# Line tracking sensor
#-------------------------------------------------------------------

# Making object - for single sensor, make only one object :)
linesensor_right = Linesensor(LINE_SENSOR_RIGHT_PIN)
linesensor_left = Linesensor(LINE_SENSOR_LEFT_PIN)

# Waiting for both sensors to see a line
leds.color(0x00ff00)

while not (linesensor_left.line_detected and linesensor_right.line_detected):
    print(f"Sensor left: {linesensor_left.line_detected} - sensor right {linesensor_right.line_detected}")

leds.color(0xff00)

#-------------------------------------------------------------------
# Motors
#-------------------------------------------------------------------

# Make the object
motors = Motors()

# Drive forward one second and then back
motors.forward(duration=1.0)
motors.backward(duration=1.0)

# Done

